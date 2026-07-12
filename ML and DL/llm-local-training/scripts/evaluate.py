from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import torch

from common import (
    build_dependency_help,
    build_tokenize_function,
    load_base_model_and_tokenizer,
    load_config,
    load_instruction_datasets,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate a fine-tuned LoRA adapter.")
    parser.add_argument("--config", required=True, help="Path to a JSON config file.")
    parser.add_argument("--checkpoint-dir", required=True, help="Directory containing the saved adapter.")
    return parser.parse_args()


def main() -> None:
    try:
        from peft import PeftModel
        from transformers import DataCollatorForSeq2Seq, Trainer, TrainingArguments
    except Exception as exc:
        raise RuntimeError(build_dependency_help(exc)) from exc

    args = parse_args()
    config = load_config(args.config)
    checkpoint_dir = Path(args.checkpoint_dir).resolve()

    base_model, tokenizer = load_base_model_and_tokenizer(config.model_name)
    model = PeftModel.from_pretrained(base_model, str(checkpoint_dir))

    raw_datasets = load_instruction_datasets(config)
    tokenize_batch = build_tokenize_function(tokenizer, config.max_seq_length)
    tokenized_datasets = raw_datasets.map(
        tokenize_batch,
        batched=True,
        remove_columns=raw_datasets["train"].column_names,
        desc="Tokenizing validation dataset",
    )

    pad_multiple = 8 if torch.cuda.is_available() else None
    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        model=model,
        padding=True,
        pad_to_multiple_of=pad_multiple,
    )

    evaluation_args = TrainingArguments(
        output_dir=str(checkpoint_dir / "_eval"),
        per_device_eval_batch_size=config.per_device_eval_batch_size,
        dataloader_num_workers=0,
        fp16=torch.cuda.is_available(),
        report_to="none",
    )

    trainer = Trainer(
        model=model,
        args=evaluation_args,
        eval_dataset=tokenized_datasets["validation"],
        data_collator=data_collator,
        tokenizer=tokenizer,
    )

    metrics = trainer.evaluate()
    metrics["perplexity"] = math.exp(min(metrics["eval_loss"], 20.0))
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
