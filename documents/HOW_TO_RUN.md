# How to Run StudyBuddy

## ✅ Prerequisites

- **Python 3.11** (recommended) or Python 3.10
- **Windows 10/11** (these instructions are for Windows with CMD)
- **Internet connection** (for first-time model downloads)

---

## 📥 Installation Steps

### Step 1: Install Python 3.11

1. Download Python 3.11 from: https://www.python.org/downloads/release/python-31111/
2. Run the installer
3. **✅ IMPORTANT**: Check "Add Python 3.11 to PATH" during installation
4. Complete the installation
5. Restart Command Prompt

### Step 2: Verify Python Installation

Open Command Prompt (CMD) and type:

```cmd
py -3.11 --version
```

You should see: `Python 3.11.x`

---

## 🔧 Setup StudyBuddy

### Step 3: Navigate to Project Folder

```cmd
cd "C:\Users\YourUsername\Documents\CSC-4240 Artificial Intelligence\final project"
```

Replace `YourUsername` with your actual Windows username.

### Step 4: Install Dependencies

Run these commands **one by one**:

```cmd
py -3.11 -m pip install --upgrade pip

py -3.11 -m pip install pdfplumber spacy keybert transformers torch sentence-transformers nltk rouge-score tqdm scikit-learn

py -3.11 -m pip install sentencepiece

py -3.11 -m pip install protobuf
```

**Note**: This will download about 500MB-1GB of libraries. Takes 5-10 minutes depending on your internet speed.

### Step 5: Download spaCy Language Model

```cmd
py -3.11 -m spacy download en_core_web_sm
```

This downloads the English language model for natural language processing (~12MB).

---

## 🚀 Running StudyBuddy

### Basic Usage

Process a PDF and generate study materials:

```cmd
py -3.11 main.py your_document.pdf
```

Replace `your_document.pdf` with the path to your PDF file.

### Example with Full Path

```cmd
py -3.11 main.py "C:\Users\johnd\Documents\lecture_notes.pdf"
```

### Interactive Chat Mode (Recommended for Demos)

```cmd
py -3.11 main.py your_document.pdf --chat
```

This opens an interactive interface where you can:
- Type `help` to see available commands
- Type `questions 10` to generate 10 more questions
- Type `summary` to see the summary
- Type `concepts` to view key concepts
- Type `stats` to see document statistics
- Type `exit` to quit

---

## 📋 Command-Line Options

### Generate More Questions

```cmd
py -3.11 main.py my_notes.pdf -n 25
```

Generates 25 questions instead of the default 15.

### Custom Output File

```cmd
py -3.11 main.py my_notes.pdf -o my_study_guide.txt
```

Saves the output to a specific file name.

### Quiet Mode (No Progress Messages)

```cmd
py -3.11 main.py my_notes.pdf -q
```

Suppresses progress messages - useful for batch processing.

### Don't Save Output File

```cmd
py -3.11 main.py my_notes.pdf --no-save
```

Only displays results without saving to a file.

### Combine Options

```cmd
py -3.11 main.py lecture.pdf -n 20 -o final_study_guide.txt --chat
```

---

## 💡 Common Commands Reference

| Command | What It Does |
|---------|-------------|
| `py -3.11 main.py file.pdf` | Basic processing |
| `py -3.11 main.py file.pdf --chat` | Interactive mode |
| `py -3.11 main.py file.pdf -n 20` | Generate 20 questions |
| `py -3.11 main.py file.pdf -q` | Quiet mode |
| `py -3.11 main.py file.pdf -o output.txt` | Custom output file |
| `py -3.11 main.py --help` | Show all options |

---

## 🎯 What Happens When You Run It

### First Run (Slow - 3-5 minutes)

1. **Initialization**: Loads spaCy and KeyBERT models (~10 seconds)
2. **Model Download**: Downloads T5 AI models (~500MB, 2-3 minutes)
3. **Processing**: Processes your document (~30 seconds)
4. **Output**: Displays and saves results

**Total first run**: 3-5 minutes

### Subsequent Runs (Fast - 10-30 seconds)

1. **Initialization**: Loads cached models (~5 seconds)
2. **Processing**: Processes your document (~5-15 seconds)
3. **Output**: Displays and saves results

**Total**: 10-30 seconds per document

---

## 📊 Expected Output

When you run StudyBuddy, you'll see:

```
============================================================
  Initializing StudyBuddy Components...
============================================================

Loading spaCy model...
✓ spaCy model loaded
Loading KeyBERT model...
✓ KeyBERT model loaded
Loading t5-small model for summarization...
✓ t5-small model loaded
Loading t5-small for question generation...
✓ Question generation model loaded

✓ All components initialized successfully!

============================================================
  Processing: your_document.pdf
============================================================

Step 1/5: Extracting text from document...
Processing PDF with 10 pages...
✓ Successfully extracted 15000 characters from PDF

Step 2/5: Preprocessing and chunking text...
✓ Created 5 chunks

Step 3/5: Extracting key concepts...
✓ Found 45 named entities
✓ Extracted 20 keywords
✓ Found 63 noun phrases

Step 4/5: Generating summary...
✓ Generated summary (150 words)

Step 5/5: Generating 15 study questions...
✓ Generated 15 questions

============================================================
  ✓ Processing Complete!
============================================================

[Summary, Questions, and Concepts are displayed here]

✓ Results saved to: your_document_study_guide.txt
```

---

## 📁 Output Files

StudyBuddy creates a text file with this format:

**Filename**: `your_document_study_guide.txt` (automatically generated)

**Contents**:
```
==============================================================
  STUDYBUDDY STUDY GUIDE
==============================================================

Document: your_document.pdf
Generated: 2025-11-18 15:30:00

SUMMARY
--------------------------------------------------------------
[AI-generated summary of your document]

STUDY QUESTIONS
--------------------------------------------------------------
1. What is machine learning?
2. How do neural networks work?
3. What are the applications of AI?
...

KEY CONCEPTS
--------------------------------------------------------------
1. artificial intelligence
2. machine learning
3. neural networks
...
```

---

## 🆘 Troubleshooting

### "py is not recognized..."

**Problem**: Python not installed or not in PATH

**Solution**: 
1. Install Python 3.11 from python.org
2. During installation, CHECK "Add Python to PATH"
3. Restart Command Prompt

### "Module not found" errors

**Problem**: Dependencies not installed

**Solution**:
```cmd
py -3.11 -m pip install pdfplumber spacy keybert transformers torch sentence-transformers nltk rouge-score tqdm scikit-learn sentencepiece protobuf
```

### "spaCy model not found"

**Problem**: Language model not downloaded

**Solution**:
```cmd
py -3.11 -m spacy download en_core_web_sm
```

### "File not found" error

**Problem**: PDF path is wrong

**Solution**: Use the full path in quotes:
```cmd
py -3.11 main.py "C:\Users\johnd\Documents\my notes.pdf"
```

### "Out of memory" error

**Problem**: Document too large or insufficient RAM

**Solution**:
- Close other applications
- Try a smaller document first
- Process documents under 50 pages

### Program runs but no output file

**Problem**: You used `--no-save` flag

**Solution**: Run without the `--no-save` flag:
```cmd
py -3.11 main.py your_file.pdf
```

---

## 🧪 Testing the Installation

Run the test script to verify everything works:

```cmd
py -3.11 test_components.py
```

You should see:
```
✓ All tests passed! StudyBuddy is ready to use.
```

---

## 💻 Example Usage Session

Here's a complete example of running StudyBuddy:

```cmd
C:\Users\johnd> cd "Documents\CSC-4240 Artificial Intelligence\final project"

C:\Users\johnd\Documents\CSC-4240 Artificial Intelligence\final project> py -3.11 main.py lecture_notes.pdf --chat

[... processing happens ...]

============================================================
  STUDYBUDDY RESULTS
============================================================

📋 SUMMARY
--------------------------------------------------------------
This document covers machine learning fundamentals including 
supervised learning, neural networks, and deep learning...

❓ STUDY QUESTIONS
--------------------------------------------------------------
1. What is supervised learning?
2. How do neural networks process information?
3. What are the main types of machine learning algorithms?
[... more questions ...]

🔑 KEY CONCEPTS
--------------------------------------------------------------
1. machine learning
2. neural networks
3. supervised learning
[... more concepts ...]

============================================================
   Welcome to StudyBuddy - Your AI Study Partner!
============================================================

I've processed your document and generated study materials.
Type 'help' to see available commands, or 'exit' to quit.

You: questions 5
StudyBuddy: Generating 5 study questions...
[5 new questions appear]

You: concepts
StudyBuddy: Here are the key concepts I identified:
[concepts list appears]

You: exit
StudyBuddy: Thanks for studying with me! Good luck! 📚
```

---

## 🎓 Tips for Best Results

### For Better Summaries
- Use documents with clear, well-structured text
- 5-50 page documents work best
- Avoid heavily formatted or scanned PDFs

### For Better Questions
- Longer documents generate more questions
- Technical content works well
- Educational materials produce the best results

### For Demos/Presentations
- Use `--chat` mode for interactive demonstrations
- Prepare a sample 5-10 page PDF beforehand
- Practice the chat commands: `questions`, `summary`, `concepts`

---

## 📝 Quick Reference Card

**Installation (one-time):**
```cmd
py -3.11 -m pip install pdfplumber spacy keybert transformers torch sentence-transformers nltk rouge-score tqdm scikit-learn sentencepiece protobuf
py -3.11 -m spacy download en_core_web_sm
```

**Basic usage:**
```cmd
py -3.11 main.py document.pdf
```

**Demo mode:**
```cmd
py -3.11 main.py document.pdf --chat
```

**All options:**
```cmd
py -3.11 main.py --help
```

---

## 🎉 You're Ready!

StudyBuddy is now installed and ready to use. Start by processing a sample PDF:

```cmd
py -3.11 main.py your_notes.pdf --chat
```

Happy studying! 📚✨

---

## 📞 Need Help?

- Check the **README.md** for detailed documentation
- Run `py -3.11 test_components.py` to verify installation
- Run `py -3.11 main.py --help` to see all options
- Review the **Troubleshooting** section above

---

**Version**: 1.0  
**Last Updated**: November 2025  
**Python Version**: 3.11 (recommended)
