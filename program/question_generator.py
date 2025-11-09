"""
Question Generator Module
Generates study questions from text and concepts using T5 models.
"""

from typing import List, Optional
import warnings
warnings.filterwarnings('ignore')


class QuestionGenerator:
    """Generate study questions using T5-based models."""
    
    def __init__(self, model_name: str = "t5-small"):
        """
        Initialize the QuestionGenerator.
        
        Args:
            model_name: Name of the T5 model to use
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load the T5 model for question generation."""
        try:
            from transformers import T5Tokenizer, T5ForConditionalGeneration
            
            print(f"Loading {self.model_name} for question generation...")
            self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
            self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
            print(f"✓ Question generation model loaded")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def generate_question_from_context(self, context: str, answer: str = None) -> Optional[str]:
        """
        Generate a question from a context (and optionally an answer).
        
        Args:
            context: The context text
            answer: Optional answer to generate question for
            
        Returns:
            Generated question or None
        """
        if not self.model or not self.tokenizer:
            return None
        
        try:
            # If answer provided, use it; otherwise, use the context itself
            if answer:
                input_text = f"generate question: context: {context} answer: {answer}"
            else:
                input_text = f"generate question: {context}"
            
            inputs = self.tokenizer.encode(
                input_text,
                return_tensors="pt",
                max_length=512,
                truncation=True
            )
            
            outputs = self.model.generate(
                inputs,
                max_length=64,
                num_beams=4,
                early_stopping=True,
                no_repeat_ngram_size=3
            )
            
            question = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Ensure it ends with a question mark
            if question and not question.endswith('?'):
                question += '?'
            
            return question
        
        except Exception as e:
            print(f"Error generating question: {e}")
            return None
    
    def generate_questions_from_concepts(self, text: str, concepts: List[str], 
                                        max_questions: int = 10) -> List[str]:
        """
        Generate questions based on key concepts.
        
        Args:
            text: The source text
            concepts: List of key concepts to generate questions about
            max_questions: Maximum number of questions to generate
            
        Returns:
            List of generated questions
        """
        questions = []
        
        print(f"Generating questions from {len(concepts)} concepts...")
        
        for i, concept in enumerate(concepts[:max_questions]):
            # Generate question using the concept as the answer
            question = self.generate_question_from_context(text[:500], concept)
            
            if question and question not in questions:
                questions.append(question)
            
            if (i + 1) % 3 == 0:
                print(f"  Generated {len(questions)} questions...")
        
        print(f"✓ Generated {len(questions)} questions")
        return questions
    
    def generate_simple_questions(self, text: str, num_questions: int = 10) -> List[str]:
        """
        Generate simple questions from text without explicit concepts.
        Uses different prompts to encourage variety.
        
        Args:
            text: Source text
            num_questions: Number of questions to generate
            
        Returns:
            List of questions
        """
        questions = []
        
        # Split text into sentences for variety
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 20]
        
        print(f"Generating {num_questions} questions from text...")
        
        prompts = [
            "generate question: ",
            "create a study question: ",
            "ask about: ",
            "what question can be asked: "
        ]
        
        prompt_idx = 0
        for i, sentence in enumerate(sentences[:num_questions * 2]):  # Process more to get enough
            if len(questions) >= num_questions:
                break
            
            # Use different prompts for variety
            prompt = prompts[prompt_idx % len(prompts)]
            prompt_idx += 1
            
            question = self._generate_with_prompt(prompt + sentence)
            
            if question and question not in questions and len(question) > 10:
                questions.append(question)
        
        # If we don't have enough, generate from full text chunks
        if len(questions) < num_questions:
            words = text.split()
            chunk_size = min(200, len(words) // 2)
            
            for i in range(0, len(words), chunk_size):
                if len(questions) >= num_questions:
                    break
                
                chunk = ' '.join(words[i:i + chunk_size])
                question = self.generate_question_from_context(chunk)
                
                if question and question not in questions:
                    questions.append(question)
        
        print(f"✓ Generated {len(questions)} questions")
        return questions[:num_questions]
    
    def _generate_with_prompt(self, prompt_text: str) -> Optional[str]:
        """Helper method to generate text with a specific prompt."""
        try:
            inputs = self.tokenizer.encode(
                prompt_text,
                return_tensors="pt",
                max_length=512,
                truncation=True
            )
            
            outputs = self.model.generate(
                inputs,
                max_length=64,
                num_beams=3,
                early_stopping=True,
                no_repeat_ngram_size=2
            )
            
            result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            if result and not result.endswith('?'):
                result += '?'
            
            return result
        except:
            return None
    
    def filter_duplicate_questions(self, questions: List[str], 
                                   similarity_threshold: float = 0.7) -> List[str]:
        """
        Remove duplicate or very similar questions.
        
        Args:
            questions: List of questions
            similarity_threshold: Threshold for considering questions similar
            
        Returns:
            Filtered list of unique questions
        """
        if not questions:
            return []
        
        unique_questions = []
        
        for question in questions:
            # Simple similarity check based on word overlap
            is_unique = True
            q_words = set(question.lower().split())
            
            for existing in unique_questions:
                e_words = set(existing.lower().split())
                overlap = len(q_words & e_words) / len(q_words | e_words)
                
                if overlap > similarity_threshold:
                    is_unique = False
                    break
            
            if is_unique:
                unique_questions.append(question)
        
        return unique_questions


if __name__ == "__main__":
    # Test the question generator
    generator = QuestionGenerator(model_name="t5-small")
    
    sample_text = """
    Machine learning is a branch of artificial intelligence that focuses on 
    building systems that can learn from data. Neural networks are computing 
    systems inspired by biological neural networks. Deep learning uses multiple 
    layers of neural networks to learn hierarchical representations.
    
    Supervised learning involves training models on labeled data. The model 
    learns to map inputs to outputs based on example input-output pairs. 
    Unsupervised learning works with unlabeled data to find patterns and structure.
    
    Popular machine learning frameworks include TensorFlow, PyTorch, and scikit-learn.
    These tools make it easier for developers to build and deploy ML models.
    """
    
    print("=== QUESTION GENERATION TEST ===\n")
    
    # Test simple question generation
    print("--- Generating Simple Questions ---")
    questions = generator.generate_simple_questions(sample_text, num_questions=5)
    
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")
    
    print("\n--- Generating Concept-Based Questions ---")
    concepts = ["machine learning", "neural networks", "supervised learning", 
                "TensorFlow", "deep learning"]
    
    concept_questions = generator.generate_questions_from_concepts(
        sample_text, concepts, max_questions=5
    )
    
    for i, q in enumerate(concept_questions, 1):
        print(f"{i}. {q}")
