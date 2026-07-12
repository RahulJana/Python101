# Local Small LLM Training Pipeline

This module adds a learning-focused local LLM fine-tuning pipeline inside the existing PyTorch section of the repository.

## Why this pipeline fits this PC

Your machine has:

- AMD Ryzen 9 5900HX
- 16 GB system RAM
- NVIDIA GeForce RTX 3060 Laptop GPU with 6 GB VRAM

That is enough for learning-oriented fine-tuning of a very small causal language model, but not enough for full LLM pretraining from scratch. Because of that, this pipeline uses LoRA fine-tuning on a small open model and keeps the defaults conservative.

## Recommended starting point

Start with the `SmolLM2-135M` config:

- small enough to run comfortably on 6 GB VRAM
- simple enough to learn the full workflow
- fast enough for short experiments on a laptop GPU

After that, you can try the included `SmolLM2-360M` stretch config with the smaller batch size.

## Folder layout

```text
llm-local-training/
|-- configs/
|   |-- smollm2_135m_rtx3060_6gb.json
|   `-- smollm2_360m_rtx3060_6gb.json
|-- sample_data/
|   `-- python101_instructions.jsonl
|-- scripts/
|   |-- chat.py
|   |-- common.py
|   |-- evaluate.py
|   `-- train.py
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## What this trains

This pipeline performs supervised fine-tuning on instruction and answer pairs in JSONL format:

```json
{"instruction": "Explain Python lists.", "input": "", "output": "A list is ..."}
```

The training loss is only applied to the response tokens, which makes it a good learning example for instruction tuning.

## Setup

1. Create and activate an environment.
2. Install a CUDA-enabled PyTorch build that matches your system.
3. Install the local requirements from this folder.

Example:

```powershell
cd "C:\Users\irahu\git_workspace\Python101\ML and DL\0-Frameworks\PyTorch\llm-local-training"
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install torch torchvision torchaudio
pip install -r requirements.txt
```

If `torch.cuda.is_available()` returns `False`, install the correct GPU build of PyTorch before training.

## Train

Start with the safest config for your laptop:

```powershell
python .\scripts\train.py --config .\configs\smollm2_135m_rtx3060_6gb.json
```

Stretch run:

```powershell
python .\scripts\train.py --config .\configs\smollm2_360m_rtx3060_6gb.json
```

## Evaluate

```powershell
python .\scripts\evaluate.py `
  --config .\configs\smollm2_135m_rtx3060_6gb.json `
  --checkpoint-dir .\outputs\smollm2_135m_python101\final_checkpoint
```

## Chat with the fine-tuned adapter

```powershell
python .\scripts\chat.py `
  --config .\configs\smollm2_135m_rtx3060_6gb.json `
  --checkpoint-dir .\outputs\smollm2_135m_python101\final_checkpoint `
  --instruction "Explain Python decorators in simple words."
```

## How to add your own dataset

Replace or extend `sample_data/python101_instructions.jsonl` with your own JSONL file using these keys:

- `instruction`
- `input`
- `output`

Then update the `train_file` value in the config file.

## Practical limits for this machine

- Best learning path: `SmolLM2-135M`
- Reasonable stretch target: `SmolLM2-360M`
- Not recommended on this machine for first attempts: 1B+ model fine-tuning, full-model training, or pretraining from scratch

## Learning note

If your goal later is to understand architecture internals rather than adapter fine-tuning, the next step should be a tiny Transformer trained from scratch on a toy corpus. For this machine, that is better treated as a separate educational project from LLM fine-tuning.
