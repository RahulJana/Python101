# Copilot Instructions for Python101

## Project Overview
**Python101** is an educational repository containing progressive Python learning materials from basics through advanced topics (ML, DL, RL). The codebase is organized as a learning progression with Jupyter Notebooks as the primary format, supplemented by standalone Python scripts for practical exercises.

## Repository Structure & Architecture

### Core Learning Modules (Numbered Directories)
- **0-getting_started/**: Foundation concepts (shell commands, datatypes, file handling, basics)
- **1-object_oriented_programming/**: OOP principles (classes, inheritance, decorators, class methods/variables)
- **2-digital_image_processing/**: OpenCV/PIL/scikit-image experiments for image manipulation
- **4-deep_learning/**: Neural networks frameworks (TensorFlow, Keras) organized by network types
- **5-reinforcement-learning/**: RL agents and algorithms with documentation in `docs/`
- **Soft Computing Lab/**: University lab assignments (MST, evolutionary algorithms)
- **Timeseries Analysis/**: Time-series forecasting with LSTM and M5 datasets
- **unittesting/**: Pytest tutorials and basic unit testing patterns

### Supporting Directories
- **Miscellaneous/**: Utility concepts (data models, magic methods, weather datasets)
- **Media/**: Assets for DIP experiments (images, videos)

## Development Environment & Workflows

### Python Environment
- **Python Version**: 3.x
- **Primary IDE**: Jupyter Notebook
- **Dependencies** (see requirements.txt): numpy, pandas, matplotlib, scikit-learn, OpenCV
- **Setup Command**: `pip install -r ./requirements.txt`

### Key Patterns in This Repository

#### 1. **Jupyter Notebook Conventions**
- Notebooks use descriptive titles with module number prefix (e.g., `2 - Python Basic Datatypes.ipynb`)
- Multi-part topics use parenthetical suffixes (e.g., `3 - Python Basic Datatypes(part - 2)`)
- Complete/finished notebooks are labeled with `(Complete)` suffix
- Experimental notebooks are prefixed with `Exp_` or `exp` + number

#### 2. **Markdown Documentation in Notebooks**
- Concepts are explained with linked video tutorials (YouTube references embedded)
- Code examples follow pattern: code block → explanation → output block
- Key patterns documented in Notes.md files (see `1-object_oriented_programming/Notes.md`)

#### 3. **Python Script Organization**
- Standalone `.py` files for executable experiments (not notebook-based)
- File naming reflects experiment number (e.g., `dip_exp_3.py`, `exp6.py`)
- Scripts are typically short, focused demonstrations rather than full libraries

#### 4. **Module-Specific Conventions**

**OOP Section**: Heavy use of `self` keyword explanation. Reference `self` as the instance passed implicitly by Python.

**DIP Section**: 
- Multiple image processing libraries compared: PIL, Matplotlib, imageio, OpenCV, scikit-image
- Experiments numbered sequentially with corresponding lab assignments
- Media/ subdirectory contains test images

**Deep Learning**:
- Organized by neuron type then architecture (Primitive → Sigmoid → Feed Forward)
- Separate `0-Frameworks/` directory for framework tutorials
- YOLO section for object detection

## Critical Developer Tasks

### Running Notebooks
- Use VS Code Jupyter extension or open in Jupyter Lab
- All notebooks are self-contained; dependencies in requirements.txt
- RL section requires specific dependencies in `5-reinforcement-learning/requirements.txt`

### Testing & Validation
- `unittesting/` has pytest examples
- Run with: `pytest unittesting/pytest-tutorials/`
- Simple test structure; focus on learning pytest patterns

### Adding New Content
- Place in appropriate numbered directory or create new one
- Use consistent naming: `[Module-Number] - [Concept Name].ipynb`
- Include inline markdown explanation cells with code examples
- Add Notes.md for complex concept explanations

## Important Integration Points

1. **Cross-Module References**: OOP concepts (classes, decorators) are prerequisite for DL/RL modules
2. **Data Dependencies**: DIP experiments reference Media/ directory for test images
3. **External Libraries**: OpenCV, scikit-image, TensorFlow are heavy dependencies; check environment

## Git Workflow
- Repository uses standard git branching (observed: `section/rl` branch for RL work)
- No special commit conventions; follow descriptive messages for educational clarity

---

**Last Updated**: 2026-02-04
