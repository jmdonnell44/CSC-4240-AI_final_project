# StudyBuddy Quick Reference Card

## 🚀 Installation (One Time)
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## ⚡ Common Commands

### Basic Usage
```bash
# Process a document
python main.py notes.pdf

# Process with custom question count
python main.py notes.pdf -n 20

# Interactive chat mode
python main.py notes.pdf --chat

# Quiet mode (no progress messages)
python main.py notes.pdf -q

# Custom output file
python main.py notes.pdf -o my_study_guide.txt

# Don't save file (just display)
python main.py notes.pdf --no-save
```

## 💬 Chat Commands (when in --chat mode)

| Command | What It Does |
|---------|-------------|
| `help` | Show available commands |
| `summary` | Display document summary |
| `questions [n]` | Generate n more questions |
| `concepts` | Show key concepts |
| `stats` | Show document statistics |
| `exit` | Exit chat mode |

Natural language also works:
- "Give me 10 more questions"
- "Summarize the main ideas"
- "What are the key concepts?"

## 🧪 Testing

```bash
# Test all components
python test_components.py

# Run usage examples
python examples.py

# Test individual modules
python text_extractor.py
python preprocessor.py
python concept_extractor.py
```

## 📊 Quick Demo for Presentation

```bash
# 1. Show basic processing (with your sample PDF)
python main.py sample_lecture.pdf

# 2. Show interactive mode
python main.py sample_lecture.pdf --chat

# In chat, type:
questions 5
concepts
exit
```

## 🔧 Quick Customization

### Change default question count (in main.py)
```python
default=15  →  default=20
```

### Use better model (slower, higher quality)
```python
# In summarizer.py and question_generator.py
model_name="t5-small"  →  model_name="t5-base"
```

### Adjust chunk size (in preprocessor.py)
```python
chunk_size=512  →  chunk_size=256
```

## 📁 File Structure
```
studybuddy/
├── main.py              # Start here
├── text_extractor.py    # PDF extraction
├── preprocessor.py      # Text cleaning
├── concept_extractor.py # Key concepts
├── summarizer.py        # Summaries
├── question_generator.py # Questions
├── chat_interface.py    # Chat mode
├── requirements.txt     # Dependencies
└── README.md           # Full docs
```

## 🆘 Quick Fixes

**Module not found?**
```bash
pip install -r requirements.txt
```

**spaCy model not found?**
```bash
python -m spacy download en_core_web_sm
```

**Out of memory?**
- Process smaller files
- Close other apps
- Use t5-small (not t5-base)

**Slow first run?**
- Normal! Downloading models (~500MB)
- Subsequent runs are fast

## 📝 For User Study

Ask participants to rate questions 1-5:
1. **Clarity**: Is the question clear?
2. **Relevance**: Is it relevant to content?
3. **Usefulness**: Would it help you study?

Sample size: 10 participants, 10 questions each = 100 ratings

## 🎯 Expected Results

- **Processing**: ~8-10 sec per 10 pages
- **Questions**: ~1 question per 50 words
- **Quality**: User ratings 4.0-4.2 / 5.0
- **Summary**: ROUGE-L ~0.40-0.45

## 💡 Pro Tips

1. **Test with known content** first
2. **Use chat mode** to impress in demos
3. **Generate extra questions** if some are weak
4. **Save outputs** for evaluation data
5. **Practice demo** beforehand

## 📞 Emergency Troubleshooting

If something breaks during demo:
1. Have screenshots ready as backup
2. Use pre-generated output file
3. Show the code instead
4. Explain what it would do

## ⏱️ Time Estimates

- **Setup**: 10-15 min
- **Test run**: 2 min
- **User study**: 30-60 min
- **Demo practice**: 15 min

## ✅ Pre-Presentation Checklist

- [ ] Tested on your machine
- [ ] Sample PDF ready
- [ ] Demo practiced
- [ ] Screenshots as backup
- [ ] Results documented
- [ ] Team contributions decided

---

**Keep this card handy during development and presentation!**
