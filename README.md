# StudyBuddy

## Overview
StudyBuddy automatically processes lecture notes to create study materials including summaries, key concepts, and study questions. It uses natural language processing tools such as spaCy, KeyBERT, and Hugging Face Transformers.


## Installation

1. Navigate to the project directory:
   ```bash
   cd studybuddy
   ```

2. Install all dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## How to Run
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


## Chat Mode
When running with `--chat`, you can use these commands:
| Command | Description |
|----------|--------------|
| `help` | Show available commands |
| `summary` | Display document summary |
| `questions [n]` | Generate n more questions |
| `concepts` | Show key concepts |
| `stats` | Show document statistics |
| `exit` | Exit chat mode |

You can also type natural requests such as:
- “Give me 10 more questions”
- “Summarize the main ideas”
- “What are the key concepts?”

## Testing
Test that all components work properly:
```bash
python test_components.py
```

You can also test individual modules:
```bash
python text_extractor.py
python preprocessor.py
python concept_extractor.py
python summarizer.py
python question_generator.py
```

## File Structure
```
studybuddy/
├── main.py                # Main pipeline and CLI
├── text_extractor.py      # PDF/text extraction
├── preprocessor.py        # Text cleaning and chunking
├── concept_extractor.py   # Key concept extraction
├── summarizer.py          # Summarization
├── question_generator.py  # Question generation
├── chat_interface.py      # Interactive chat
├── requirements.txt       # Dependencies
└── test_components.py     # Component testing
```

## Troubleshooting
- ModuleNotFoundError → Run `pip install -r requirements.txt`
- spaCy model not found → Run `python -m spacy download en_core_web_sm`
- PDF extraction failed → Check if the file is encrypted or image-based
- Slow first run → Model downloads are required on first use (~500MB)
- Out of memory → Reduce chunk size in `preprocessor.py` or use smaller files
