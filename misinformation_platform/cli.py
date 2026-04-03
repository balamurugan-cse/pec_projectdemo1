"""
Command Line Interface for Misinformation Platform

Provides a CLI tool for analyzing content and verifying claims.
"""

import sys
import json
import argparse
from typing import Optional

from .content_pipeline import ContentPipeline
from .explanation_generator import ExplanationGenerator


def analyze_content(content: str, context: Optional[dict] = None, output_format: str = 'text'):
    """Analyze content and display results."""
    pipeline = ContentPipeline()
    result = pipeline.process(content, context)

    if output_format == 'json':
        print(json.dumps(result, indent=2))
    else:
        # Text format
        print("\n" + "=" * 70)
        print("MISINFORMATION ANALYSIS RESULT")
        print("=" * 70 + "\n")

        # Overall assessment
        overall = result.get('overall_assessment', {})
        print(f"Overall Verdict: {overall.get('verdict', 'unknown').upper()}")
        print(f"Overall Confidence: {overall.get('confidence', 0):.1%}")
        print(f"Summary: {overall.get('summary', '')}")
        print(f"\nClaims Analyzed: {overall.get('total_claims', 0)}")

        if overall.get('claim_breakdown'):
            print("\nClaim Breakdown:")
            for verdict, count in overall['claim_breakdown'].items():
                print(f"  - {verdict}: {count}")

        # Detailed results
        print("\n" + "-" * 70)
        print("DETAILED CLAIM ANALYSIS")
        print("-" * 70 + "\n")

        for idx, detail in enumerate(result.get('detailed_results', []), 1):
            claim = detail.get('claim', {})
            explanation = detail.get('explanation', {})

            print(f"Claim #{idx}:")
            print(f"  Text: {claim.get('text', '')}")
            print(f"  Verdict: {explanation.get('verdict', 'unknown').upper()}")

            confidence_info = explanation.get('confidence', {})
            print(f"  Confidence: {confidence_info.get('score', 0):.1%} ({confidence_info.get('level', 'unknown')})")

            correction = explanation.get('correction', {})
            if correction.get('needed'):
                print(f"  Correction Needed: {correction.get('type', 'unknown')}")
                print(f"  Suggestion: {correction.get('suggestion', '')}")

            print()

        print("=" * 70 + "\n")


def verify_claim(claim: str, output_format: str = 'text'):
    """Verify a single claim and display results."""
    pipeline = ContentPipeline()
    explanation_gen = ExplanationGenerator()

    claim_data = {
        'id': 'cli_claim',
        'text': claim,
        'claim_score': 1.0,
    }

    verification = pipeline.verification_engine.verify_claim(claim_data)
    confidence = pipeline.confidence_scorer.calculate_confidence(verification)
    explanation = explanation_gen.generate_explanation(claim_data, verification, confidence)

    if output_format == 'json':
        print(json.dumps(explanation, indent=2))
    else:
        formatted = explanation_gen.format_for_display(explanation)
        print(formatted)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Misinformation Analysis Platform CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze content from text
  python -m misinformation_platform.cli analyze "The Earth is flat."

  # Verify a single claim
  python -m misinformation_platform.cli verify "Water boils at 100 degrees Celsius."

  # Output as JSON
  python -m misinformation_platform.cli analyze "Some claim" --format json
        """
    )

    parser.add_argument(
        'command',
        choices=['analyze', 'verify'],
        help='Command to execute'
    )

    parser.add_argument(
        'text',
        help='Text content or claim to analyze/verify'
    )

    parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    parser.add_argument(
        '--source',
        help='Source of the content (optional context)'
    )

    parser.add_argument(
        '--author',
        help='Author of the content (optional context)'
    )

    args = parser.parse_args()

    # Build context if provided
    context = {}
    if args.source:
        context['source'] = args.source
    if args.author:
        context['author'] = args.author

    try:
        if args.command == 'analyze':
            analyze_content(args.text, context if context else None, args.format)
        elif args.command == 'verify':
            verify_claim(args.text, args.format)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
