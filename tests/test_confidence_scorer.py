"""
Tests for Confidence Scorer Module
"""

import unittest
from misinformation_platform.confidence_scorer import ConfidenceScorer


class TestConfidenceScorer(unittest.TestCase):
    """Test cases for ConfidenceScorer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.scorer = ConfidenceScorer()

    def test_calculate_confidence_with_good_evidence(self):
        """Test confidence calculation with good evidence."""
        verification_result = {
            'evidence': [
                {'source': 'source1', 'relevance': 0.9, 'reliability': 0.95},
                {'source': 'source2', 'relevance': 0.85, 'reliability': 0.90},
            ],
            'ambiguity_score': 0.1,
            'bias_indicators': [],
        }

        result = self.scorer.calculate_confidence(verification_result)

        self.assertIn('confidence_score', result)
        self.assertIn('confidence_level', result)
        self.assertGreater(result['confidence_score'], 0.5)

    def test_calculate_confidence_with_poor_evidence(self):
        """Test confidence calculation with poor evidence."""
        verification_result = {
            'evidence': [{'source': 'none', 'relevance': 0.0, 'reliability': 0.0}],
            'ambiguity_score': 0.8,
            'bias_indicators': ['emotional_language', 'loaded_terminology'],
        }

        result = self.scorer.calculate_confidence(verification_result)

        self.assertLess(result['confidence_score'], 0.5)
        # With very poor evidence and high bias, confidence should be very low
        self.assertIn(result['confidence_level'], ['low', 'very_low'])

    def test_confidence_categorization(self):
        """Test confidence level categorization."""
        self.assertEqual(self.scorer._categorize_confidence(0.9), 'very_high')
        self.assertEqual(self.scorer._categorize_confidence(0.75), 'high')
        self.assertEqual(self.scorer._categorize_confidence(0.55), 'medium')
        self.assertEqual(self.scorer._categorize_confidence(0.35), 'low')
        self.assertEqual(self.scorer._categorize_confidence(0.15), 'very_low')

    def test_confidence_breakdown(self):
        """Test confidence score breakdown."""
        verification_result = {
            'evidence': [{'source': 'test', 'relevance': 0.8, 'reliability': 0.9}],
            'ambiguity_score': 0.2,
            'bias_indicators': [],
        }

        result = self.scorer.calculate_confidence(verification_result)

        self.assertIn('breakdown', result)
        breakdown = result['breakdown']
        self.assertIn('evidence_quality', breakdown)
        self.assertIn('source_reliability', breakdown)
        self.assertIn('claim_clarity', breakdown)


if __name__ == '__main__':
    unittest.main()
