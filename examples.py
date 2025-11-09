#!/usr/bin/env python3
"""
Example: Using StudyBuddy Programmatically

This script shows how to use StudyBuddy components in your own code.
"""

from text_extractor import TextExtractor
from preprocessor import Preprocessor
from concept_extractor import ConceptExtractor
from summarizer import Summarizer
from question_generator import QuestionGenerator


def example_1_basic_usage():
    """Example 1: Basic usage with a simple text."""
    print("="*60)
    print("  Example 1: Basic Usage")
    print("="*60 + "\n")
    
    sample_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, 
    in contrast to natural intelligence displayed by animals including humans. 
    AI research has been defined as the field of study of intelligent agents, 
    which refers to any system that perceives its environment and takes actions 
    that maximize its chance of achieving its goals.
    
    Machine learning is a subset of AI that provides systems the ability to 
    automatically learn and improve from experience without being explicitly 
    programmed. Deep learning is a subset of machine learning based on 
    artificial neural networks.
    """
    
    # Initialize components
    preprocessor = Preprocessor()
    summarizer = Summarizer(model_name="t5-small")
    question_gen = QuestionGenerator(model_name="t5-small")
    
    # Process
    print("1. Preprocessing text...")
    processed = preprocessor.preprocess(sample_text)
    print(f"   Words: {processed['metadata']['total_words']}")
    
    print("\n2. Generating summary...")
    summary = summarizer.summarize(processed['cleaned_text'], max_length=50)
    print(f"   Summary: {summary}")
    
    print("\n3. Generating questions...")
    questions = question_gen.generate_simple_questions(processed['cleaned_text'], num_questions=3)
    for i, q in enumerate(questions, 1):
        print(f"   {i}. {q}")
    
    print()


def example_2_pdf_processing():
    """Example 2: Processing a PDF file."""
    print("="*60)
    print("  Example 2: PDF Processing")
    print("="*60 + "\n")
    
    # Initialize extractor
    extractor = TextExtractor()
    
    # Check if test PDF exists
    test_pdf = "/mnt/user-data/uploads/final_project_CSC4240_5240.pdf"
    
    import os
    if os.path.exists(test_pdf):
        print(f"Processing: {test_pdf}")
        
        # Get file info
        info = extractor.get_file_info(test_pdf)
        print(f"File size: {info['size_mb']} MB")
        print(f"Pages: {info.get('pages', 'N/A')}")
        
        # Extract text
        print("\nExtracting text...")
        text = extractor.extract_from_file(test_pdf)
        
        if text:
            print(f"Extracted {len(text)} characters")
            print(f"\nFirst 200 characters:")
            print(text[:200] + "...")
    else:
        print(f"Test PDF not found: {test_pdf}")
        print("Place a PDF file at the above location to test.")
    
    print()


def example_3_concept_extraction():
    """Example 3: Advanced concept extraction."""
    print("="*60)
    print("  Example 3: Concept Extraction")
    print("="*60 + "\n")
    
    sample_text = """
    The transformer architecture was introduced by Google researchers in 2017.
    It revolutionized natural language processing by using self-attention mechanisms.
    Popular transformer models include BERT, GPT, and T5. Companies like OpenAI,
    Google, and Meta have invested heavily in developing large language models.
    These models can perform tasks like translation, summarization, and question answering.
    """
    
    print("Initializing concept extractor...")
    extractor = ConceptExtractor()
    
    print("\nExtracting concepts...")
    concepts = extractor.extract_all_concepts(sample_text, top_keywords=10)
    
    print("\n--- Named Entities ---")
    for ent in concepts['named_entities'][:5]:
        print(f"  • {ent['text']} ({ent['label']})")
    
    print("\n--- Keywords ---")
    for kw, score in concepts['keywords'][:5]:
        print(f"  • {kw} (score: {score:.3f})")
    
    print(f"\n--- Total Unique Concepts: {concepts['total_unique_concepts']} ---")
    print()


def example_4_custom_pipeline():
    """Example 4: Building a custom pipeline."""
    print("="*60)
    print("  Example 4: Custom Pipeline")
    print("="*60 + "\n")
    
    # Sample lecture notes
    lecture_text = """
    Today's lecture covers supervised learning in machine learning.
    Supervised learning requires labeled training data where each example
    has an input and a corresponding output label. Common algorithms include
    linear regression, logistic regression, decision trees, and neural networks.
    
    The training process involves minimizing a loss function that measures
    the difference between predicted and actual outputs. Cross-validation
    is used to prevent overfitting and evaluate model performance.
    """
    
    print("Building custom pipeline...")
    
    # Step 1: Preprocess
    preprocessor = Preprocessor(chunk_size=100, overlap=20)
    processed = preprocessor.preprocess(lecture_text)
    print(f"✓ Preprocessed: {processed['metadata']['total_words']} words")
    
    # Step 2: Extract concepts
    concept_extractor = ConceptExtractor()
    important_concepts = concept_extractor.get_important_concepts(
        processed['cleaned_text'], 
        top_n=5
    )
    print(f"✓ Extracted {len(important_concepts)} key concepts")
    
    # Step 3: Generate summary
    summarizer = Summarizer(model_name="t5-small")
    summary = summarizer.summarize(processed['cleaned_text'], max_length=60)
    print(f"✓ Generated summary")
    
    # Step 4: Generate questions
    question_gen = QuestionGenerator(model_name="t5-small")
    questions = question_gen.generate_questions_from_concepts(
        processed['cleaned_text'],
        important_concepts,
        max_questions=5
    )
    print(f"✓ Generated {len(questions)} questions")
    
    # Display results
    print("\n--- Summary ---")
    print(summary)
    
    print("\n--- Key Concepts ---")
    for concept in important_concepts:
        print(f"  • {concept}")
    
    print("\n--- Study Questions ---")
    for i, q in enumerate(questions, 1):
        print(f"  {i}. {q}")
    
    print()


def example_5_batch_processing():
    """Example 5: Batch processing multiple chunks."""
    print("="*60)
    print("  Example 5: Batch Processing")
    print("="*60 + "\n")
    
    # Multiple text chunks (simulating different sections of notes)
    chunks = [
        "Neural networks consist of layers of interconnected nodes called neurons.",
        "Backpropagation is the algorithm used to train neural networks.",
        "Activation functions introduce non-linearity into neural networks.",
        "Common activation functions include ReLU, sigmoid, and tanh."
    ]
    
    print(f"Processing {len(chunks)} chunks...")
    
    summarizer = Summarizer(model_name="t5-small")
    
    # Summarize each chunk
    summaries = summarizer.summarize_chunks(chunks, max_length=30)
    
    print("\n--- Chunk Summaries ---")
    for i, summary in enumerate(summaries, 1):
        print(f"{i}. {summary}")
    
    print()


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("  StudyBuddy Usage Examples")
    print("="*60 + "\n")
    
    print("These examples show how to use StudyBuddy components.\n")
    print("Note: First run will download models (~500MB) and may be slow.\n")
    
    # Run examples
    try:
        example_1_basic_usage()
        input("Press Enter to continue to Example 2...")
        
        example_2_pdf_processing()
        input("Press Enter to continue to Example 3...")
        
        example_3_concept_extraction()
        input("Press Enter to continue to Example 4...")
        
        example_4_custom_pipeline()
        input("Press Enter to continue to Example 5...")
        
        example_5_batch_processing()
        
        print("="*60)
        print("  All examples completed!")
        print("="*60 + "\n")
        
    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Make sure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        print("  python -m spacy download en_core_web_sm")


if __name__ == "__main__":
    main()
