"""
Verification Engine Module

Evaluates claims against evidence sources and determines reliability.
Handles ambiguity, conflicting information, and incomplete context.
"""

from typing import List, Dict, Any, Tuple
from datetime import datetime
import re


class VerificationEngine:
    """
    Verifies claims using evidence-based analysis and evaluation.
    """

    # Predefined knowledge base (in production, would connect to external APIs)
    KNOWLEDGE_BASE = {
        'earth': {
            'facts': ['round', 'spherical', 'planet', 'orbits sun'],
            'confidence': 1.0,
        },
        'water': {
            'facts': ['boils at 100 celsius', 'freezes at 0 celsius', 'h2o'],
            'confidence': 1.0,
        },
        'covid': {
            'facts': ['pandemic started 2019', 'caused by coronavirus', 'vaccines developed'],
            'confidence': 0.95,
        },
    }

    def __init__(self):
        """Initialize the verification engine."""
        self.evidence_sources = []
        self.verification_history = []

    def verify_claim(self, claim: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify a single claim against available evidence.

        Args:
            claim: Dictionary containing claim text and metadata

        Returns:
            Verification result with verdict, evidence, and confidence
        """
        claim_text = claim.get('text', '').lower()

        # Search for relevant evidence
        evidence = self._gather_evidence(claim_text)

        # Evaluate claim against evidence
        verdict, confidence = self._evaluate_claim(claim_text, evidence)

        # Check for ambiguity and bias
        ambiguity_score = self._detect_ambiguity(claim_text)
        bias_indicators = self._detect_bias(claim_text)

        result = {
            'claim_id': claim.get('id'),
            'claim_text': claim.get('text'),
            'verdict': verdict,
            'confidence': confidence,
            'evidence': evidence,
            'ambiguity_score': ambiguity_score,
            'bias_indicators': bias_indicators,
            'verified_at': datetime.now().isoformat(),
            'limitations': self._identify_limitations(claim_text, evidence),
        }

        self.verification_history.append(result)
        return result

    def verify_claims(self, claims: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Verify multiple claims.

        Args:
            claims: List of claim dictionaries

        Returns:
            List of verification results
        """
        return [self.verify_claim(claim) for claim in claims]

    def _gather_evidence(self, claim_text: str) -> List[Dict[str, Any]]:
        """
        Gather evidence related to the claim.
        In production, would query external fact-checking APIs and databases.
        """
        evidence = []

        # Search knowledge base
        for topic, info in self.KNOWLEDGE_BASE.items():
            if topic in claim_text:
                for fact in info['facts']:
                    if fact in claim_text:
                        evidence.append({
                            'source': 'knowledge_base',
                            'topic': topic,
                            'content': fact,
                            'relevance': 0.9,
                            'reliability': info['confidence'],
                        })

        # If no direct evidence found, mark as unverifiable
        if not evidence:
            evidence.append({
                'source': 'none',
                'content': 'No direct evidence found in available sources',
                'relevance': 0.0,
                'reliability': 0.0,
            })

        return evidence

    def _evaluate_claim(
        self, claim_text: str, evidence: List[Dict[str, Any]]
    ) -> Tuple[str, float]:
        """
        Evaluate claim against evidence to determine verdict and confidence.

        Returns:
            Tuple of (verdict, confidence) where verdict is one of:
            - 'accurate': Claim is supported by evidence
            - 'misleading': Claim is partially true but missing context
            - 'false': Claim contradicts evidence
            - 'unverifiable': Insufficient evidence to verify
        """
        if not evidence or evidence[0]['source'] == 'none':
            return 'unverifiable', 0.1

        # Analyze evidence support
        supporting_evidence = []
        contradicting_evidence = []

        for ev in evidence:
            if ev['relevance'] > 0.7:
                supporting_evidence.append(ev)

        # Check for absolute claims which are often misleading
        has_absolutes = bool(re.search(
            r'\b(always|never|every|all|none|100%|zero|impossible)\b',
            claim_text
        ))

        # Determine verdict
        if supporting_evidence:
            avg_reliability = sum(e['reliability'] for e in supporting_evidence) / len(supporting_evidence)

            if has_absolutes:
                # Absolute claims require very high evidence
                if avg_reliability > 0.95:
                    return 'accurate', avg_reliability * 0.9
                else:
                    return 'misleading', avg_reliability * 0.7

            if avg_reliability > 0.8:
                return 'accurate', avg_reliability
            elif avg_reliability > 0.5:
                return 'partially_accurate', avg_reliability * 0.8
            else:
                return 'misleading', avg_reliability * 0.6

        return 'unverifiable', 0.2

    def _detect_ambiguity(self, text: str) -> float:
        """
        Detect ambiguity in claim text.
        Returns score from 0 (clear) to 1 (highly ambiguous).
        """
        ambiguity_score = 0.0

        # Vague quantifiers
        vague_terms = ['some', 'many', 'few', 'several', 'often', 'rarely', 'might', 'could', 'may']
        for term in vague_terms:
            if term in text.lower():
                ambiguity_score += 0.1

        # Pronouns without clear antecedents
        pronouns = ['it', 'they', 'them', 'this', 'that', 'these']
        for pronoun in pronouns:
            if f' {pronoun} ' in f' {text.lower()} ':
                ambiguity_score += 0.05

        return min(ambiguity_score, 1.0)

    def _detect_bias(self, text: str) -> List[str]:
        """
        Detect potential bias indicators in text.
        """
        bias_indicators = []
        text_lower = text.lower()

        # Emotional language
        emotional_words = ['shocking', 'amazing', 'terrible', 'outrageous', 'incredible']
        if any(word in text_lower for word in emotional_words):
            bias_indicators.append('emotional_language')

        # Loaded terms
        loaded_terms = ['radical', 'extreme', 'militant', 'fanatic']
        if any(term in text_lower for term in loaded_terms):
            bias_indicators.append('loaded_terminology')

        # Absolute statements
        if re.search(r'\b(always|never|all|none)\b', text_lower):
            bias_indicators.append('absolute_statements')

        # Unattributed claims
        if not re.search(r'\b(according to|study|research|report|said)\b', text_lower):
            if not re.search(r'\b(I|we|my opinion)\b', text_lower):
                bias_indicators.append('unattributed_claim')

        return bias_indicators

    def _identify_limitations(
        self, claim_text: str, evidence: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Identify limitations in the verification process.
        """
        limitations = []

        if not evidence or evidence[0]['source'] == 'none':
            limitations.append('Limited evidence sources available')

        if len(evidence) < 2:
            limitations.append('Single source of evidence - requires corroboration')

        if any(e.get('reliability', 0) < 0.7 for e in evidence):
            limitations.append('Some evidence sources have lower reliability')

        if len(claim_text.split()) < 5:
            limitations.append('Claim is very short - may lack necessary context')

        return limitations
