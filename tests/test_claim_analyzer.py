"""
Tests for Claim Analyzer Module
"""

import unittest
from misinformation_platform.claim_analyzer import ClaimAnalyzer


class TestClaimAnalyzer(unittest.TestCase):
    """Test cases for ClaimAnalyzer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = ClaimAnalyzer()

    def test_analyze_valid_content(self):
        """Test analysis of valid content."""
        content = "The Earth is round. Water boils at 100 degrees Celsius."
        result = self.analyzer.analyze(content)

        self.assertEqual(result['status'], 'success')
        self.assertGreater(result['claims_identified'], 0)
        self.assertIsInstance(result['claims'], list)

    def test_analyze_empty_content(self):
        """Test analysis of empty content."""
        result = self.analyzer.analyze("")

        self.assertEqual(result['status'], 'error')
        self.assertEqual(result['claims'], [])

    def test_analyze_invalid_content(self):
        """Test analysis of invalid content."""
        result = self.analyzer.analyze(None)

        self.assertEqual(result['status'], 'error')

    def test_contains_statistics(self):
        """Test detection of statistical content."""
        text_with_stats = "95% of scientists agree on climate change."
        text_without_stats = "Scientists generally agree on climate change."

        self.assertTrue(self.analyzer._contains_statistics(text_with_stats))
        self.assertFalse(self.analyzer._contains_statistics(text_without_stats))

    def test_contains_absolutes(self):
        """Test detection of absolute statements."""
        text_with_absolute = "This always happens in every case."
        text_without_absolute = "This sometimes happens."

        self.assertTrue(self.analyzer._contains_absolutes(text_with_absolute))
        self.assertFalse(self.analyzer._contains_absolutes(text_without_absolute))

    def test_claim_score_calculation(self):
        """Test claim score calculation."""
        factual_claim = "Water boils at 100 degrees Celsius."
        question = "Does water boil at 100 degrees?"

        factual_score = self.analyzer._calculate_claim_score(factual_claim)
        question_score = self.analyzer._calculate_claim_score(question)

        # Factual claims should have higher score than questions
        self.assertGreater(factual_score, question_score)


if __name__ == '__main__':
    unittest.main()
