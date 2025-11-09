#!/usr/bin/env python3
"""
Test script to verify all StudyBuddy components are working correctly.
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        from text_extractor import TextExtractor
        print("  ✓ text_extractor")
    except ImportError as e:
        print(f"  ✗ text_extractor: {e}")
        return False
    
    try:
        from preprocessor import Preprocessor
        print("  ✓ preprocessor")
    except ImportError as e:
        print(f"  ✗ preprocessor: {e}")
        return False
    
    try:
        from concept_extractor import ConceptExtractor
        print("  ✓ concept_extractor")
    except ImportError as e:
        print(f"  ✗ concept_extractor: {e}")
        return False
    
    try:
        from summarizer import Summarizer
        print("  ✓ summarizer")
    except ImportError as e:
        print(f"  ✗ summarizer: {e}")
        return False
    
    try:
        from question_generator import QuestionGenerator
        print("  ✓ question_generator")
    except ImportError as e:
        print(f"  ✗ question_generator: {e}")
        return False
    
    try:
        from chat_interface import ChatInterface
        print("  ✓ chat_interface")
    except ImportError as e:
        print(f"  ✗ chat_interface: {e}")
        return False
    
    return True

def test_dependencies():
    """Test if all required dependencies are installed."""
    print("\nTesting dependencies...")
    
    dependencies = [
        'pdfplumber',
        'spacy',
        'keybert',
        'transformers',
        'torch',
    ]
    
    all_good = True
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"  ✓ {dep}")
        except ImportError:
            print(f"  ✗ {dep} - NOT INSTALLED")
            all_good = False
    
    return all_good

def test_spacy_model():
    """Test if spaCy model is available."""
    print("\nTesting spaCy model...")
    
    try:
        import spacy
        nlp = spacy.load("en_core_web_sm")
        print("  ✓ en_core_web_sm model loaded")
        return True
    except OSError:
        print("  ✗ en_core_web_sm model not found")
        print("  Run: python -m spacy download en_core_web_sm")
        return False
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def quick_functional_test():
    """Run a quick functional test of the pipeline."""
    print("\nRunning functional test...")
    
    try:
        from preprocessor import Preprocessor
        from concept_extractor import ConceptExtractor
        
        sample_text = """
        Machine learning is a subset of artificial intelligence. Neural networks
        are used for deep learning. Supervised learning requires labeled data.
        """
        
        # Test preprocessor
        preprocessor = Preprocessor(chunk_size=50, overlap=10)
        result = preprocessor.preprocess(sample_text)
        print(f"  ✓ Preprocessor: {result['metadata']['total_words']} words processed")
        
        # Test concept extractor (if models loaded)
        print("  ⏳ Loading concept extraction models (may take a moment)...")
        extractor = ConceptExtractor()
        concepts = extractor.get_important_concepts(sample_text, top_n=3)
        print(f"  ✓ Concept Extractor: Found {len(concepts)} concepts")
        
        return True
    
    except Exception as e:
        print(f"  ✗ Functional test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("="*60)
    print("  StudyBuddy Component Test")
    print("="*60 + "\n")
    
    # Test imports
    imports_ok = test_imports()
    
    # Test dependencies
    deps_ok = test_dependencies()
    
    # Test spaCy model
    spacy_ok = test_spacy_model()
    
    # Run functional test if everything else passed
    if imports_ok and deps_ok and spacy_ok:
        functional_ok = quick_functional_test()
    else:
        functional_ok = False
        print("\n⚠️  Skipping functional test due to missing dependencies")
    
    # Summary
    print("\n" + "="*60)
    print("  TEST SUMMARY")
    print("="*60)
    print(f"  Imports:      {'✓ PASS' if imports_ok else '✗ FAIL'}")
    print(f"  Dependencies: {'✓ PASS' if deps_ok else '✗ FAIL'}")
    print(f"  spaCy Model:  {'✓ PASS' if spacy_ok else '✗ FAIL'}")
    print(f"  Functional:   {'✓ PASS' if functional_ok else '✗ FAIL'}")
    print("="*60 + "\n")
    
    if all([imports_ok, deps_ok, spacy_ok, functional_ok]):
        print("✓ All tests passed! StudyBuddy is ready to use.")
        print("\nTry running:")
        print("  python main.py /mnt/user-data/uploads/final_project_CSC4240_5240.pdf")
        return 0
    else:
        print("✗ Some tests failed. Please install missing dependencies.")
        print("\nInstallation steps:")
        print("  1. pip install -r requirements.txt")
        print("  2. python -m spacy download en_core_web_sm")
        return 1

if __name__ == "__main__":
    sys.exit(main())
