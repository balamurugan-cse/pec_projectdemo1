"""
Confidence Scorer Module

Calculates and manages confidence levels for verification results.
Provides transparent scoring based on multiple factors.
"""

from typing import Dict, Any, List
import math


class ConfidenceScorer:
    """
    Calculates confidence scores for verification results.
    """

    def __init__(self):
        """Initialize the confidence scorer."""
        self.weights = {
            'evidence_quality': 0.35,
            'evidence_quantity': 0.15,
            'source_reliability': 0.25,
            'claim_clarity': 0.15,
            'cross_validation': 0.10,
        }

    def calculate_confidence(
        self,
        verification_result: Dict[str, Any],
        claim_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive confidence score for verification result.

        Args:
            verification_result: The verification result to score
            claim_data: Optional additional claim data

        Returns:
            Dictionary with confidence score and breakdown
        """
        evidence = verification_result.get('evidence', [])
        ambiguity = verification_result.get('ambiguity_score', 0.5)
        bias_indicators = verification_result.get('bias_indicators', [])

        # Calculate component scores
        evidence_quality_score = self._score_evidence_quality(evidence)
        evidence_quantity_score = self._score_evidence_quantity(evidence)
        source_reliability_score = self._score_source_reliability(evidence)
        claim_clarity_score = 1.0 - ambiguity  # Inverse of ambiguity
        cross_validation_score = self._score_cross_validation(evidence)

        # Apply bias penalty
        bias_penalty = len(bias_indicators) * 0.05

        # Calculate weighted confidence
        confidence = (
            self.weights['evidence_quality'] * evidence_quality_score +
            self.weights['evidence_quantity'] * evidence_quantity_score +
            self.weights['source_reliability'] * source_reliability_score +
            self.weights['claim_clarity'] * claim_clarity_score +
            self.weights['cross_validation'] * cross_validation_score
        )

        # Apply bias penalty
        confidence = max(0.0, confidence - bias_penalty)

        # Determine confidence level category
        confidence_level = self._categorize_confidence(confidence)

        return {
            'confidence_score': round(confidence, 3),
            'confidence_level': confidence_level,
            'breakdown': {
                'evidence_quality': round(evidence_quality_score, 3),
                'evidence_quantity': round(evidence_quantity_score, 3),
                'source_reliability': round(source_reliability_score, 3),
                'claim_clarity': round(claim_clarity_score, 3),
                'cross_validation': round(cross_validation_score, 3),
                'bias_penalty': round(bias_penalty, 3),
            },
            'interpretation': self._interpret_confidence(confidence_level),
        }

    def _score_evidence_quality(self, evidence: List[Dict[str, Any]]) -> float:
        """Score the quality of evidence."""
        if not evidence or evidence[0].get('source') == 'none':
            return 0.0

        # Average relevance of evidence
        relevances = [e.get('relevance', 0.0) for e in evidence if e.get('relevance')]
        if not relevances:
            return 0.3

        return sum(relevances) / len(relevances)

    def _score_evidence_quantity(self, evidence: List[Dict[str, Any]]) -> float:
        """Score based on amount of evidence."""
        if not evidence or evidence[0].get('source') == 'none':
            return 0.0

        valid_evidence_count = len([e for e in evidence if e.get('relevance', 0) > 0.5])

        # Logarithmic scaling: more evidence helps but with diminishing returns
        if valid_evidence_count == 0:
            return 0.0
        elif valid_evidence_count == 1:
            return 0.5
        else:
            # Cap at 1.0
            return min(1.0, 0.5 + 0.2 * math.log(valid_evidence_count))

    def _score_source_reliability(self, evidence: List[Dict[str, Any]]) -> float:
        """Score based on reliability of sources."""
        if not evidence or evidence[0].get('source') == 'none':
            return 0.0

        reliabilities = [e.get('reliability', 0.5) for e in evidence]
        if not reliabilities:
            return 0.5

        return sum(reliabilities) / len(reliabilities)

    def _score_cross_validation(self, evidence: List[Dict[str, Any]]) -> float:
        """Score based on cross-validation across multiple sources."""
        if not evidence or evidence[0].get('source') == 'none':
            return 0.0

        # Check if we have multiple independent sources
        sources = set(e.get('source', '') for e in evidence)
        unique_sources = len(sources)

        if unique_sources <= 1:
            return 0.3
        elif unique_sources == 2:
            return 0.7
        else:
            return 1.0

    def _categorize_confidence(self, score: float) -> str:
        """Categorize confidence score into levels."""
        if score >= 0.85:
            return 'very_high'
        elif score >= 0.70:
            return 'high'
        elif score >= 0.50:
            return 'medium'
        elif score >= 0.30:
            return 'low'
        else:
            return 'very_low'

    def _interpret_confidence(self, level: str) -> str:
        """Provide human-readable interpretation of confidence level."""
        interpretations = {
            'very_high': 'Strong evidence supports the verification result with minimal uncertainty',
            'high': 'Good evidence supports the verification result with minor limitations',
            'medium': 'Moderate evidence available; result should be viewed with some caution',
            'low': 'Limited evidence available; significant uncertainty in verification',
            'very_low': 'Insufficient evidence for reliable verification; result highly uncertain',
        }
        return interpretations.get(level, 'Unknown confidence level')
