"""
Content Pipeline Module

Orchestrates the real-time processing of content through the analysis pipeline.
Coordinates claim analysis, verification, confidence scoring, and explanation generation.
"""

from typing import Dict, Any, List
from datetime import datetime

from .claim_analyzer import ClaimAnalyzer
from .verification_engine import VerificationEngine
from .confidence_scorer import ConfidenceScorer
from .explanation_generator import ExplanationGenerator


class ContentPipeline:
    """
    Real-time content processing pipeline that orchestrates the complete analysis flow.
    """

    def __init__(self):
        """Initialize the content pipeline with all required components."""
        self.claim_analyzer = ClaimAnalyzer()
        self.verification_engine = VerificationEngine()
        self.confidence_scorer = ConfidenceScorer()
        self.explanation_generator = ExplanationGenerator()

        self.processing_history = []

    def process(self, content: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process content through the complete analysis pipeline.

        Args:
            content: The textual content to analyze
            context: Optional context information (source, author, timestamp, etc.)

        Returns:
            Complete analysis result with all components
        """
        start_time = datetime.now()

        # Step 1: Analyze content and extract claims
        analysis_result = self.claim_analyzer.analyze(content, context)

        if analysis_result['status'] != 'success':
            return {
                'status': 'error',
                'message': analysis_result.get('message', 'Analysis failed'),
                'timestamp': datetime.now().isoformat(),
            }

        claims = analysis_result.get('claims', [])

        # Step 2: Verify each claim
        verification_results = []
        for claim in claims:
            verification = self.verification_engine.verify_claim(claim)
            verification_results.append(verification)

        # Step 3: Calculate confidence scores
        confidence_results = []
        for verification in verification_results:
            confidence = self.confidence_scorer.calculate_confidence(verification)
            confidence_results.append(confidence)

        # Step 4: Generate explanations
        explanations = []
        for claim, verification, confidence in zip(claims, verification_results, confidence_results):
            explanation = self.explanation_generator.generate_explanation(
                claim, verification, confidence
            )
            explanations.append(explanation)

        # Calculate overall assessment
        overall_assessment = self._calculate_overall_assessment(
            verification_results, confidence_results
        )

        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()

        result = {
            'status': 'success',
            'content_metadata': {
                'length': analysis_result.get('content_length'),
                'sentences': analysis_result.get('sentence_count'),
                'claims_identified': analysis_result.get('claims_identified'),
            },
            'overall_assessment': overall_assessment,
            'detailed_results': [
                {
                    'claim': claim,
                    'verification': verification,
                    'confidence': confidence,
                    'explanation': explanation,
                }
                for claim, verification, confidence, explanation
                in zip(claims, verification_results, confidence_results, explanations)
            ],
            'processing_time_seconds': processing_time,
            'timestamp': datetime.now().isoformat(),
            'context': context or {},
        }

        # Store in history
        self.processing_history.append({
            'timestamp': datetime.now().isoformat(),
            'content_length': len(content),
            'claims_count': len(claims),
            'overall_verdict': overall_assessment.get('verdict'),
        })

        return result

    def _calculate_overall_assessment(
        self,
        verification_results: List[Dict[str, Any]],
        confidence_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate overall assessment of the content.

        Args:
            verification_results: List of verification results
            confidence_results: List of confidence analyses

        Returns:
            Overall assessment dictionary
        """
        if not verification_results:
            return {
                'verdict': 'no_claims',
                'confidence': 0.0,
                'summary': 'No verifiable claims identified in content',
            }

        # Count verdicts
        verdict_counts = {}
        for result in verification_results:
            verdict = result.get('verdict', 'unverifiable')
            verdict_counts[verdict] = verdict_counts.get(verdict, 0) + 1

        # Calculate average confidence
        avg_confidence = sum(
            c.get('confidence_score', 0) for c in confidence_results
        ) / len(confidence_results)

        # Determine overall verdict
        total_claims = len(verification_results)
        accurate_count = verdict_counts.get('accurate', 0)
        false_count = verdict_counts.get('false', 0)
        misleading_count = verdict_counts.get('misleading', 0)
        unverifiable_count = verdict_counts.get('unverifiable', 0)

        if false_count > total_claims * 0.5:
            overall_verdict = 'predominantly_false'
        elif misleading_count > total_claims * 0.5:
            overall_verdict = 'predominantly_misleading'
        elif accurate_count > total_claims * 0.7:
            overall_verdict = 'predominantly_accurate'
        elif unverifiable_count > total_claims * 0.7:
            overall_verdict = 'mostly_unverifiable'
        else:
            overall_verdict = 'mixed'

        return {
            'verdict': overall_verdict,
            'confidence': round(avg_confidence, 3),
            'claim_breakdown': verdict_counts,
            'total_claims': total_claims,
            'summary': self._generate_overall_summary(overall_verdict, avg_confidence),
        }

    def _generate_overall_summary(self, verdict: str, confidence: float) -> str:
        """Generate human-readable overall summary."""
        summaries = {
            'predominantly_false': f'Content contains predominantly false claims (confidence: {confidence:.1%})',
            'predominantly_misleading': f'Content is predominantly misleading or lacks context (confidence: {confidence:.1%})',
            'predominantly_accurate': f'Content is predominantly accurate (confidence: {confidence:.1%})',
            'mostly_unverifiable': f'Most claims cannot be verified with available evidence (confidence: {confidence:.1%})',
            'mixed': f'Content contains a mix of accurate, misleading, and unverifiable claims (confidence: {confidence:.1%})',
            'no_claims': 'No verifiable claims identified',
        }
        return summaries.get(verdict, f'Analysis complete with {confidence:.1%} confidence')

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get processing statistics.

        Returns:
            Dictionary with pipeline statistics
        """
        if not self.processing_history:
            return {
                'total_processed': 0,
                'message': 'No content processed yet',
            }

        total_claims = sum(h.get('claims_count', 0) for h in self.processing_history)

        return {
            'total_processed': len(self.processing_history),
            'total_claims_analyzed': total_claims,
            'average_claims_per_content': round(total_claims / len(self.processing_history), 2),
            'verification_history_size': len(self.verification_engine.verification_history),
        }
