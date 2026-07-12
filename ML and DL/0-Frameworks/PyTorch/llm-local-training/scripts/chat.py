from __future__ import annotations

import argparse
from pathlib import Path

import torch
from peft import PeftModel

from common import build_prompt, load_base_model_and_tokenizer, load_config


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chat with a LoRA fine-tuned small LM.")
    parser.add_argument("--config", required=True, help="Path to a JSON config file.")
    parser.add_argument("--checkpoint-dir", required=True, help="Directory containing the saved adapter.")
    parser.add_argument("--instruction", required=True, help="Instruction to send to the model.")
    parser.add_argument("--input-text", default="", help="Optional extra context for the instruction.")
    parser.add_argument("--max-new-tokens", type=int, default=None, help="Override the generation length.")
    parser.add_argument("--temperature", type=float, default=0.8, help="Sampling temperature.")
    parser.add_argument("--top-p", type=float, default=0.95, help="Top-p sampling value.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config)
    checkpoint_dir = Path(args.checkpoint_dir).resolve()

    model, tokenizer = load_base_model_and_tokenizer(config.model_name)
    model = PeftModel.from_pretrained(model, str(checkpoint_dir))

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()

    prompt = build_prompt(args.instruction, args.input_text)
    encoded = tokenizer(prompt, return_tensors="pt")
    encoded = {key: value.to(device) for key, value in encoded.items()}

    with torch.inference_mode():
        generated = model.generate(
            **encoded,
            max_new_tokens=args.max_new_tokens or config.max_new_tokens,
            do_sample=True,
            temperature=args.temperature,
            top_p=args.top_p,
            pad_token_id=tokenizer.eos_token_id,
        )

    prompt_length = encoded["input_ids"].shape[1]
    response_tokens = generated[0][prompt_length:]
    response = tokenizer.decode(response_tokens, skip_special_tokens=True).strip()
    print(response)


if __name__ == "__main__":
    main()
