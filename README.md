# StudyBuddy



## Overview
StudyBuddy automatically processes lecture notes to create study materials including summaries, key concepts, and study questions. It uses natural language processing tools like spaCy, KeyBERT, and Hugging Face Transformers.

## Requirements
- Python 3.8 or higher
- pip package manager

## Installation

1. **Navigate to the project directory**
   ```bash
   cd studybuddy
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Download the spaCy model**
   ```bash
   python -m spacy download en_core_web_sm
   ```

---

## How to Run

### Basic Usage
Process a PDF or text file to generate a study guide:
```bash
python main.py your_notes.pdf
```

### Options
| Option | Description |
|--------|-------------|
| `-n [num]` | Number of questions to generate (default: 15) |
| `-o [path]` | Custom output file path |
| `--chat` | Start interactive chat mode |
| `-q` | Quiet mode (suppress output) |

Example:
```bash
python main.py lecture_notes.pdf -n 20 --chat
```

## Output
A file will be created in the same directory (e.g., `studyguide.txt`) containing:
- Summary
- Study Questions
- Key Concepts

---

## Troubleshooting
- **ModuleNotFoundError** → Run `pip install -r requirements.txt`
- **spaCy model not found** → Run `python -m spacy download en_core_web_sm`
- **PDF not readable** → Make sure it’s not scanned or encrypted

