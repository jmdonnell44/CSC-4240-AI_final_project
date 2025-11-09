"""
Concept Extractor Module
Extracts key concepts and keywords using spaCy NER and KeyBERT.
"""

from typing import List, Dict, Tuple
import warnings
warnings.filterwarnings('ignore')


class ConceptExtractor:
    """Extract key concepts using spaCy and KeyBERT."""
    
    def __init__(self):
        """Initialize the ConceptExtractor with spaCy and KeyBERT models."""
        self.nlp = None
        self.keybert_model = None
        self._load_models()
    
    def _load_models(self):
        """Load spaCy and KeyBERT models."""
        try:
            import spacy
            print("Loading spaCy model...")
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                print("Downloading spaCy model (this happens once)...")
                import os
                os.system("python -m spacy download en_core_web_sm")
                self.nlp = spacy.load("en_core_web_sm")
            print("✓ spaCy model loaded")
        except Exception as e:
            print(f"Warning: Could not load spaCy: {e}")
        
        try:
            from keybert import KeyBERT
            print("Loading KeyBERT model...")
            self.keybert_model = KeyBERT()
            print("✓ KeyBERT model loaded")
        except Exception as e:
            print(f"Warning: Could not load KeyBERT: {e}")
    
    def extract_named_entities(self, text: str) -> List[Dict[str, str]]:
        """
        Extract named entities using spaCy.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of dictionaries with entity text and label
        """
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "description": spacy.explain(ent.label_)
            })
        
        return entities
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Extract keywords using KeyBERT.
        
        Args:
            text: Text to analyze
            top_n: Number of keywords to extract
            
        Returns:
            List of (keyword, score) tuples
        """
        if not self.keybert_model:
            return []
        
        try:
            keywords = self.keybert_model.extract_keywords(
                text,
                keyphrase_ngram_range=(1, 2),
                stop_words='english',
                top_n=top_n,
                diversity=0.5  # Ensures diverse keywords
            )
            return keywords
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return []
    
    def extract_noun_phrases(self, text: str) -> List[str]:
        """
        Extract noun phrases using spaCy.
        
        Args:
            text: Text to analyze
            
        Returns:
            List of noun phrases
        """
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        noun_phrases = [chunk.text for chunk in doc.noun_chunks]
        
        # Remove duplicates while preserving order
        seen = set()
        unique_phrases = []
        for phrase in noun_phrases:
            phrase_lower = phrase.lower()
            if phrase_lower not in seen and len(phrase.split()) > 1:  # Multi-word phrases
                seen.add(phrase_lower)
                unique_phrases.append(phrase)
        
        return unique_phrases
    
    def extract_all_concepts(self, text: str, top_keywords: int = 15) -> Dict:
        """
        Extract all types of concepts from text.
        
        Args:
            text: Text to analyze
            top_keywords: Number of top keywords to extract
            
        Returns:
            Dictionary with all extracted concepts
        """
        print("Extracting concepts...")
        
        # Extract named entities
        entities = self.extract_named_entities(text)
        print(f"✓ Found {len(entities)} named entities")
        
        # Extract keywords
        keywords = self.extract_keywords(text, top_n=top_keywords)
        print(f"✓ Extracted {len(keywords)} keywords")
        
        # Extract noun phrases
        noun_phrases = self.extract_noun_phrases(text)
        print(f"✓ Found {len(noun_phrases)} noun phrases")
        
        # Combine and deduplicate
        all_concepts = set()
        
        # Add entity texts
        for ent in entities:
            all_concepts.add(ent['text'].lower())
        
        # Add keywords
        for kw, score in keywords:
            all_concepts.add(kw.lower())
        
        # Add top noun phrases
        for phrase in noun_phrases[:20]:  # Limit to top 20
            all_concepts.add(phrase.lower())
        
        return {
            "named_entities": entities,
            "keywords": keywords,
            "noun_phrases": noun_phrases[:20],
            "all_concepts": sorted(list(all_concepts)),
            "total_unique_concepts": len(all_concepts)
        }
    
    def get_important_concepts(self, text: str, top_n: int = 10) -> List[str]:
        """
        Get the most important concepts (simplified for question generation).
        
        Args:
            text: Text to analyze
            top_n: Number of concepts to return
            
        Returns:
            List of important concept strings
        """
        concepts = self.extract_all_concepts(text, top_keywords=top_n)
        
        # Prioritize keywords (they have scores)
        important = [kw for kw, score in concepts['keywords'][:top_n]]
        
        return important


if __name__ == "__main__":
    # Test the concept extractor
    extractor = ConceptExtractor()
    
    sample_text = """
    Machine learning is a subset of artificial intelligence that focuses on 
    building systems that learn from data. Neural networks, particularly deep 
    learning models, have revolutionized computer vision and natural language 
    processing. Companies like Google, OpenAI, and Meta are leading research 
    in this field. Popular frameworks include TensorFlow and PyTorch.
    
    The transformer architecture, introduced in 2017, has become the foundation 
    for large language models. GPT and BERT are examples of transformer-based models.
    """
    
    print("=== CONCEPT EXTRACTION TEST ===\n")
    
    concepts = extractor.extract_all_concepts(sample_text)
    
    print("\n--- Named Entities ---")
    for ent in concepts['named_entities'][:5]:
        print(f"  • {ent['text']} ({ent['label']})")
    
    print("\n--- Keywords ---")
    for kw, score in concepts['keywords'][:5]:
        print(f"  • {kw} (score: {score:.3f})")
    
    print("\n--- Noun Phrases ---")
    for phrase in concepts['noun_phrases'][:5]:
        print(f"  • {phrase}")
    
    print(f"\n--- Summary ---")
    print(f"Total unique concepts: {concepts['total_unique_concepts']}")
    
    print("\n--- Important Concepts (for questions) ---")
    important = extractor.get_important_concepts(sample_text, top_n=5)
    for concept in important:
        print(f"  • {concept}")
