"""
Example: Basic Usage

Demonstrates basic usage of the Misinformation Platform.
"""

from misinformation_platform import (
    ClaimAnalyzer,
    VerificationEngine,
    ConfidenceScorer,
    ExplanationGenerator
)
from misinformation_platform.content_pipeline import ContentPipeline


def example_1_basic_analysis():
    """Example 1: Basic content analysis."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Content Analysis")
    print("=" * 70 + "\n")

    # Sample content with various claims
    content = """
    The Earth is round and orbits around the Sun. Water boils at 100 degrees
    Celsius at sea level. The COVID-19 pandemic started in 2019. Some people
    believe that all vaccines are dangerous, but this is not supported by
    scientific evidence.
    """

    # Create pipeline and process content
    pipeline = ContentPipeline()
    result = pipeline.process(content)

    # Display overall assessment
    print("Overall Assessment:")
    overall = result['overall_assessment']
    print(f"  Verdict: {overall['verdict']}")
    print(f"  Confidence: {overall['confidence']:.1%}")
    print(f"  Total Claims: {overall['total_claims']}")
    print(f"  Summary: {overall['summary']}\n")

    # Display each claim
    for idx, detail in enumerate(result['detailed_results'], 1):
        claim = detail['claim']
        explanation = detail['explanation']

        print(f"Claim {idx}: {claim['text'][:60]}...")
        print(f"  Verdict: {explanation['verdict']}")
        print(f"  Confidence: {explanation['confidence']['score']:.1%}\n")


def example_2_single_claim_verification():
    """Example 2: Verify a single claim."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Single Claim Verification")
    print("=" * 70 + "\n")

    claim_text = "Water boils at 100 degrees Celsius."

    # Initialize components
    verification_engine = VerificationEngine()
    confidence_scorer = ConfidenceScorer()
    explanation_gen = ExplanationGenerator()

    # Create claim structure
    claim = {
        'id': 'example_claim',
        'text': claim_text,
        'claim_score': 1.0,
    }

    # Verify claim
    verification = verification_engine.verify_claim(claim)
    confidence = confidence_scorer.calculate_confidence(verification)
    explanation = explanation_gen.generate_explanation(claim, verification, confidence)

    # Display formatted explanation
    formatted = explanation_gen.format_for_display(explanation)
    print(formatted)


def example_3_claim_extraction():
    """Example 3: Extract claims from content."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Claim Extraction")
    print("=" * 70 + "\n")

    content = """
    Recent studies show that 95% of scientists agree on climate change.
    The stock market always goes up in the long term. Nobody can predict
    earthquakes with 100% accuracy.
    """

    # Analyze content to extract claims
    analyzer = ClaimAnalyzer()
    result = analyzer.analyze(content)

    print(f"Analyzed {result['sentence_count']} sentences")
    print(f"Identified {result['claims_identified']} claims\n")

    for claim in result['claims']:
        print(f"Claim: {claim['text']}")
        print(f"  Score: {claim['claim_score']:.2f}")
        print(f"  Contains Statistics: {claim['contains_statistics']}")
        print(f"  Contains Absolutes: {claim['contains_absolutes']}")
        print(f"  Entities: {', '.join(claim['extracted_entities'])}\n")


def example_4_pipeline_with_context():
    """Example 4: Process content with context information."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Content Analysis with Context")
    print("=" * 70 + "\n")

    content = "Breaking news: Scientists confirm that the Earth orbits the Sun."

    context = {
        'source': 'Example News Site',
        'author': 'Science Reporter',
        'timestamp': '2024-01-15T10:30:00Z',
    }

    pipeline = ContentPipeline()
    result = pipeline.process(content, context)

    print(f"Content from: {result['context']['source']}")
    print(f"Author: {result['context']['author']}")
    print(f"Processing time: {result['processing_time_seconds']:.3f} seconds\n")

    print("Analysis Results:")
    overall = result['overall_assessment']
    print(f"  Verdict: {overall['verdict']}")
    print(f"  Confidence: {overall['confidence']:.1%}")


def example_5_bias_and_ambiguity_detection():
    """Example 5: Detect bias and ambiguity."""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Bias and Ambiguity Detection")
    print("=" * 70 + "\n")

    # Content with potential bias and ambiguity
    content = """
    This shocking revelation proves that they are all wrong. Some people
    might say this is incredible, but everyone knows the truth. The radical
    changes are outrageous and terrible.
    """

    pipeline = ContentPipeline()
    result = pipeline.process(content)

    for idx, detail in enumerate(result['detailed_results'], 1):
        claim = detail['claim']
        explanation = detail['explanation']

        print(f"Claim {idx}: {claim['text']}")
        print(f"  Ambiguity Level: {explanation['ambiguity_level']:.2f}")
        print(f"  Bias Detected: {', '.join(explanation['bias_detected']) if explanation['bias_detected'] else 'None'}")
        print()


def main():
    """Run all examples."""
    print("\n" + "#" * 70)
    print("# MISINFORMATION PLATFORM - USAGE EXAMPLES")
    print("#" * 70)

    example_1_basic_analysis()
    example_2_single_claim_verification()
    example_3_claim_extraction()
    example_4_pipeline_with_context()
    example_5_bias_and_ambiguity_detection()

    print("\n" + "#" * 70)
    print("# Examples complete!")
    print("#" * 70 + "\n")


if __name__ == '__main__':
    main()
