#!/usr/bin/env python3
"""
StudyBuddy - AI-Powered Study Question Generator
Main pipeline orchestration and CLI entry point.
"""

import argparse
import os
import sys
import re
import textwrap
from datetime import datetime

from text_extractor import TextExtractor
from preprocessor import Preprocessor
from concept_extractor import ConceptExtractor
from summarizer import Summarizer
from smart_question_generator import SmartQuestionGenerator
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
        self.question_generator = SmartQuestionGenerator()
        
        if self.verbose:
            print("\n[OK] All components initialized successfully!\n")
    
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
            print(f"[OK] Created {self.processed_data['metadata']['total_chunks']} chunks")
        
        # Step 3: Extract concepts
        if self.verbose:
            print("\nStep 3/5: Extracting key concepts...")
        
        concepts_data = self.concept_extractor.extract_all_concepts(
            self.processed_data['cleaned_text'],
            top_keywords=20
        )
        
        important_concepts = self.concept_extractor.get_important_concepts(
            self.processed_data['cleaned_text'],
            top_n=20
        )
        # Filter out incomplete/malformed concepts and deduplicate
        seen_concepts = set()
        filtered_concepts = []
        for c in important_concepts:
            c_lower = c.lower()
            # Skip if already seen
            if c_lower in seen_concepts:
                continue
            # Skip single incomplete words
            if len(c.split()) == 1 and c_lower in ['neural', 'training', 'model', 'sigmoid', 'neurons', 'neuron']:
                continue
            # Skip if too short or contains weird artifacts
            if len(c) < 4 or len(c.split()) > 5:
                continue
            seen_concepts.add(c_lower)
            filtered_concepts.append(c)

        important_concepts = filtered_concepts[:15]
        
        # Step 4: Generate summary (grounded in source sentences to avoid contradictions)
        if self.verbose:
            print("\nStep 4/5: Generating summary...")
        
        summary = self._build_grounded_summary(self.processed_data.get('sentences', []), max_items=6)
        if not summary:
            summary = self.summarizer.generate_overall_summary(
                self.processed_data['cleaned_text'],
                target_length=350
            )
            summary = self._augment_summary(summary, self.processed_data.get('sentences', []))
            summary = self._normalize_summary(summary)
        
        if summary:
            if self.verbose:
                print(f"[OK] Generated summary ({len(summary.split())} words)")
        else:
            summary = "Summary generation unavailable (model loading issue)."
            if self.verbose:
                print("[WARN] Summary generation skipped")
        
        # Step 5: Generate questions
        if self.verbose:
            print(f"\nStep 5/5: Generating {num_questions} study questions...")
        
        questions, answers = self.question_generator.generate_question_answer_pairs(
            self.processed_data['cleaned_text'],
            important_concepts,
            max_questions=num_questions
        )
        if len(questions) < num_questions and len(answers) < num_questions:
            # Backfill with simple questions if we somehow came up short
            extras = self.question_generator.generate_simple_questions(
                self.processed_data['cleaned_text'],
                num_questions - len(questions)
            )
            questions.extend(extras)
            answers.extend(["Answer unavailable."] * len(extras))
        if len(answers) < len(questions):
            answers.extend(["Answer unavailable."] * (len(questions) - len(answers)))
        concept_details = self.question_generator.describe_concepts(
            important_concepts,
            self.processed_data['sentences']
        )
        concept_details = concept_details[:8]
        
        # Store results
        self.results = {
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'processed_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'summary': summary,
            'questions': questions,
            'answers': answers,
            'concept_details': concept_details,
            'concepts': important_concepts,
            'all_concepts_data': concepts_data,
            'statistics': {
                'original_characters': len(self.document_text),
                'word_count': self.processed_data['metadata']['total_words'],
                'sentence_count': self.processed_data['metadata']['total_sentences'],
                'chunk_count': self.processed_data['metadata']['total_chunks'],
                'total_questions': len(questions),
                'total_concepts': len(concept_details)
            }
        }
        
        if self.verbose:
            print("\n" + "="*60)
            print("  [OK] Processing Complete!")
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
        print("SUMMARY")
        print("-" * 60)
        self._print_formatted_summary(self.results['summary'])

        # Questions
        print("\nSTUDY QUESTIONS")
        print("-" * 60)
        for i, (question, answer) in enumerate(zip(self.results['questions'], self.results.get('answers', [])), 1):
            print(f"{i:2d}. {question}")
            print(f"    Answer: {answer}")
        print()

        # Key concepts
        print("\nKEY CONCEPTS")
        print("-" * 60)
        for i, item in enumerate(self.results.get('concept_details', []), 1):
            print(f"{i:2d}. {item['description']}")
        print()

        # Statistics
        print("\nSTATISTICS")
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
                f.write(self._format_summary_text(self.results['summary']))
                f.write("\n")
                
                f.write("STUDY QUESTIONS\n")
                f.write("-"*60 + "\n")
                for i, (q, a) in enumerate(zip(self.results['questions'], self.results.get('answers', [])), 1):
                    f.write(f"{i}. {q}\n")
                    f.write(f"   Answer: {a}\n\n")
                
                f.write("KEY CONCEPTS\n")
                f.write("-"*60 + "\n")
                for item in self.results.get('concept_details', []):
                    f.write(f"- {item['description']}\n")
                f.write("\n")
            
            print(f"[OK] Results saved to: {output_file}")
        
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
            'answers': self.results.get('answers', []),
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
    
    def _augment_summary(self, summary: str, sentences: list) -> str:
        """
        Ensure the summary is sufficiently detailed by appending key sentences
        when the generated summary is too short.
        """
        if not summary:
            return ' '.join(sentences[:5]) if sentences else "Summary unavailable."
        
        word_count = len(summary.split())
        if word_count >= 120:
            return summary
        
        extras = []
        for s in sentences:
            if len(' '.join(extras + [s]).split()) + word_count > 200:
                break
            if s and s not in summary:
                extras.append(s)
        if extras:
            return (summary.strip() + " " + ' '.join(extras)).strip()
        return summary
    
    def _normalize_summary(self, summary: str) -> str:
        """Deduplicate summary sentences and fix basic capitalization/punctuation."""
        if not summary:
            return "Summary unavailable."
        
        parts = [s.strip() for s in re.split(r'(?<=[.!?])\s+', summary) if s.strip()]
        seen = set()
        normalized = []
        for idx, s in enumerate(parts):
            key = s.lower().rstrip('.!?')
            if key in seen:
                continue
            seen.add(key)
            fixed = s.rstrip('.!?').strip()
            if fixed:
                paraphrased = self._paraphrase_sentence(fixed, idx)
                normalized.append(paraphrased)
        return ' '.join(normalized)
    
    def _build_grounded_summary(self, sentences: list, max_items: int = 5) -> str:
        """Create a concise, non-contradictory summary from source sentences."""
        if not sentences:
            return ""
        
        unique = []
        seen = set()
        for s in sentences:
            s_clean = s.strip()
            key = s_clean.lower().rstrip('.!?')
            if s_clean and key not in seen:
                seen.add(key)
                unique.append(s_clean)
            if len(unique) >= max_items:
                break
        
        paraphrased = []
        for idx, s in enumerate(unique):
            paraphrased.append(self._paraphrase_sentence(s, idx))
        
        return ' '.join(paraphrased)
    
    def _paraphrase_sentence(self, sentence: str, variant_index: int = 0) -> str:
        """Lightly rephrase a sentence to avoid mirroring source wording."""
        content = sentence.strip().rstrip('.!?')
        if not content:
            return ""

        # Keep paraphrasing minimal and direct to avoid repetitive prefixes
        content_lower = content[0].lower() + content[1:] if len(content) > 1 else content.lower()
        paraphrased_content = self._apply_paraphrasing_rules(content_lower)
        # Simple sentence with capitalization
        paraphrased = paraphrased_content.capitalize()
        if not paraphrased.endswith('.'):
            paraphrased += '.'
        return paraphrased

    def _apply_paraphrasing_rules(self, text: str) -> str:
        """Apply basic paraphrasing rules to avoid verbatim copying."""
        # Dictionary of common word substitutions
        substitutions = {
            r'\bcomposed of\b': 'made up of',
            r'\bincludes\b': 'contains',
            r'\binvolves\b': 'requires',
            r'\ballowing them to\b': 'which enables them to',
            r'\bcomes from\b': 'originates from',
            r'\bwidely used in\b': 'commonly applied to',
            r'\bmeasures\b': 'quantifies',
            r'\breducing\b': 'minimizing',
            r'\bimproving\b': 'enhancing'
        }

        result = text
        for pattern, replacement in substitutions.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

        return result
    
    def _format_summary_text(self, summary: str) -> str:
        """Return a neatly formatted summary string for saving."""
        if not summary:
            return "Summary unavailable.\n"
        
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', summary) if s.strip()]
        paragraph = ' '.join(sentences).strip()
        if not paragraph.endswith('.'):
            paragraph += '.'
        # Wrap to a reasonable width for readability
        wrapped = textwrap.fill(paragraph, width=88)
        return wrapped + "\n"
    
    def _print_formatted_summary(self, summary: str):
        """Print summary as a clean paragraph."""
        formatted = self._format_summary_text(summary).strip()
        print(formatted)


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
    parser.add_argument('-n', '--num-questions', type=int, default=5,
                       help='Number of questions to generate (default: 5)')
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

    # If chat mode is activated, generate only 5 questions initially
    num_questions = 5 if args.chat else args.num_questions

    # Process document
    results = app.process_document(args.file, num_questions=num_questions)
    
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
    
    print("\n[OK] StudyBuddy finished successfully!")


if __name__ == "__main__":
    main()
