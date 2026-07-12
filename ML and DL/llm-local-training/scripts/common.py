from __future__ import annotations

import importlib.metadata as importlib_metadata
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

import torch

if TYPE_CHECKING:
    from datasets import DatasetDict


MODULE_ROOT = Path(__file__).resolve().parents[1]


@dataclass
class TrainingConfig:
    model_name: str = "HuggingFaceTB/SmolLM2-135M"
    train_file: str = "sample_data/python101_instructions.jsonl"
    validation_file: str | None = None
    output_dir: str = "outputs/smollm2_135m_python101"
    max_seq_length: int = 256
    validation_split_ratio: float = 0.2
    num_train_epochs: int = 5
    per_device_train_batch_size: int = 2
    per_device_eval_batch_size: int = 2
    gradient_accumulation_steps: int = 8
    learning_rate: float = 2e-4
    weight_decay: float = 0.01
    warmup_ratio: float = 0.03
    logging_steps: int = 2
    save_steps: int = 10
    eval_steps: int = 10
    seed: int = 42
    lora_r: int = 8
    lora_alpha: int = 16
    lora_dropout: float = 0.05
    gradient_checkpointing: bool = True
    max_new_tokens: int = 128

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "TrainingConfig":
        config = cls(**payload)
        config.train_file = str(resolve_module_path(config.train_file))
        config.output_dir = str(resolve_module_path(config.output_dir))
        if config.validation_file:
            config.validation_file = str(resolve_module_path(config.validation_file))
        else:
            config.validation_file = None
        return config

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def resolve_module_path(value: str) -> Path:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate
    return (MODULE_ROOT / candidate).resolve()


def load_config(config_path: str) -> TrainingConfig:
    with open(config_path, "r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return TrainingConfig.from_dict(payload)


def get_installed_version(package_name: str) -> str:
    try:
        return importlib_metadata.version(package_name)
    except importlib_metadata.PackageNotFoundError:
        return "not installed"


def build_dependency_help(exception: Exception, requirements_path: Path | None = None) -> str:
    requirements = requirements_path or (MODULE_ROOT / "requirements.txt")
    package_versions = {
        "torch": getattr(torch, "__version__", "unknown"),
        "transformers": get_installed_version("transformers"),
        "accelerate": get_installed_version("accelerate"),
        "peft": get_installed_version("peft"),
        "datasets": get_installed_version("datasets"),
        "evaluate": get_installed_version("evaluate"),
        "sentencepiece": get_installed_version("sentencepiece"),
    }

    version_summary = ", ".join(f"{name}={version}" for name, version in package_versions.items())
    return (
        "The local LLM training dependencies are missing or incompatible.\n"
        f"Detected versions: {version_summary}\n"
        f"Original error: {exception}\n"
        "This usually happens when `transformers` is newer than the installed `torch`, or when the "
        "Hugging Face training packages are only partially installed.\n"
        f"Fix it by reinstalling the pinned stack from:\n"
        f"  pip install -r \"{requirements}\"\n"
    )


def build_prompt(instruction: str, input_text: str = "") -> str:
    prompt = f"### Instruction:\n{instruction.strip()}\n\n"
    if input_text.strip():
        prompt += f"### Input:\n{input_text.strip()}\n\n"
    prompt += "### Response:\n"
    return prompt


def build_tokenize_function(tokenizer, max_seq_length: int):
    eos_token = tokenizer.eos_token or ""

    def tokenize_batch(batch: dict[str, list[Any]]) -> dict[str, list[list[int]]]:
        all_input_ids: list[list[int]] = []
        all_attention_masks: list[list[int]] = []
        all_labels: list[list[int]] = []

        total_items = len(batch["instruction"])
        inputs = batch.get("input", [""] * total_items)

        for index in range(total_items):
            instruction = str(batch["instruction"][index]).strip()
            input_text = str(inputs[index] or "").strip()
            output_text = str(batch["output"][index]).strip()

            prompt = build_prompt(instruction, input_text)
            full_text = f"{prompt}{output_text}{eos_token}"

            tokenized_full = tokenizer(
                full_text,
                truncation=True,
                max_length=max_seq_length,
                add_special_tokens=False,
            )
            tokenized_prompt = tokenizer(
                prompt,
                truncation=True,
                max_length=max_seq_length,
                add_special_tokens=False,
            )

            labels = tokenized_full["input_ids"].copy()
            prompt_length = min(len(tokenized_prompt["input_ids"]), len(labels))
            labels[:prompt_length] = [-100] * prompt_length

            all_input_ids.append(tokenized_full["input_ids"])
            all_attention_masks.append(tokenized_full["attention_mask"])
            all_labels.append(labels)

        return {
            "input_ids": all_input_ids,
            "attention_mask": all_attention_masks,
            "labels": all_labels,
        }

    return tokenize_batch


def load_instruction_datasets(config: TrainingConfig) -> "DatasetDict":
    from datasets import DatasetDict, load_dataset

    if config.validation_file:
        dataset = load_dataset(
            "json",
            data_files={"train": config.train_file, "validation": config.validation_file},
        )
        return DatasetDict(train=dataset["train"], validation=dataset["validation"])

    train_dataset = load_dataset("json", data_files={"train": config.train_file})["train"]
    split_dataset = train_dataset.train_test_split(
        test_size=config.validation_split_ratio,
        seed=config.seed,
    )
    return DatasetDict(train=split_dataset["train"], validation=split_dataset["test"])


def load_base_model_and_tokenizer(model_name: str):
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model_kwargs: dict[str, Any] = {"low_cpu_mem_usage": True}
    if torch.cuda.is_available():
        model_kwargs["torch_dtype"] = torch.float16

    model = AutoModelForCausalLM.from_pretrained(model_name, **model_kwargs)
    return model, tokenizer


def find_lora_target_modules(model) -> list[str]:
    preferred_modules = [
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj",
        "c_attn",
        "c_proj",
        "c_fc",
        "fc_in",
        "fc_out",
    ]
    leaf_names = {name.split(".")[-1] for name, _ in model.named_modules()}
    discovered = [name for name in preferred_modules if name in leaf_names]
    if discovered:
        return discovered

    fallback = sorted(
        {
            name.split(".")[-1]
            for name, module in model.named_modules()
            if isinstance(module, torch.nn.Linear) and not name.endswith("lm_head")
        }
    )
    if fallback:
        return fallback

    raise ValueError("Could not infer LoRA target modules for the selected model.")


def create_lora_model(config: TrainingConfig):
    from peft import LoraConfig, TaskType, get_peft_model

    model, tokenizer = load_base_model_and_tokenizer(config.model_name)
    model.config.use_cache = False

    if config.gradient_checkpointing:
        model.gradient_checkpointing_enable()
        if hasattr(model, "enable_input_require_grads"):
            model.enable_input_require_grads()

    target_modules = find_lora_target_modules(model)
    lora_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        r=config.lora_r,
        lora_alpha=config.lora_alpha,
        lora_dropout=config.lora_dropout,
        bias="none",
        target_modules=target_modules,
    )
    lora_model = get_peft_model(model, lora_config)
    return lora_model, tokenizer, target_modules
