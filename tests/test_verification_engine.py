"""
Tests for Verification Engine Module
"""

import unittest
from misinformation_platform.verification_engine import VerificationEngine


class TestVerificationEngine(unittest.TestCase):
    """Test cases for VerificationEngine class."""

    def setUp(self):
        """Set up test fixtures."""
        self.engine = VerificationEngine()

    def test_verify_claim_with_evidence(self):
        """Test verification of claim with available evidence."""
        claim = {
            'id': 'test_claim_1',
            'text': 'The Earth is round.',
        }

        result = self.engine.verify_claim(claim)

        self.assertIn('verdict', result)
        self.assertIn('confidence', result)
        self.assertIn('evidence', result)

    def test_verify_claim_without_evidence(self):
        """Test verification of claim without evidence."""
        claim = {
            'id': 'test_claim_2',
            'text': 'Something completely unknown and unverifiable.',
        }

        result = self.engine.verify_claim(claim)

        self.assertEqual(result['verdict'], 'unverifiable')
        self.assertLess(result['confidence'], 0.5)

    def test_detect_ambiguity(self):
        """Test ambiguity detection."""
        clear_text = "Water boils at exactly 100 degrees Celsius."
        ambiguous_text = "Some people might say that it could be true."

        clear_score = self.engine._detect_ambiguity(clear_text)
        ambiguous_score = self.engine._detect_ambiguity(ambiguous_text)

        self.assertLess(clear_score, ambiguous_score)

    def test_detect_bias(self):
        """Test bias detection."""
        biased_text = "This shocking and outrageous claim is radical."
        neutral_text = "According to the study, the results indicate."

        biased_indicators = self.engine._detect_bias(biased_text)
        neutral_indicators = self.engine._detect_bias(neutral_text)

        self.assertGreater(len(biased_indicators), len(neutral_indicators))

    def test_verify_multiple_claims(self):
        """Test verification of multiple claims."""
        claims = [
            {'id': 'claim1', 'text': 'The Earth is round.'},
            {'id': 'claim2', 'text': 'Water boils at 100 Celsius.'},
        ]

        results = self.engine.verify_claims(claims)

        self.assertEqual(len(results), 2)
        for result in results:
            self.assertIn('verdict', result)
            self.assertIn('confidence', result)


if __name__ == '__main__':
    unittest.main()
