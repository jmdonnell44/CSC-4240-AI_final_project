"""
Smart Question Generator Module
Generates high-quality study questions by analyzing sentence patterns.
"""

from typing import List, Set
import re


class SmartQuestionGenerator:
    """Generate study questions using intelligent sentence analysis."""
    
    def __init__(self):
        """Initialize the question generator."""
        print("Using smart question generation...")
    
    def generate_questions_from_concepts(self, text: str, concepts: List[str], 
                                        max_questions: int = 15) -> List[str]:
        """
        Generate questions from text analysis.
        
        Args:
            text: Source text
            concepts: List of key concepts (not used in this version)
            max_questions: Maximum questions to generate
            
        Returns:
            List of questions
        """
        return self.generate_simple_questions(text, max_questions)
    
    def generate_simple_questions(self, text: str, num_questions: int = 15) -> List[str]:
        """
        Generate questions by analyzing sentence patterns.
        
        Args:
            text: Source text
            num_questions: Number of questions to generate
            
        Returns:
            List of questions
        """
        print(f"Generating {num_questions} questions from text analysis...")
        
        questions = []
        seen_questions = set()
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 30]
        
        for sentence in sentences:
            if len(questions) >= num_questions:
                break
            
            # Try multiple question patterns
            new_questions = self._extract_questions_from_sentence(sentence)
            
            for q in new_questions:
                if q and q not in seen_questions and len(questions) < num_questions:
                    questions.append(q)
                    seen_questions.add(q)
        
        print(f"✓ Generated {len(questions)} questions")
        return questions
    
    def _extract_questions_from_sentence(self, sentence: str) -> List[str]:
        """Extract multiple possible questions from a sentence."""
        questions = []
        
        # Pattern 1: "NAME served as ROLE" -> "What position did NAME hold?"
        match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+) served as (the )?([^,\.]+)', sentence)
        if match:
            name = match.group(1)
            role = match.group(3).strip()
            questions.append(f"What position did {name} hold?")
            questions.append(f"Who served as {role}?")
        
        # Pattern 2: "NAME was DESCRIPTION" -> "Who was NAME?"
        match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+) was (the )?(primary author|first|chief|one of)', sentence)
        if match:
            name = match.group(1)
            questions.append(f"Who was {name}?")
        
        # Pattern 3: Year mentions -> "What happened in YEAR?"
        years = re.findall(r'\b(1[67]\d{2})\b', sentence)
        for year in years:
            # Find what happened in that year
            context_match = re.search(r'([^.!?]{20,60})\s+' + year, sentence)
            if context_match:
                context = context_match.group(1).strip()
                # Clean up the context
                context = re.sub(r'^(in|from|during|after|before)\s+', '', context, flags=re.IGNORECASE)
                if len(context) > 10:
                    questions.append(f"What happened in {year}?")
                    break
        
        # Pattern 4: "NAME created/founded/wrote/invented X" 
        match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+) (created|founded|wrote|invented|authored|established) (the )?([^,\.]+)', sentence)
        if match:
            name = match.group(1)
            verb = match.group(2)
            thing = match.group(4).strip()
            questions.append(f"What did {name} {verb}?")
        
        # Pattern 5: "The EVENT was/were DESCRIPTION"
        match = re.search(r'[Tt]he ([A-Z][a-z]+(?: [A-Z][a-z]+)*) (was|were) ([^,\.]{10,60})', sentence)
        if match:
            event = match.group(1)
            if event not in ['United States', 'Constitutional Convention']:  # Avoid overly broad terms
                questions.append(f"What was the {event}?")
        
        # Pattern 6: Numbers/quantities -> "How many..."
        match = re.search(r'(first|second|third|\d+) ([^,\.]{5,30})', sentence)
        if match and 'amendment' in sentence.lower():
            questions.append("How many amendments are in the Bill of Rights?")
        
        # Pattern 7: Famous documents/events
        if 'Declaration of Independence' in sentence:
            questions.append("What is the Declaration of Independence?")
        if 'Bill of Rights' in sentence:
            questions.append("What is the Bill of Rights?")
        if 'Constitutional Convention' in sentence:
            questions.append("When was the Constitutional Convention held?")
        if 'Louisiana Purchase' in sentence:
            questions.append("What was the Louisiana Purchase?")
        if 'Federalist Papers' in sentence:
            questions.append("What were the Federalist Papers?")
        
        # Pattern 8: "NAME is known as TITLE" -> "What is NAME known as?"
        match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+) is known as (the )?([^,\.]+)', sentence)
        if match:
            name = match.group(1)
            title = match.group(3).strip()
            questions.append(f"What is {name} known as?")
            questions.append(f"Who is known as the {title}?")
        
        # Pattern 9: President mentions
        match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+) (became|was) the (first|second|third|fourth) President', sentence)
        if match:
            name = match.group(1)
            number = match.group(3)
            questions.append(f"Who was the {number} President of the United States?")
        
        # Pattern 10: Accomplishments/achievements
        if any(word in sentence.lower() for word in ['doubled', 'established', 'created', 'founded', 'secured']):
            match = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', sentence)
            if match:
                name = match.group(1)
                questions.append(f"What were the major accomplishments of {name}?")
        
        return questions
    
    def filter_duplicate_questions(self, questions: List[str], 
                                   similarity_threshold: float = 0.7) -> List[str]:
        """Remove duplicate questions."""
        if not questions:
            return []
        
        unique_questions = []
        seen_lower = set()
        
        for question in questions:
            question_lower = question.lower()
            if question_lower not in seen_lower:
                unique_questions.append(question)
                seen_lower.add(question_lower)
        
        return unique_questions


if __name__ == "__main__":
    # Test the generator
    generator = SmartQuestionGenerator()
    
    sample = """
    George Washington served as the commander-in-chief of the Continental Army during the American Revolutionary War from 1775 to 1783.
    Thomas Jefferson was the primary author of the Declaration of Independence in 1776.
    James Madison is known as the Father of the Constitution.
    The Constitutional Convention was held in Philadelphia in 1787.
    Benjamin Franklin invented bifocal glasses, the lightning rod, and the Franklin stove.
    """
    
    questions = generator.generate_simple_questions(sample, 10)
    
    print("\n=== Test Questions ===")
    for i, q in enumerate(questions, 1):
        print(f"{i}. {q}")
