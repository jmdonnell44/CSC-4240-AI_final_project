#!/usr/bin/env python3
"""
StudyBuddy - AI-Powered Study Question Generator
Main pipeline orchestration and CLI entry point.
"""

import argparse
import os
import sys
from datetime import datetime

from text_extractor import TextExtractor
from preprocessor import Preprocessor
from concept_extractor import ConceptExtractor
from summarizer import Summarizer
from question_generator import QuestionGenerator
from chat_interface import ChatInterface


class StudyBuddy:
    """Main StudyBuddy application class."""
    
    def __init__(self, verbose: bool = True):
        """
        Initialize StudyBuddy with all components.
        
        Args:
            verbose: Whether to print progress messages
        """
        self.verbose = verbose
        self.text_extractor = None
        self.preprocessor = None
        self.concept_extractor = None
        self.summarizer = None
        self.question_generator = None
        
        self.document_text = None
        self.processed_data = None
        self.results = {}
    
    def initialize(self):
        """Initialize all components."""
        if self.verbose:
            print("\n" + "="*60)
            print("  Initializing StudyBuddy Components...")
            print("="*60 + "\n")
        
        # Initialize components
        self.text_extractor = TextExtractor()
        self.preprocessor = Preprocessor(chunk_size=512, overlap=128)
        self.concept_extractor = ConceptExtractor()
        self.summarizer = Summarizer(model_name="t5-small")
        self.question_generator = QuestionGenerator(model_name="t5-small")
        
        if self.verbose:
            print("\n✓ All components initialized successfully!\n")
    
    def process_document(self, file_path: str, num_questions: int = 15):
        """
        Process a document through the complete pipeline.
        
        Args:
            file_path: Path to the document file
            num_questions: Number of questions to generate
            
        Returns:
            Dictionary with all results
        """
        if not os.path.exists(file_path):
            print(f"Error: File not found: {file_path}")
            return None
        
        if self.verbose:
            print("="*60)
            print(f"  Processing: {os.path.basename(file_path)}")
            print("="*60 + "\n")
        
        # Step 1: Extract text
        if self.verbose:
            print("Step 1/5: Extracting text from document...")
        
        self.document_text = self.text_extractor.extract_from_file(file_path)
        
        if not self.document_text:
            print("Failed to extract text from document.")
            return None
        
        # Step 2: Preprocess
        if self.verbose:
            print("\nStep 2/5: Preprocessing and chunking text...")
        
        self.processed_data = self.preprocessor.preprocess(self.document_text)
        
        if self.verbose:
            print(f"✓ Created {self.processed_data['metadata']['total_chunks']} chunks")
        
        # Step 3: Extract concepts
        if self.verbose:
            print("\nStep 3/5: Extracting key concepts...")
        
        concepts_data = self.concept_extractor.extract_all_concepts(
            self.processed_data['cleaned_text'],
            top_keywords=20
        )
        
        important_concepts = self.concept_extractor.get_important_concepts(
            self.processed_data['cleaned_text'],
            top_n=15
        )
        
        # Step 4: Generate summary
        if self.verbose:
            print("\nStep 4/5: Generating summary...")
        
        summary = self.summarizer.generate_overall_summary(
            self.processed_data['cleaned_text'],
            target_length=200
        )
        
        if self.verbose:
            print(f"✓ Generated summary ({len(summary.split())} words)")
        
        # Step 5: Generate questions
        if self.verbose:
            print(f"\nStep 5/5: Generating {num_questions} study questions...")
        
        questions = self.question_generator.generate_simple_questions(
            self.processed_data['cleaned_text'],
            num_questions=num_questions
        )
        
        # Filter duplicates
        questions = self.question_generator.filter_duplicate_questions(questions)
        
        # Store results
        self.results = {
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'processed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'summary': summary,
            'questions': questions,
            'concepts': important_concepts,
            'all_concepts_data': concepts_data,
            'statistics': {
                'original_characters': len(self.document_text),
                'word_count': self.processed_data['metadata']['total_words'],
                'sentence_count': self.processed_data['metadata']['total_sentences'],
                'chunk_count': self.processed_data['metadata']['total_chunks'],
                'total_questions': len(questions),
                'total_concepts': len(important_concepts)
            }
        }
        
        if self.verbose:
            print("\n" + "="*60)
            print("  ✓ Processing Complete!")
            print("="*60 + "\n")
        
        return self.results
    
    def display_results(self):
        """Display the processing results."""
        if not self.results:
            print("No results to display. Process a document first.")
            return
        
        print("\n" + "="*60)
        print("  STUDYBUDDY RESULTS")
        print("="*60 + "\n")
        
        # Summary
        print("📋 SUMMARY")
        print("-" * 60)
        print(self.results['summary'])
        print()
        
        # Questions
        print("\n❓ STUDY QUESTIONS")
        print("-" * 60)
        for i, question in enumerate(self.results['questions'], 1):
            print(f"{i:2d}. {question}")
        print()
        
        # Key concepts
        print("\n🔑 KEY CONCEPTS")
        print("-" * 60)
        for i, concept in enumerate(self.results['concepts'], 1):
            print(f"{i:2d}. {concept}")
        print()
        
        # Statistics
        print("\n📊 STATISTICS")
        print("-" * 60)
        stats = self.results['statistics']
        print(f"  Words: {stats['word_count']}")
        print(f"  Sentences: {stats['sentence_count']}")
        print(f"  Questions Generated: {stats['total_questions']}")
        print(f"  Key Concepts: {stats['total_concepts']}")
        print()
    
    def save_results(self, output_file: str = None):
        """
        Save results to a text file.
        
        Args:
            output_file: Path to output file (optional)
        """
        if not self.results:
            print("No results to save.")
            return
        
        if not output_file:
            base_name = os.path.splitext(self.results['file_name'])[0]
            output_file = f"{base_name}_study_guide.txt"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("  STUDYBUDDY STUDY GUIDE\n")
                f.write("="*60 + "\n\n")
                f.write(f"Document: {self.results['file_name']}\n")
                f.write(f"Generated: {self.results['processed_at']}\n\n")
                
                f.write("SUMMARY\n")
                f.write("-"*60 + "\n")
                f.write(self.results['summary'] + "\n\n")
                
                f.write("STUDY QUESTIONS\n")
                f.write("-"*60 + "\n")
                for i, q in enumerate(self.results['questions'], 1):
                    f.write(f"{i}. {q}\n")
                f.write("\n")
                
                f.write("KEY CONCEPTS\n")
                f.write("-"*60 + "\n")
                for i, c in enumerate(self.results['concepts'], 1):
                    f.write(f"{i}. {c}\n")
                f.write("\n")
            
            print(f"✓ Results saved to: {output_file}")
        
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def start_chat(self):
        """Start interactive chat interface."""
        if not self.results:
            print("No results available. Process a document first.")
            return
        
        interface = ChatInterface()
        
        # Set up context
        interface.set_context({
            'summary': self.results['summary'],
            'questions': self.results['questions'],
            'concepts': self.results['concepts'],
            'stats': self.results['statistics']
        })
        
        # Add callback for generating more questions
        def generate_more_questions(n):
            return self.question_generator.generate_simple_questions(
                self.processed_data['cleaned_text'],
                num_questions=n
            )
        
        interface.add_callback('generate_questions', generate_more_questions)
        
        # Start the interface
        interface.start()


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="StudyBuddy - AI-Powered Study Question Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s my_notes.pdf
  %(prog)s my_notes.pdf -n 20 -o study_guide.txt
  %(prog)s my_notes.pdf --chat
  %(prog)s my_notes.pdf -q --no-save
        """
    )
    
    parser.add_argument('file', help='Path to the document file (PDF or TXT)')
    parser.add_argument('-n', '--num-questions', type=int, default=15,
                       help='Number of questions to generate (default: 15)')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='Suppress progress messages')
    parser.add_argument('--no-save', action='store_true',
                       help='Don\'t save results to file')
    parser.add_argument('--chat', action='store_true',
                       help='Start interactive chat after processing')
    
    args = parser.parse_args()
    
    # Create StudyBuddy instance
    app = StudyBuddy(verbose=not args.quiet)
    
    # Initialize
    app.initialize()
    
    # Process document
    results = app.process_document(args.file, num_questions=args.num_questions)
    
    if not results:
        sys.exit(1)
    
    # Display results
    if not args.quiet:
        app.display_results()
    
    # Save results
    if not args.no_save:
        app.save_results(args.output)
    
    # Start chat if requested
    if args.chat:
        app.start_chat()
    
    print("\n✓ StudyBuddy finished successfully!")


if __name__ == "__main__":
    main()
