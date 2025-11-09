"""
Summarizer Module
Generates summaries using T5 transformer model from Hugging Face.
"""

from typing import Optional
import warnings
warnings.filterwarnings('ignore')


class Summarizer:
    """Generate summaries using T5 model."""
    
    def __init__(self, model_name: str = "t5-small"):
        """
        Initialize the Summarizer with a T5 model.
        
        Args:
            model_name: Name of the T5 model to use (t5-small, t5-base)
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load the T5 model and tokenizer."""
        try:
            from transformers import T5Tokenizer, T5ForConditionalGeneration
            
            print(f"Loading {self.model_name} model for summarization...")
            self.tokenizer = T5Tokenizer.from_pretrained(self.model_name)
            self.model = T5ForConditionalGeneration.from_pretrained(self.model_name)
            print(f"✓ {self.model_name} model loaded")
        except Exception as e:
            print(f"Error loading model: {e}")
    
    def summarize(self, text: str, max_length: int = 150, min_length: int = 40) -> Optional[str]:
        """
        Generate a summary of the input text.
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary in tokens
            min_length: Minimum length of summary in tokens
            
        Returns:
            Generated summary or None if generation fails
        """
        if not self.model or not self.tokenizer:
            print("Error: Model not loaded")
            return None
        
        if not text or len(text.strip()) < 50:
            return "Text too short to summarize."
        
        try:
            # Prepare input
            input_text = "summarize: " + text
            
            # Tokenize
            inputs = self.tokenizer.encode(
                input_text,
                return_tensors="pt",
                max_length=512,
                truncation=True
            )
            
            # Generate summary
            summary_ids = self.model.generate(
                inputs,
                max_length=max_length,
                min_length=min_length,
                length_penalty=2.0,
                num_beams=4,
                early_stopping=True
            )
            
            # Decode
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            
            return summary
        
        except Exception as e:
            print(f"Error generating summary: {e}")
            return None
    
    def summarize_chunks(self, chunks: list, max_length: int = 150) -> list:
        """
        Summarize multiple text chunks.
        
        Args:
            chunks: List of text chunks to summarize
            max_length: Maximum length per summary
            
        Returns:
            List of summaries
        """
        summaries = []
        
        print(f"Summarizing {len(chunks)} chunks...")
        for i, chunk in enumerate(chunks, 1):
            if len(chunk.split()) > 30:  # Only summarize substantial chunks
                summary = self.summarize(chunk, max_length=max_length)
                if summary:
                    summaries.append(summary)
                    
                if i % 5 == 0:
                    print(f"  Processed {i}/{len(chunks)} chunks")
        
        print(f"✓ Generated {len(summaries)} summaries")
        return summaries
    
    def generate_overall_summary(self, text: str, target_length: int = 200) -> str:
        """
        Generate an overall summary of a long document.
        
        Args:
            text: Full text to summarize
            target_length: Target length of the summary
            
        Returns:
            Overall summary
        """
        # For very long texts, we may need to chunk and combine
        words = text.split()
        
        if len(words) <= 500:
            # Short enough to summarize directly
            return self.summarize(text, max_length=target_length)
        else:
            # Split into manageable chunks and summarize each
            chunk_size = 500
            chunks = []
            for i in range(0, len(words), chunk_size):
                chunk = ' '.join(words[i:i + chunk_size])
                chunks.append(chunk)
            
            # Summarize each chunk
            chunk_summaries = self.summarize_chunks(chunks, max_length=100)
            
            # Combine chunk summaries
            combined = ' '.join(chunk_summaries)
            
            # Summarize the combined summaries
            final_summary = self.summarize(combined, max_length=target_length)
            
            return final_summary if final_summary else "Unable to generate summary."


if __name__ == "__main__":
    # Test the summarizer
    summarizer = Summarizer(model_name="t5-small")
    
    sample_text = """
    Artificial intelligence has made remarkable progress in recent years, 
    particularly in the field of natural language processing. Large language 
    models like GPT and BERT have demonstrated impressive capabilities in 
    understanding and generating human-like text. These models are trained 
    on massive amounts of text data and can perform a wide variety of tasks 
    including translation, summarization, question answering, and creative writing.
    
    The transformer architecture, introduced in 2017, has been a key innovation 
    enabling these advances. Transformers use self-attention mechanisms to process 
    input sequences in parallel, making them much more efficient than previous 
    recurrent neural network approaches. This has allowed researchers to scale 
    up models to billions of parameters.
    
    However, there are important challenges and concerns. These models require 
    enormous computational resources to train, raising environmental concerns. 
    They can also perpetuate biases present in their training data and sometimes 
    generate false or misleading information. Researchers are actively working 
    on making models more efficient, fair, and reliable.
    """
    
    print("=== SUMMARIZATION TEST ===\n")
    print(f"Original text length: {len(sample_text.split())} words\n")
    
    # Test different summary lengths
    print("--- Short Summary (50 tokens) ---")
    short_summary = summarizer.summarize(sample_text, max_length=50, min_length=20)
    print(short_summary)
    print(f"Length: {len(short_summary.split())} words\n")
    
    print("--- Medium Summary (100 tokens) ---")
    medium_summary = summarizer.summarize(sample_text, max_length=100, min_length=40)
    print(medium_summary)
    print(f"Length: {len(medium_summary.split())} words\n")
