"""
Test runner for all tests
"""

import unittest
import sys

# Import all test modules
from tests import (
    test_claim_analyzer,
    test_verification_engine,
    test_confidence_scorer,
    test_content_pipeline,
)


def run_all_tests():
    """Run all test suites."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test modules
    suite.addTests(loader.loadTestsFromModule(test_claim_analyzer))
    suite.addTests(loader.loadTestsFromModule(test_verification_engine))
    suite.addTests(loader.loadTestsFromModule(test_confidence_scorer))
    suite.addTests(loader.loadTestsFromModule(test_content_pipeline))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Return exit code based on results
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_all_tests())
