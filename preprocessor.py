"""
Preprocessor Module
Handles text cleaning, normalization, and chunking for NLP processing.
"""

import re
from typing import List


class Preprocessor:
    """Clean and chunk text for processing."""
    
    def __init__(self, chunk_size: int = 512, overlap: int = 128):
        """
        Initialize the Preprocessor.
        
        Args:
            chunk_size: Maximum number of words per chunk
            overlap: Number of words to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text.
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text:
            return ""
        
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep periods, commas, and basic punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-\']', '', text)
        
        # Fix spacing around punctuation
        text = re.sub(r'\s+([.,!?;:])', r'\1', text)
        
        # Remove multiple periods (but keep ellipsis)
        text = re.sub(r'\.{4,}', '...', text)
        
        # Normalize line breaks
        text = re.sub(r'\n+', '\n', text)
        
        return text.strip()
    
    def split_into_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences.
        
        Args:
            text: Text to split
            
        Returns:
            List of sentences
        """
        # Simple sentence splitter (can be improved with NLTK)
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            
        Returns:
            List of text chunks
        """
        # Split into words
        words = text.split()
        
        if len(words) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(words):
            end = start + self.chunk_size
            chunk_words = words[start:end]
            chunk_text = ' '.join(chunk_words)
            chunks.append(chunk_text)
            
            # Move start position with overlap
            start += self.chunk_size - self.overlap
        
        return chunks
    
    def preprocess(self, text: str) -> dict:
        """
        Full preprocessing pipeline: clean and chunk text.
        
        Args:
            text: Raw text to process
            
        Returns:
            Dictionary with cleaned text, chunks, and metadata
        """
        # Clean the text
        cleaned_text = self.clean_text(text)
        
        # Split into sentences
        sentences = self.split_into_sentences(cleaned_text)
        
        # Create chunks
        chunks = self.chunk_text(cleaned_text)
        
        # Calculate statistics
        word_count = len(cleaned_text.split())
        
        result = {
            "cleaned_text": cleaned_text,
            "sentences": sentences,
            "chunks": chunks,
            "metadata": {
                "total_words": word_count,
                "total_sentences": len(sentences),
                "total_chunks": len(chunks),
                "chunk_size": self.chunk_size,
                "overlap": self.overlap
            }
        }
        
        return result
    
    def get_statistics(self, text: str) -> dict:
        """
        Get text statistics.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with statistics
        """
        words = text.split()
        sentences = self.split_into_sentences(text)
        
        return {
            "character_count": len(text),
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_words_per_sentence": round(len(words) / len(sentences), 2) if sentences else 0
        }


if __name__ == "__main__":
    # Test the preprocessor
    preprocessor = Preprocessor(chunk_size=100, overlap=20)
    
    sample_text = """
    Artificial Intelligence is transforming education. Machine learning algorithms 
    can now analyze student performance and provide personalized recommendations.
    Natural Language Processing enables automated essay grading and feedback.
    
    However, there are challenges. Privacy concerns must be addressed. Teachers 
    need training to use these tools effectively. The digital divide may widen 
    educational inequalities.
    
    Despite challenges, AI in education offers tremendous potential. Adaptive 
    learning systems can tailor content to individual needs. Intelligent tutoring 
    systems provide 24/7 support. The future of education is increasingly digital.
    """
    
    result = preprocessor.preprocess(sample_text)
    
    print("=== PREPROCESSING RESULTS ===\n")
    print(f"Original length: {len(sample_text)} characters")
    print(f"Cleaned length: {len(result['cleaned_text'])} characters")
    print(f"\nMetadata: {result['metadata']}")
    print(f"\nNumber of chunks: {len(result['chunks'])}")
    print(f"\nFirst chunk:\n{result['chunks'][0][:200]}...")
    
    stats = preprocessor.get_statistics(result['cleaned_text'])
    print(f"\nStatistics: {stats}")
