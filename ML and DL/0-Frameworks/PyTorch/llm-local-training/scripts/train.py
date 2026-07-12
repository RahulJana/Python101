from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from transformers import DataCollatorForSeq2Seq, Trainer, TrainingArguments, set_seed

from common import build_tokenize_function, create_lora_model, load_config, load_instruction_datasets


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fine-tune a small causal LM with LoRA.")
    parser.add_argument("--config", required=True, help="Path to a JSON config file.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)

    if config.save_steps != config.eval_steps:
        raise ValueError("save_steps and eval_steps should match when load_best_model_at_end is enabled.")

    set_seed(config.seed)
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_datasets = load_instruction_datasets(config)
    model, tokenizer, target_modules = create_lora_model(config)
    tokenize_batch = build_tokenize_function(tokenizer, config.max_seq_length)

    tokenized_datasets = raw_datasets.map(
        tokenize_batch,
        batched=True,
        remove_columns=raw_datasets["train"].column_names,
        desc="Tokenizing instruction dataset",
    )

    pad_multiple = 8 if torch.cuda.is_available() else None
    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        model=model,
        padding=True,
        pad_to_multiple_of=pad_multiple,
    )

    training_args = TrainingArguments(
        output_dir=str(output_dir),
        num_train_epochs=config.num_train_epochs,
        per_device_train_batch_size=config.per_device_train_batch_size,
        per_device_eval_batch_size=config.per_device_eval_batch_size,
        gradient_accumulation_steps=config.gradient_accumulation_steps,
        learning_rate=config.learning_rate,
        weight_decay=config.weight_decay,
        warmup_ratio=config.warmup_ratio,
        logging_steps=config.logging_steps,
        logging_first_step=True,
        evaluation_strategy="steps",
        save_strategy="steps",
        eval_steps=config.eval_steps,
        save_steps=config.save_steps,
        save_total_limit=2,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        fp16=torch.cuda.is_available(),
        bf16=False,
        gradient_checkpointing=config.gradient_checkpointing,
        dataloader_num_workers=0,
        remove_unused_columns=False,
        report_to="none",
        optim="adamw_torch",
        seed=config.seed,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        data_collator=data_collator,
        tokenizer=tokenizer,
    )

    model.print_trainable_parameters()

    train_result = trainer.train()
    eval_metrics = trainer.evaluate()

    final_checkpoint = output_dir / "final_checkpoint"
    trainer.save_model(str(final_checkpoint))
    tokenizer.save_pretrained(final_checkpoint)

    summary = {
        "device": "cuda" if torch.cuda.is_available() else "cpu",
        "config": config.to_dict(),
        "target_modules": target_modules,
        "train_metrics": train_result.metrics,
        "eval_metrics": eval_metrics,
        "best_model_checkpoint": trainer.state.best_model_checkpoint,
        "final_checkpoint": str(final_checkpoint),
    }
    with open(output_dir / "training_summary.json", "w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
