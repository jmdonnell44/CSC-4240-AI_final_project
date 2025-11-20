"""
Chat Interface Module
Provides interactive command-based interface for StudyBuddy.
"""

from typing import Optional, Dict, Callable, List


class ChatInterface:
    """Interactive chat interface for StudyBuddy."""
    
    def __init__(self):
        """Initialize the chat interface."""
        self.context = {}
        self.commands = {
            'help': self.show_help,
            'summary': self.request_summary,
            'questions': self.request_questions,
            'concepts': self.show_concepts,
            'stats': self.show_stats,
            'exit': self.exit_chat,
            'quit': self.exit_chat
        }
        self.running = False
    
    def start(self, initial_context: Dict = None):
        """
        Start the interactive chat session.
        
        Args:
            initial_context: Initial context with document info
        """
        if initial_context:
            self.context = initial_context
        
        self.running = True
        
        print("\n" + "="*60)
        print("   Welcome to StudyBuddy - Your AI Study Partner!")
        print("="*60)
        print("\nI've processed your document and generated study materials.")
        print("Type 'help' to see available commands, or 'exit' to quit.\n")
        
        while self.running:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                self.process_input(user_input)
                
            except KeyboardInterrupt:
                print("\n\nExiting StudyBuddy. Good luck with your studies!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def process_input(self, user_input: str):
        """
        Process user input and execute commands.
        
        Args:
            user_input: User's input string
        """
        # Convert to lowercase for command matching
        input_lower = user_input.lower()
        
        # Check for exact command matches
        for command, handler in self.commands.items():
            if input_lower.startswith(command):
                handler(user_input)
                return
        
        # Check for keyword-based commands
        if 'summar' in input_lower:
            self.request_summary(user_input)
        elif 'question' in input_lower:
            self.request_questions(user_input)
        elif 'concept' in input_lower or 'keyword' in input_lower:
            self.show_concepts(user_input)
        elif 'help' in input_lower:
            self.show_help(user_input)
        else:
            print("StudyBuddy: I'm not sure what you mean. Type 'help' for available commands.")
    
    def show_help(self, user_input: str = ""):
        """Display help information."""
        print("\nStudyBuddy: Here are the commands I understand:\n")
        print("  📝 summary [topic]    - Get a summary (optionally about a specific topic)")
        print("  ❓ questions [n]      - Generate n more questions (default: 5)")
        print("  🔑 concepts           - Show extracted key concepts")
        print("  📊 stats              - Show document statistics")
        print("  ❔ help               - Show this help message")
        print("  🚪 exit/quit          - Exit StudyBuddy")
        print("\nYou can also ask naturally, like:")
        print("  • 'Give me 10 more questions'")
        print("  • 'Summarize the main ideas'")
        print("  • 'What are the key concepts?'\n")
    
    def request_summary(self, user_input: str):
        """Handle summary requests."""
        print("\nStudyBuddy: Here's a summary of your document:\n")
        
        if 'summary' in self.context:
            print(self.context['summary'])
        else:
            print("Summary not available. Please process a document first.")
        print()
    
    def request_questions(self, user_input: str):
        """Handle question generation requests."""
        # Try to extract number from input
        import re
        numbers = re.findall(r'\d+', user_input)
        num_questions = int(numbers[0]) if numbers else 5
        
        print(f"\nStudyBuddy: Generating {num_questions} study questions...\n")
        
        # This would call the question generator with additional questions
        if 'callback_generate_questions' in self.context:
            questions = self.context['callback_generate_questions'](num_questions)
            for i, q in enumerate(questions, 1):
                print(f"{i}. {q}")
        else:
            print("Question generation not available in this session.")
        print()
    
    def show_concepts(self, user_input: str):
        """Show extracted key concepts."""
        print("\nStudyBuddy: Here are the key concepts I identified:\n")
        
        if 'concepts' in self.context and self.context['concepts']:
            for i, concept in enumerate(self.context['concepts'][:15], 1):
                print(f"{i:2d}. {concept}")
        else:
            print("Concepts not available.")
        print()
    
    def show_stats(self, user_input: str):
        """Show document statistics."""
        print("\nStudyBuddy: Document Statistics\n")
        print("-" * 40)
        
        if 'stats' in self.context:
            stats = self.context['stats']
            for key, value in stats.items():
                key_formatted = key.replace('_', ' ').title()
                print(f"  {key_formatted}: {value}")
        else:
            print("  Statistics not available.")
        print()
    
    def exit_chat(self, user_input: str = ""):
        """Exit the chat interface."""
        print("\nStudyBuddy: Thanks for studying with me! Good luck! 📚\n")
        self.running = False
    
    def set_context(self, context: Dict):
        """
        Update the context with new information.
        
        Args:
            context: Dictionary with context information
        """
        self.context.update(context)
    
    def add_callback(self, name: str, callback: Callable):
        """
        Add a callback function for dynamic operations.
        
        Args:
            name: Name of the callback
            callback: Callback function
        """
        self.context[f'callback_{name}'] = callback


def create_simple_interface(summary: str, questions: List, concepts: List, stats: Dict):
    """
    Create a simple chat interface with pre-loaded data.
    
    Args:
        summary: Document summary
        questions: List of generated questions
        concepts: List of key concepts
        stats: Document statistics
        
    Returns:
        Configured ChatInterface instance
    """
    interface = ChatInterface()
    
    interface.set_context({
        'summary': summary,
        'questions': questions,
        'concepts': concepts,
        'stats': stats
    })
    
    return interface


if __name__ == "__main__":
    # Test the chat interface
    print("Testing ChatInterface...\n")
    
    # Create sample context
    sample_context = {
        'summary': "This document discusses artificial intelligence and machine learning concepts.",
        'questions': [
            "What is machine learning?",
            "How do neural networks work?",
            "What is supervised learning?"
        ],
        'concepts': [
            "machine learning",
            "neural networks", 
            "deep learning",
            "supervised learning",
            "artificial intelligence"
        ],
        'stats': {
            'total_words': 1500,
            'total_sentences': 75,
            'total_questions': 15
        }
    }
    
    # Create and start interface
    interface = ChatInterface()
    interface.start(sample_context)
