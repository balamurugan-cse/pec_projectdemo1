"""
Claim Analyzer Module

Analyzes textual claims within context to identify key assertions,
extract factual statements, and prepare them for verification.
"""

import re
from typing import List, Dict, Any
from datetime import datetime


class ClaimAnalyzer:
    """
    Analyzes textual content to extract and structure claims for verification.
    """

    def __init__(self):
        """Initialize the claim analyzer."""
        self.claim_patterns = [
            r'\b(is|are|was|were|will be|has been)\b',  # State of being
            r'\b(always|never|every|all|none)\b',  # Absolute statements
            r'\b(\d+\.?\d*%?|\d+\.?\d*\s*(million|billion|thousand))\b',  # Statistics
            r'\b(proven|confirmed|debunked|false|true)\b',  # Verification language
        ]

    def analyze(self, content: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Analyze content to extract claims and metadata.

        Args:
            content: The textual content to analyze
            context: Optional context information (source, timestamp, etc.)

        Returns:
            Dictionary containing extracted claims and analysis metadata
        """
        if not content or not isinstance(content, str):
            return {
                'status': 'error',
                'message': 'Invalid or empty content provided',
                'claims': []
            }

        # Split content into sentences
        sentences = self._split_into_sentences(content)

        # Extract claims from sentences
        claims = []
        for idx, sentence in enumerate(sentences):
            claim_score = self._calculate_claim_score(sentence)

            if claim_score > 0.3:  # Threshold for considering as a claim
                claims.append({
                    'id': f'claim_{idx}',
                    'text': sentence.strip(),
                    'claim_score': claim_score,
                    'position': idx,
                    'contains_statistics': self._contains_statistics(sentence),
                    'contains_absolutes': self._contains_absolutes(sentence),
                    'extracted_entities': self._extract_entities(sentence),
                })

        return {
            'status': 'success',
            'content_length': len(content),
            'sentence_count': len(sentences),
            'claims_identified': len(claims),
            'claims': claims,
            'context': context or {},
            'analyzed_at': datetime.now().isoformat(),
        }

    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting (can be enhanced with NLP libraries)
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

    def _calculate_claim_score(self, sentence: str) -> float:
        """
        Calculate a score indicating likelihood of being a factual claim.
        Higher score means more likely to be a verifiable claim.
        """
        score = 0.0
        sentence_lower = sentence.lower()

        # Check for claim patterns
        for pattern in self.claim_patterns:
            if re.search(pattern, sentence_lower):
                score += 0.25

        # Boost for specific claim indicators
        if self._contains_statistics(sentence):
            score += 0.3

        if self._contains_absolutes(sentence):
            score += 0.2

        # Questions are less likely to be claims
        if sentence.strip().endswith('?'):
            score *= 0.5

        return min(score, 1.0)

    def _contains_statistics(self, text: str) -> bool:
        """Check if text contains statistical data."""
        return bool(re.search(r'\b\d+\.?\d*%?|\d+\.?\d*\s*(million|billion|thousand)\b', text))

    def _contains_absolutes(self, text: str) -> bool:
        """Check if text contains absolute statements."""
        absolutes = ['always', 'never', 'every', 'all', 'none', 'no one', 'everyone']
        text_lower = text.lower()
        return any(absolute in text_lower for absolute in absolutes)

    def _extract_entities(self, text: str) -> List[str]:
        """
        Extract named entities from text (simplified version).
        In production, would use NLP libraries like spaCy.
        """
        # Simple capitalized word extraction as placeholder
        words = text.split()
        entities = []

        for word in words:
            # Check if word starts with capital letter and is not at sentence start
            cleaned = word.strip('.,!?;:')
            if cleaned and cleaned[0].isupper() and len(cleaned) > 1:
                entities.append(cleaned)

        return list(set(entities))
