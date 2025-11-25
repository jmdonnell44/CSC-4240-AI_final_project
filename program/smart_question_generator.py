"""
Smart Question Generator Module
Generates high-quality study questions by analyzing sentence patterns.
"""

from typing import List, Tuple
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
            concepts: List of key concepts to anchor question templates
            max_questions: Maximum questions to generate
            
        Returns:
            List of questions
        """
        questions, _ = self.generate_question_answer_pairs(text, concepts, max_questions)
        return questions
    
    def generate_question_answer_pairs(self, text: str, concepts: List[str],
                                       max_questions: int = 15) -> Tuple[List[str], List[str]]:
        """
        Generate aligned question/answer pairs grounded directly in source sentences.
        Prioritizes sentence-based extraction for grammatical accuracy.
        """
        questions: List[str] = []
        answers: List[str] = []
        seen = set()
        seen_answers = set()
        last_subject = ""
        
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 20]
        
        # Primary: derive Q/A directly from sentences
        for sentence in sentences:
            if len(questions) >= max_questions:
                break
            
            pairs, detected_subject = self._extract_question_answer_from_sentence(sentence, last_subject)
            if detected_subject:
                last_subject = detected_subject
            for q, a in pairs:
                q_norm = q.strip()
                if not q_norm:
                    continue
                q_lower = q_norm.lower()
                a_norm = a.strip()
                if q_lower in seen:
                    continue
                a_key = self._answer_key(a_norm)
                if a_key in seen_answers:
                    continue
                questions.append(self._ensure_question_casing(q_norm))
                answers.append(self._ensure_answer_casing(a_norm))
                seen.add(q_lower)
                seen_answers.add(a_key)
                if len(questions) >= max_questions:
                    break
        
        # Secondary: fill gaps with concept-driven Q/A using matched sentences
        if len(questions) < max_questions:
            for concept in concepts:
                if len(questions) >= max_questions:
                    break
                concept_clean = concept.strip().strip('.,;:')
                if not concept_clean or len(concept_clean.split()) > 4:
                    continue  # Skip if empty or too long to be a good concept
                concept_norm = self._normalize_concept_phrase(concept_clean)

                # Validate that the normalized concept makes sense
                if len(concept_norm.split()) == 0 or len(concept_norm) < 3:
                    continue

                match_sentence = self._find_sentence_for_concept(concept_norm, sentences)
                if not match_sentence:
                    continue

                # Extract a clean subject phrase
                subject_phrase = self._extract_subject_from_sentence_for_concept(concept_norm, match_sentence)
                if not subject_phrase or subject_phrase.lower() in ['neural', 'training', 'model']:
                    subject_phrase = concept_norm

                # Validate subject phrase is complete
                if len(subject_phrase.split()) < 2 and subject_phrase.lower() in ['neural', 'training', 'model', 'sigmoid']:
                    continue  # Skip incomplete subjects

                question = self._question_for_subject(subject_phrase)
                q_lower = question.lower()
                if q_lower in seen:
                    continue

                answer_text = self._build_definition_answer(subject_phrase, match_sentence)
                a_key = self._answer_key(answer_text)
                if a_key in seen_answers:
                    continue

                questions.append(self._ensure_question_casing(question))
                answers.append(self._ensure_answer_casing(answer_text))
                seen.add(q_lower)
                seen_answers.add(a_key)
        
        # Trim to requested count
        return questions[:max_questions], answers[:max_questions]
    
    def generate_answers(self, text: str, sentences: List[str], questions: List[str]) -> List[str]:
        """
        Generate concise answers by matching questions to relevant sentences.
        """
        answers = []
        if not text or not questions:
            return answers
        
        # Prepare sentence pool
        sentence_pool = sentences or []
        if not sentence_pool:
            sentence_pool = [s.strip() for s in re.split(r'[.!?]+', text) if len(s.strip()) > 20]
        
        # Simple keyword-based matching
        stopwords = {
            'what', 'why', 'how', 'is', 'are', 'the', 'a', 'an', 'does',
            'do', 'of', 'in', 'for', 'and', 'to', 'on', 'as', 'with', 'used',
            'use', 'you', 'can'
        }
        
        for question in questions:
            # Extract keywords from the question
            keywords = [w.lower() for w in re.findall(r'[A-Za-z]+', question) if len(w) > 2 and w.lower() not in stopwords]
            best_sentence = ""
            best_score = 0
            
            for sentence in sentence_pool:
                sentence_lower = sentence.lower()
                score = sum(1 for kw in keywords if kw in sentence_lower)
                if score > best_score:
                    best_score = score
                    best_sentence = sentence.strip()
            
            if best_sentence:
                answers.append(self._ensure_answer_casing(best_sentence))
            else:
                # Fallback: use first two sentences of the text as a generic answer
                fallback = ' '.join(sentence_pool[:2]).strip() if sentence_pool else text[:200].strip()
                answers.append(self._ensure_answer_casing(fallback))
        
        return answers
    
    def describe_concepts(self, concepts: List[str], sentences: List[str]) -> List[dict]:
        """
        Attach a short description to each concept using the nearest matching sentence.
        """
        descriptions = []
        if not concepts:
            return descriptions

        sentence_pool = sentences or []
        seen = set()
        seen_descriptions = set()
        
        for concept in concepts:
            concept_clean = concept.strip()
            if not concept_clean:
                continue
            concept_clean = self._format_concept_phrase(self._normalize_concept_phrase(concept_clean))
            c_key = concept_clean.lower()

            if c_key in seen:
                continue
            seen.add(c_key)

            match_sentence = self._find_sentence_for_concept(concept_clean, sentence_pool)
            if not match_sentence:
                continue  # Skip concepts without matching sentences instead of generic text

            paraphrased_desc = self._build_concept_statement(concept_clean, match_sentence)

            # Skip empty or invalid descriptions
            if not paraphrased_desc or len(paraphrased_desc.strip()) < 10:
                continue

            desc_key = self._normalize_key(paraphrased_desc)
            if desc_key in seen_descriptions:
                continue
            seen_descriptions.add(desc_key)

            descriptions.append({
                "concept": self._ensure_answer_casing(concept_clean).rstrip('.'),
                "description": paraphrased_desc
            })

        return descriptions
    
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
        
        questions = self._generate_questions_from_sentences(text, num_questions)
        
        print(f"[OK] Generated {len(questions)} questions")
        return questions
    
    def _normalize_concept_phrase(self, phrase: str) -> str:
        """
        Clean and reorder simple concept phrases for grammatical correctness.
        """
        tokens = [t for t in re.findall(r"[A-Za-z']+", phrase) if t]
        tokens = [t for t in tokens if len(t) > 1 or t.isupper()]
        if len(tokens) == 2 and tokens[0].lower() == "learning":
            tokens = [tokens[1], tokens[0]]  # flip "learning supervised" -> "supervised learning"
        # Remove extra spaces and clean up
        normalized = ' '.join(tokens).strip()
        # Fix spacing issues (e.g., "network s" -> "networks")
        normalized = re.sub(r'\b(\w+)\s+s\b', r'\1s', normalized)
        if normalized:
            normalized = normalized[0].upper() + normalized[1:]
        return normalized or phrase.strip()
    
    def _extract_subject_from_sentence_for_concept(self, concept: str, sentence: str) -> str:
        """
        Find the shortest span in a sentence that covers all tokens of the concept.
        """
        concept_tokens = [t.lower() for t in re.findall(r"[A-Za-z']+", concept) if len(t) > 1]
        if not concept_tokens:
            return ""
        
        words = sentence.split()
        lower_words = [w.strip('.,;:').lower() for w in words]
        
        best_span = None
        for start in range(len(words)):
            covered = set()
            for end in range(start, len(words)):
                word_clean = lower_words[end]
                if word_clean in concept_tokens:
                    covered.add(word_clean)
                if len(covered) == len(set(concept_tokens)):
                    span = ' '.join(words[start:end+1]).strip()
                    if not best_span or len(span) < len(best_span):
                        best_span = span
                    break
        return best_span or ""
    
    def _find_sentence_for_concept(self, concept: str, sentences: List[str]) -> str:
        """
        Return the first sentence that mentions the concept (case-insensitive).
        """
        concept_lower = concept.lower()
        tokens = [t for t in re.findall(r'[A-Za-z]+', concept_lower) if len(t) > 2]
        for sentence in sentences:
            if concept_lower in sentence.lower():
                return sentence.strip()
        if tokens:
            for sentence in sentences:
                sl = sentence.lower()
                if all(token in sl for token in tokens):
                    return sentence.strip()
        return ""
    
    def _extract_examples(self, text: str) -> str:
        """Extract example list following 'such as' or similar phrasing."""
        match = re.search(r'such as ([^.;]+)', text, flags=re.IGNORECASE)
        if match:
            examples = match.group(1).strip().rstrip('.')
            return examples
        return ""
    
    def _extract_list_after_colon(self, text: str) -> str:
        """Extract list items following a colon."""
        if ':' in text:
            tail = text.split(':', 1)[1].strip()
            tail = tail.rstrip('.')
            return tail
        return ""
    
    def _extract_question_answer_from_sentence(self, sentence: str, context_subject: str = "") -> Tuple[List[tuple], str]:
        """
        Create (question, answer) pairs directly from a sentence with concise answers.
        Also returns a subject to carry forward for pronoun resolution.
        """
        qa_pairs = []
        sentence_clean = sentence.strip()
        sentence_lower = sentence_clean.lower()
        carry_subject = context_subject

        # General definitions: "X is/are ..."
        definition_match = re.match(
            r'^([A-Za-z][\w\s\-]{2,80}?)\s+(is|are|was|were)\s+(.*)',
            sentence_clean,
            flags=re.IGNORECASE
        )
        if definition_match and not sentence_lower.startswith('there '):
            subject = definition_match.group(1).strip()
            verb = definition_match.group(2).strip()
            predicate = definition_match.group(3).strip().rstrip('.')

            # Skip pronouns without context
            if subject.lower() in {'they', 'it', 'these', 'those', 'this', 'each'}:
                if not context_subject:
                    return qa_pairs, carry_subject  # Skip this sentence
                subject = context_subject

            # Validate subject is meaningful (at least 2 words or proper noun)
            if len(subject.split()) >= 2 or (len(subject.split()) == 1 and subject[0].isupper()):
                carry_subject = subject
                answer = f"{subject} {verb} {predicate}."
                question = self._question_for_subject(subject, verb)
                qa_pairs.append((question, answer))

                if 'focus' in predicate.lower() and len(subject.split()) >= 2:
                    qa_pairs.append((f"What does {subject} focus on?", answer))
                if any(phrase in predicate.lower() for phrase in ['such as', 'including']):
                    examples = self._extract_examples(predicate)
                    if examples:
                        qa_pairs.append((f"What are examples of {subject}?", f"Examples include {examples}."))

        # Categories: "three major categories of X"
        category_match = re.search(
            r'\b(three|four|five|\d+)\s+(?:main\s+|major\s+)?categories of\s+([^:.,]+)',
            sentence_clean,
            flags=re.IGNORECASE
        )
        if category_match:
            number = category_match.group(1)
            topic = category_match.group(2).strip()
            categories_list = self._extract_list_after_colon(sentence_clean)
            answer = categories_list if categories_list else sentence_clean
            qa_pairs.append((f"What are the {number} categories of {topic}?", self._ensure_answer_casing(answer)))

        # Usage: "X uses Y"
        usage_match = re.match(
            r'^([A-Za-z][\w\s\-]{2,80}?) uses ([^.,;]+)',
            sentence_clean,
            flags=re.IGNORECASE
        )
        if usage_match:
            subject = usage_match.group(1).strip()
            obj = usage_match.group(2).strip()
            if subject.lower() in {'they', 'it', 'these', 'those', 'this', 'each'}:
                if not context_subject:
                    return qa_pairs, carry_subject
                subject = context_subject
            if len(subject.split()) >= 2:
                qa_pairs.append((self._question_for_subject(subject), f"{subject} uses {obj}."))
                carry_subject = subject

        # Foundation: "X is based on Y"
        based_match = re.match(
            r'^([A-Za-z][\w\s\-]{2,80}?) is based on ([^.,;]+)',
            sentence_clean,
            flags=re.IGNORECASE
        )
        if based_match:
            subject = based_match.group(1).strip()
            foundation = based_match.group(2).strip()
            if subject.lower() in {'they', 'it', 'these', 'those', 'this', 'each'}:
                if not context_subject:
                    return qa_pairs, carry_subject
                subject = context_subject
            if len(subject.split()) >= 2:
                qa_pairs.append((self._question_for_subject(subject), f"{subject} is based on {foundation}."))
                carry_subject = subject

        # Examples: "X ... such as A, B, and C"
        if 'such as' in sentence_lower:
            subject = self._subject_before_such_as(sentence_clean) or context_subject
            examples = self._extract_examples(sentence_clean)
            if subject and examples and len(subject.split()) >= 2:
                qa_pairs.append((f"What are examples of {subject}?", f"Examples include {examples}."))

        # Begins with pattern: "X begins with Y"
        begins_match = re.match(
            r'^([A-Za-z][\w\s\-]{2,80}?) begins with ([^.,;]+)',
            sentence_clean,
            flags=re.IGNORECASE
        )
        if begins_match:
            subject = begins_match.group(1).strip()
            remainder = begins_match.group(2).strip()
            if subject.lower() in {'they', 'it', 'these', 'those', 'this', 'each'}:
                subject = context_subject or subject
            if subject and len(subject.split()) >= 1:
                qa_pairs.append((f"What does {subject} begin with?", self._ensure_answer_casing(f"{subject} begins with {remainder}.")))
                carry_subject = subject
        
        return qa_pairs, carry_subject
    
    def _ensure_question_casing(self, question: str) -> str:
        """Ensure questions are capitalized and end with a question mark."""
        q = question.strip()
        if not q.endswith('?'):
            q += '?'
        if q and q[0].islower():
            q = q[0].upper() + q[1:]
        return q
    
    def _ensure_answer_casing(self, answer: str) -> str:
        """Ensure answers start with a capital letter and end with a period."""
        if not answer:
            return "Answer unavailable."
        a = answer.strip()

        # Fix common grammar mistakes from paraphrasing
        a = re.sub(r'\bare consist of\b', 'consist of', a, flags=re.IGNORECASE)
        a = re.sub(r'\bAre consist of\b', 'Consist of', a)

        if a and a[0].islower():
            a = a[0].upper() + a[1:]
        if not a.endswith('.'):
            a += '.'
        return a
    
    def _answer_key(self, answer: str) -> str:
        """Create a normalized key for answer de-duplication."""
        return re.sub(r'\s+', ' ', answer.strip().lower().rstrip('.'))
    
    def _paraphrase_concept_description(self, concept: str, sentence: str, variant_index: int) -> str:
        """Paraphrase concept descriptions to avoid copying exact source wording."""
        core = sentence.strip().rstrip('.')
        if not core:
            core = f"{concept} is discussed in the text"
        core_lower = core[0].lower() + core[1:] if len(core) > 1 else core.lower()
        templates = [
            "{concept} refers to {c}.",
            "{concept} involves {c}.",
            "{concept} is about {c}.",
            "{concept} covers {c}.",
            "{concept} relates to {c}."
        ]
        if variant_index < len(templates):
            template = templates[variant_index]
            paraphrased = template.format(concept=concept, c=core_lower).strip()
        else:
            paraphrased = f"{concept} - {core_lower}."
        return self._ensure_answer_casing(paraphrased)
    
    def _format_concept_phrase(self, phrase: str) -> str:
        """Normalize concept phrasing and remove repeated words."""
        tokens = [t for t in re.findall(r"[A-Za-z']+", phrase) if t]
        cleaned = []
        seen = set()
        for t in tokens:
            t_low = t.lower()
            base = t_low.rstrip('s')
            if t_low in seen or base in seen or (base + 's') in seen:
                continue
            seen.add(t_low)
            cleaned.append(t)
        formatted = ' '.join(cleaned).strip()
        # Fix spacing issues
        formatted = re.sub(r'\b(\w+)\s+s\b', r'\1s', formatted)
        if formatted:
            formatted = formatted[0].upper() + formatted[1:]
        return formatted

    def _normalize_key(self, text: str) -> str:
        """Normalize text for strict deduplication (lowercase, strip punctuation, collapse spaces)."""
        cleaned = re.sub(r'[^\w\s]', ' ', text.lower())
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned
    
    def _build_concept_statement(self, concept: str, sentence: str) -> str:
        """Create a clean, single-sentence concept statement without repeated wording."""
        concept_norm = self._format_concept_phrase(concept)
        sentence_clean = sentence.strip().rstrip('.')

        if not sentence_clean:
            return self._ensure_answer_casing(f"{concept_norm} is an important concept in this material")

        sentence_lower = sentence_clean.lower()
        concept_lower = concept_norm.lower()

        # If the sentence already starts with the concept, use it directly with light paraphrasing
        if sentence_lower.startswith(concept_lower):
            # Extract the part after the concept
            remainder = sentence_clean[len(concept_norm):].lstrip(" ,.-")

            # Check if it starts with a verb we can paraphrase
            if remainder.lower().startswith('is '):
                content = remainder[3:].strip()
                content = self._paraphrase_content(content)
                return self._ensure_answer_casing(f"{concept_norm} refers to {content}")
            elif remainder.lower().startswith('are '):
                content = remainder[4:].strip()
                original_content = content
                content = self._paraphrase_content(content)
                # Fix grammar: if paraphrasing changed "composed of" to "consist of", don't add "are"
                # because "They consist of" is correct, not "They are consist of"
                if original_content.lower().startswith('composed of') or original_content.lower().startswith('made up of'):
                    # The verb form changed, so don't add "are"
                    return self._ensure_answer_casing(f"{concept_norm} {content}")
                else:
                    # Normal case: keep "are"
                    return self._ensure_answer_casing(f"{concept_norm} are {content}")
            elif remainder.lower().startswith('involves '):
                content = remainder[9:].strip()
                content = self._paraphrase_content(content)
                return self._ensure_answer_casing(f"{concept_norm} encompasses {content}")
            else:
                # Paraphrase the full sentence
                paraphrased = self._paraphrase_content(sentence_clean)
                return self._ensure_answer_casing(paraphrased)

        # If the concept appears in the sentence, try to extract a complete definition
        concept_pattern = re.escape(concept_lower)
        match = re.search(rf'\b{concept_pattern}[^.]*?(is|are)\s+([^.]+)', sentence_lower)
        if match:
            verb = match.group(1)
            definition = sentence_clean[match.start(2):].strip().rstrip('.')
            definition = self._paraphrase_content(definition)

            # Paraphrase the verb
            verb_map = {'is': 'refers to', 'are': 'refer to'}
            paraphrased_verb = verb_map.get(verb, verb)

            return self._ensure_answer_casing(f"{concept_norm} {paraphrased_verb} {definition}")

        # Try to find if the concept is the subject of a sentence pattern
        # Look for patterns like "X is Y" or "X involves Y"
        for verb_phrase in ['is a', 'is an', 'is the', 'are', 'involves', 'includes', 'refers to', 'uses']:
            if f" {verb_phrase} " in sentence_lower:
                # Check if concept is before this verb
                parts = sentence_lower.split(f" {verb_phrase} ", 1)
                if concept_lower in parts[0]:
                    # Extract just the definition part
                    definition = sentence_clean.split(f" {verb_phrase} ", 1)[1].strip()
                    definition = self._paraphrase_content(definition)

                    # Paraphrase the verb phrase
                    paraphrase_map = {
                        'is a': 'represents a',
                        'is an': 'represents an',
                        'is the': 'represents the',
                        'are': 'are described as',
                        'involves': 'encompasses',
                        'includes': 'contains',
                        'refers to': 'relates to',
                        'uses': 'utilizes'
                    }
                    paraphrased = paraphrase_map.get(verb_phrase, verb_phrase)

                    return self._ensure_answer_casing(f"{concept_norm} {paraphrased} {definition}")

        # If concept is in the sentence but no clear pattern, use the full sentence with paraphrasing
        if concept_lower in sentence_lower:
            paraphrased = self._paraphrase_content(sentence_clean)
            return self._ensure_answer_casing(paraphrased)

        # Last resort: skip this concept
        return ""

    def _paraphrase_content(self, text: str) -> str:
        """Apply paraphrasing rules to avoid verbatim copying."""
        if not text:
            return text

        # Dictionary of word/phrase substitutions
        substitutions = {
            r'\bcomposed of\b': 'consist of',
            r'\bmade up of\b': 'consist of',
            r'\binspired by\b': 'based on',
            r'\bincludes\b': 'contains',
            r'\binvolves\b': 'requires',
            r'\ballowing them to\b': 'which enables them to',
            r'\bcomes from\b': 'originates from',
            r'\bwidely used in\b': 'commonly applied to',
            r'\bmeasures\b': 'quantifies',
            r'\breducing\b': 'minimizing',
            r'\bimproving\b': 'enhancing',
            r'\bapplies\b': 'uses',
            r'\breceives\b': 'takes',
            r'\bpasses\b': 'sends',
            r'\badjusting\b': 'modifying',
            r'\bhas enabled\b': 'has facilitated',
            r'\brefers to\b': 'describes'
        }

        result = text
        for pattern, replacement in substitutions.items():
            result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)

        return result

    def _subject_before_such_as(self, sentence: str) -> str:
        """Extract a likely subject immediately before 'such as'."""
        idx = sentence.lower().find('such as')
        if idx == -1:
            return ""
        prefix = sentence[:idx].strip()
        words = prefix.split()
        if not words:
            return ""
        tail_words = words[-4:] if len(words) >= 1 else words
        subject = ' '.join(tail_words).strip(' ,.')
        return self._format_concept_phrase(subject) or subject
    
    def _question_for_subject(self, subject: str, verb: str = "is") -> str:
        """Return a grammatically correct 'What is/are ...?' question."""
        subj = subject.strip()
        # Clean up the subject to avoid incomplete phrases
        subj = re.sub(r'\b(neural|training|model|sigmoid)\s*$', lambda m: m.group(1) + ' networks', subj, flags=re.IGNORECASE)
        subj = subj.rstrip('?.!')

        is_plural = subj.lower().endswith('s') and not subj.lower().endswith('ss')
        helper = "are" if verb.lower() in {"are", "were"} or is_plural else "is"
        return f"What {helper} {subj}?"
    
    def _build_definition_answer(self, subject: str, sentence: str) -> str:
        """Build a concise answer using the subject and the matched sentence."""
        sentence_clean = sentence.strip().rstrip('.')
        subject_clean = subject.strip().rstrip('.,;:')

        # If the sentence already starts with the subject, use it directly
        if sentence_clean.lower().startswith(subject_clean.lower()):
            return self._ensure_answer_casing(sentence_clean)

        # Try to extract relevant part from the sentence
        # Look for "is/are" patterns and extract the definition part
        match = re.search(rf'{re.escape(subject_clean)}.*?(is|are)\s+(.+)', sentence_clean, re.IGNORECASE)
        if match:
            verb = match.group(1)
            definition = match.group(2).strip()
            return self._ensure_answer_casing(f"{subject_clean} {verb} {definition}")

        # If the subject is mentioned in the sentence, try to extract context around it
        if subject_clean.lower() in sentence_clean.lower():
            return self._ensure_answer_casing(sentence_clean)

        # Default: combine subject and sentence
        return self._ensure_answer_casing(f"{subject_clean}: {sentence_clean}")
    
    def _generate_questions_from_sentences(self, text: str, max_questions: int,
                                           existing_questions: List[str] = None) -> List[str]:
        """
        Generate questions from sentence patterns, respecting existing questions.
        """
        questions = []
        existing = existing_questions or []
        seen_questions = {q.lower() for q in existing if isinstance(q, str)}
        
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        base_count = len(existing)
        
        for sentence in sentences:
            if base_count + len(questions) >= max_questions:
                break
            
            new_questions = self._extract_questions_from_sentence(sentence)
            
            for q in new_questions:
                if not q:
                    continue
                
                q_lower = q.lower()
                if q_lower in seen_questions:
                    continue
                
                questions.append(self._ensure_question_casing(q))
                seen_questions.add(q_lower)
                
                if base_count + len(questions) >= max_questions:
                    break
        
        return questions
    
    def _extract_questions_from_sentence(self, sentence: str) -> List[str]:
        """Extract multiple possible questions from a sentence."""
        questions = []
        sentence_clean = sentence.strip()
        sentence_lower = sentence_clean.lower()

        # General definitions: "X is/are ..."
        definition_match = re.match(
            r'^([A-Za-z][\w\s\-]{2,80}?)\s+(is|are|was|were)\s+(.*)',
            sentence_clean,
            flags=re.IGNORECASE
        )
        if definition_match and not sentence_lower.startswith('there '):
            subject = definition_match.group(1).strip()
            predicate = definition_match.group(3).strip().rstrip('.')

            # Skip pronouns and ensure meaningful subjects
            if subject.lower() in {'they', 'it', 'these', 'those', 'this', 'each'}:
                return questions

            # Only generate questions for subjects with at least 2 words or proper nouns
            if len(subject.split()) >= 2 or (len(subject.split()) == 1 and subject[0].isupper()):
                questions.append(f"What is {subject}?")

                predicate_lower = predicate.lower()
                if 'focus' in predicate_lower and len(subject.split()) >= 2:
                    questions.append(f"What does {subject} focus on?")
                if 'based on' in predicate_lower:
                    questions.append(f"What is {subject} based on?")
                if any(phrase in predicate_lower for phrase in ['used in', 'used for', 'used to']):
                    questions.append(f"How is {subject} used?")
                if any(phrase in predicate_lower for phrase in ['such as', 'including']):
                    questions.append(f"What are examples of {subject}?")
        
        # Categories: "three major categories of X"
        category_match = re.search(
            r'\b(three|four|five|\d+)\s+(?:main\s+|major\s+)?categories of\s+([^:.,]+)',
            sentence_clean,
            flags=re.IGNORECASE
        )
        if category_match:
            number = category_match.group(1)
            topic = category_match.group(2).strip()
            questions.append(f"What are the {number} categories of {topic}?")
        
        # Usage: "X uses Y"
        usage_match = re.match(
            r'^([A-Za-z][\w\s\-]{2,80}?) uses ([^.,;]+)',
            sentence_clean,
            flags=re.IGNORECASE
        )
        if usage_match:
            subject = usage_match.group(1).strip()
            obj = usage_match.group(2).strip()
            questions.append(f"What does {subject} use?")
            questions.append(f"Why does {subject} use {obj}?")
        
        # Foundation: "X is based on Y"
        based_match = re.match(
            r'^([A-Za-z][\w\s\-]{2,80}?) is based on ([^.,;]+)',
            sentence_clean,
            flags=re.IGNORECASE
        )
        if based_match:
            subject = based_match.group(1).strip()
            foundation = based_match.group(2).strip()
            questions.append(f"What is {subject} based on?")
            questions.append(f"How does {subject} work?")
            if foundation:
                questions.append(f"Why does {subject} rely on {foundation}?")
        
        # Examples: "X ... such as A, B, and C"
        if 'such as' in sentence_lower:
            prefix_match = re.match(
                r'^([A-Za-z][\w\s\-]{2,80}?) .*such as ',
                sentence_clean,
                flags=re.IGNORECASE
            )
            if prefix_match:
                subject = prefix_match.group(1).strip()
                questions.append(f"What are examples of {subject}?")
        
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
