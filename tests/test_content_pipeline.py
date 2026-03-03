"""
Tests for Content Pipeline Module
"""

import unittest
from misinformation_platform.content_pipeline import ContentPipeline


class TestContentPipeline(unittest.TestCase):
    """Test cases for ContentPipeline class."""

    def setUp(self):
        """Set up test fixtures."""
        self.pipeline = ContentPipeline()

    def test_process_valid_content(self):
        """Test processing of valid content."""
        content = "The Earth is round and orbits the Sun."
        result = self.pipeline.process(content)

        self.assertEqual(result['status'], 'success')
        self.assertIn('overall_assessment', result)
        self.assertIn('detailed_results', result)
        self.assertGreater(result['processing_time_seconds'], 0)

    def test_process_empty_content(self):
        """Test processing of empty content."""
        result = self.pipeline.process("")

        self.assertEqual(result['status'], 'error')

    def test_process_with_context(self):
        """Test processing with context information."""
        content = "Water boils at 100 degrees Celsius."
        context = {'source': 'Test Source', 'author': 'Test Author'}

        result = self.pipeline.process(content, context)

        self.assertEqual(result['status'], 'success')
        self.assertEqual(result['context'], context)

    def test_overall_assessment(self):
        """Test overall assessment calculation."""
        content = "The Earth is round. Water boils at 100C. The sky is blue."
        result = self.pipeline.process(content)

        overall = result['overall_assessment']
        self.assertIn('verdict', overall)
        self.assertIn('confidence', overall)
        # total_claims is only present if there are claims detected
        if overall.get('verdict') != 'no_claims':
            self.assertIn('total_claims', overall)

    def test_get_statistics(self):
        """Test statistics retrieval."""
        # Process some content first
        self.pipeline.process("The Earth is round.")
        self.pipeline.process("Water is wet.")

        stats = self.pipeline.get_statistics()

        self.assertIn('total_processed', stats)
        self.assertEqual(stats['total_processed'], 2)


if __name__ == '__main__':
    unittest.main()
