"""
Improved Question Generator Module
Generates better study questions using sentence analysis and templates.
"""

from typing import List
import re


class ImprovedQuestionGenerator:
    """Generate study questions using intelligent templates and sentence analysis."""
    
    def __init__(self):
        """Initialize the question generator."""
        print("Using improved question generation...")
        self.question_templates = [
            "What is {}?",
            "Who was {}?",
            "When did {} occur?",
            "How did {} work?",
            "Why was {} important?",
            "What were the main features of {}?",
            "Describe the role of {}.",
            "Explain the significance of {}.",
            "What impact did {} have?",
            "How was {} established?"
        ]
    
    def generate_questions_from_concepts(self, text: str, concepts: List[str], 
                                        max_questions: int = 15) -> List[str]:
        """
        Generate questions from key concepts.
        
        Args:
            text: Source text
            concepts: List of key concepts
            max_questions: Maximum questions to generate
            
        Returns:
            List of questions
        """
        questions = []
        
        print(f"Generating {max_questions} questions from concepts...")
        
        # Generate questions from concepts
        for i, concept in enumerate(concepts):
            if len(questions) >= max_questions:
                break
            
            # Choose template based on concept type
            if any(name in concept.lower() for name in ['washington', 'jefferson', 'franklin', 'adams', 'madison', 'hamilton']):
                template = "Who was {}?"
            elif any(word in concept.lower() for word in ['war', 'convention', 'purchase', 'declaration']):
                template = "What was {}?"
            elif re.search(r'\d{4}', concept):  # Contains year
                template = "What happened in {}?"
            else:
                template = self.question_templates[i % len(self.question_templates)]
            
            question = template.format(concept)
            questions.append(question)
        
        # Generate additional questions from text analysis
        sentences = self._extract_key_sentences(text)
        
        for sentence in sentences:
            if len(questions) >= max_questions:
                break
            
            question = self._sentence_to_question(sentence)
            if question and question not in questions:
                questions.append(question)
        
        print(f"✓ Generated {len(questions)} questions")
        return questions[:max_questions]
    
    def generate_simple_questions(self, text: str, num_questions: int = 15) -> List[str]:
        """
        Generate questions from text analysis.
        
        Args:
            text: Source text
            num_questions: Number of questions to generate
            
        Returns:
            List of questions
        """
        questions = []
        
        print(f"Generating {num_questions} questions from text...")
        
        # Extract key sentences
        sentences = self._extract_key_sentences(text)
        
        for sentence in sentences:
            if len(questions) >= num_questions:
                break
            
            question = self._sentence_to_question(sentence)
            if question and question not in questions:
                questions.append(question)
        
        # If we don't have enough, add template-based questions
        if len(questions) < num_questions:
            additional = self._generate_template_questions(text, num_questions - len(questions))
            questions.extend(additional)
        
        print(f"✓ Generated {len(questions)} questions")
        return questions[:num_questions]
    
    def _extract_key_sentences(self, text: str) -> List[str]:
        """Extract important sentences from text."""
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        # Score sentences based on keywords
        scored_sentences = []
        keywords = ['was', 'were', 'is', 'are', 'became', 'served', 'founded', 
                   'created', 'established', 'known', 'called', 'invented']
        
        for sentence in sentences:
            score = sum(1 for keyword in keywords if keyword in sentence.lower())
            # Bonus for proper nouns (capitals)
            score += len(re.findall(r'\b[A-Z][a-z]+', sentence)) * 0.5
            # Bonus for numbers/dates
            score += len(re.findall(r'\b\d{4}\b', sentence)) * 2
            
            if score > 0:
                scored_sentences.append((score, sentence))
        
        # Sort by score and return top sentences
        scored_sentences.sort(reverse=True)
        return [sent for score, sent in scored_sentences[:30]]
    
    def _sentence_to_question(self, sentence: str) -> str:
        """Convert a statement into a question."""
        sentence = sentence.strip()
        
        # Pattern 1: "X was Y" -> "Who was X?" or "What was X?"
        match = re.search(r'^([A-Z][a-z]+ [A-Z][a-z]+) was (.+)', sentence)
        if match:
            subject = match.group(1)
            if any(title in subject for title in ['President', 'Secretary', 'Father']):
                return f"Who was {subject}?"
            return f"What was {subject}?"
        
        # Pattern 2: "X served as Y" -> "What role did X serve?"
        match = re.search(r'^([A-Z][a-z]+ [A-Z][a-z]+) served as', sentence)
        if match:
            return f"What role did {match.group(1)} serve?"
        
        # Pattern 3: Contains a year -> "What happened in YEAR?"
        match = re.search(r'in (\d{4})', sentence)
        if match:
            year = match.group(1)
            # Find what happened
            event_match = re.search(r'(\w+(?:\s+\w+){0,3})\s+in\s+' + year, sentence)
            if event_match:
                event = event_match.group(1).strip()
                return f"What was {event} in {year}?"
        
        # Pattern 4: "X created/founded/established Y" -> "What did X create/found/establish?"
        for verb in ['created', 'founded', 'established', 'invented', 'wrote']:
            if verb in sentence.lower():
                match = re.search(r'^([A-Z][a-z]+ [A-Z][a-z]+) ' + verb, sentence, re.IGNORECASE)
                if match:
                    return f"What did {match.group(1)} {verb}?"
        
        # Pattern 5: Look for important facts
        match = re.search(r'(the [A-Z][a-z]+(?: [A-Z][a-z]+)*)', sentence)
        if match:
            thing = match.group(1)
            return f"What was {thing}?"
        
        return None
    
    def _generate_template_questions(self, text: str, num_needed: int) -> List[str]:
        """Generate additional questions using templates."""
        questions = []
        
        # Find proper nouns
        proper_nouns = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*', text)
        proper_nouns = list(set(proper_nouns))[:num_needed]
        
        for noun in proper_nouns:
            if len(questions) >= num_needed:
                break
            
            # Determine question type
            if any(name in noun for name in ['Washington', 'Jefferson', 'Franklin', 'Adams', 'Madison', 'Hamilton']):
                questions.append(f"What were the major accomplishments of {noun}?")
            elif 'Constitution' in noun or 'Declaration' in noun:
                questions.append(f"What was the purpose of {noun}?")
            else:
                questions.append(f"What was the significance of {noun}?")
        
        return questions
    
    def filter_duplicate_questions(self, questions: List[str], 
                                   similarity_threshold: float = 0.7) -> List[str]:
        """Remove duplicate questions."""
        if not questions:
            return []
        
        unique_questions = []
        
        for question in questions:
            # Simple deduplication
            if question not in unique_questions:
                unique_questions.append(question)
        
        return unique_questions


if __name__ == "__main__":
    # Test the improved generator
    generator = ImprovedQuestionGenerator()
    
    sample_text = """
    George Washington served as the first President of the United States from 1789 to 1797.
    Thomas Jefferson was the primary author of the Declaration of Independence in 1776.
    Benjamin Franklin conducted famous experiments with electricity.
    The Constitutional Convention was held in Philadelphia in 1787.
    James Madison is known as the Father of the Constitution.
    """
    
    questions = generator.generate_simple_questions(sample_text, num_questions=5)
    
    print("\n=== Generated Questions ===")
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")
