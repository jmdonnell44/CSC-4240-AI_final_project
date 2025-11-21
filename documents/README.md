### Steps to install dependencies and run the program:

## Python version:

python version 3.11.4 is required to install the dependencies
https://www.python.org/downloads/release/python-311x/
python 3.13 will cause installation failures

### Install dependencies

from project root

```bash
pip install -r documents/requirements.txt
```

### Install the spacy model

```bash
py -3.11 -m pip install "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl"

```


### Run the program.

Process a document and generate study materials:

```bash
py -3.11 main.py ../documents/ml_intro.txt --chat
```

What it does:
Extracts text from the PDF, generates a summary, creates 15 study questions, saves the results to 'your_notes_study_guide.txt'

### How to generate more questions

```bash
py main.py your_notes.pdf -n 25
```

### How to access chat mode

```bash
py main.py your_notes.pdf --chat
```


Additional features of chat mode:
Get additional questions, get summaries, view key concepts, and see statistics

### How to save to a different location

```bash
py main.py my_notes.pdf -o output/study_guide.txt
```

### How to run the program quietly (no output messages)

```bash
py main.py my_notes.pdf -q
```

---

## Interactive Chat Commands

Once in chat mode, you can use these commands:

| Command | Description | Example |
|---------|-------------|---------|
| `help` | Show available commands | `help` |
| `summary` | Get document summary | `summary` |
| `questions [n]` | Generate n more questions | `questions 10` |
| `concepts` | Show key concepts | `concepts` |
| `stats` | Show document statistics | `stats` |
| `exit` / `quit` | Exit chat mode | `exit` |

Alternatively, you can ask them in a more human layout such as:
- "Give me 10 more questions"
- "Summarize the main ideas"
- "What are the key concepts?"

---

### What each file does

1. **text_extractor.py** - PDF/text file processing using pdfplumber
2. **preprocessor.py** - Text cleaning and chunking utilities
3. **concept_extractor.py** - spaCy NER + KeyBERT keyword extraction
4. **summarizer.py** - T5-based abstractive summarization
5. **question_generator.py** - T5-based question generation
6. **chat_interface.py** - Interactive command processing
7. **main.py** - Pipeline orchestration and CLI

---

### Models Used

- **spaCy en_core_web_sm** - Named entity recognition
- **KeyBERT** - Keyword extraction using BERT embeddings
- **T5-small** - Summarization and question generation (Hugging Face)
