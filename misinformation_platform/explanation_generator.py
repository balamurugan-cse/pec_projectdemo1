"""
Explanation Generator Module

Generates structured explanations and evidence-based corrections
for verification results with transparent reasoning.
"""

from typing import Dict, Any, List
from datetime import datetime


class ExplanationGenerator:
    """
    Generates human-readable explanations for verification results.
    """

    def __init__(self):
        """Initialize the explanation generator."""
        pass

    def generate_explanation(
        self,
        claim: Dict[str, Any],
        verification_result: Dict[str, Any],
        confidence_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate comprehensive explanation for a verification result.

        Args:
            claim: The original claim data
            verification_result: Verification result from VerificationEngine
            confidence_analysis: Confidence analysis from ConfidenceScorer

        Returns:
            Structured explanation with corrections and reasoning
        """
        verdict = verification_result.get('verdict', 'unverifiable')
        confidence_score = confidence_analysis.get('confidence_score', 0.0)
        evidence = verification_result.get('evidence', [])

        # Generate main explanation
        main_explanation = self._generate_main_explanation(verdict, confidence_score)

        # Generate evidence summary
        evidence_summary = self._generate_evidence_summary(evidence)

        # Generate correction or clarification
        correction = self._generate_correction(claim, verdict, evidence)

        # Generate reasoning chain
        reasoning = self._generate_reasoning(
            claim, verification_result, confidence_analysis
        )

        # Identify assumptions
        assumptions = self._identify_assumptions(verification_result)

        # Document limitations
        limitations = verification_result.get('limitations', [])

        return {
            'summary': main_explanation,
            'verdict': verdict,
            'confidence': {
                'score': confidence_score,
                'level': confidence_analysis.get('confidence_level'),
                'interpretation': confidence_analysis.get('interpretation'),
            },
            'evidence_summary': evidence_summary,
            'correction': correction,
            'reasoning_chain': reasoning,
            'assumptions': assumptions,
            'limitations': limitations,
            'bias_detected': verification_result.get('bias_indicators', []),
            'ambiguity_level': verification_result.get('ambiguity_score', 0.0),
            'generated_at': datetime.now().isoformat(),
        }

    def _generate_main_explanation(self, verdict: str, confidence: float) -> str:
        """Generate main explanation text based on verdict and confidence."""
        templates = {
            'accurate': f'The claim appears to be accurate based on available evidence (confidence: {confidence:.1%}).',
            'partially_accurate': f'The claim is partially accurate but may lack important context (confidence: {confidence:.1%}).',
            'misleading': f'The claim is misleading or lacks critical context (confidence: {confidence:.1%}).',
            'false': f'The claim contradicts available evidence and appears to be false (confidence: {confidence:.1%}).',
            'unverifiable': f'There is insufficient evidence to verify this claim (confidence: {confidence:.1%}).',
        }

        return templates.get(verdict, f'Analysis complete with {confidence:.1%} confidence.')

    def _generate_evidence_summary(self, evidence: List[Dict[str, Any]]) -> str:
        """Generate summary of evidence used in verification."""
        if not evidence or evidence[0].get('source') == 'none':
            return 'No direct evidence was found in available sources.'

        valid_evidence = [e for e in evidence if e.get('relevance', 0) > 0.5]

        if not valid_evidence:
            return 'Limited relevant evidence was found.'

        summary_parts = []
        for ev in valid_evidence[:3]:  # Limit to top 3 pieces of evidence
            source = ev.get('source', 'unknown')
            content = ev.get('content', '')
            reliability = ev.get('reliability', 0.5)

            summary_parts.append(
                f"- {source.replace('_', ' ').title()}: {content} "
                f"(reliability: {reliability:.1%})"
            )

        return '\n'.join(summary_parts)

    def _generate_correction(
        self,
        claim: Dict[str, Any],
        verdict: str,
        evidence: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate correction or clarification if needed."""
        claim_text = claim.get('text', '')

        if verdict == 'accurate':
            return {
                'needed': False,
                'type': 'none',
                'suggestion': None,
                'explanation': 'No correction needed; claim is supported by evidence.',
            }

        if verdict == 'unverifiable':
            return {
                'needed': True,
                'type': 'clarification',
                'suggestion': 'This claim cannot be verified with available evidence. '
                             'Additional context or sources would be needed for verification.',
                'explanation': 'Claim lacks sufficient evidence for verification.',
            }

        if verdict in ['misleading', 'partially_accurate']:
            return {
                'needed': True,
                'type': 'context_addition',
                'suggestion': f'The claim "{claim_text}" requires additional context. '
                             'While partially true, it may omit important nuances or exceptions.',
                'explanation': 'Additional context needed to prevent misunderstanding.',
            }

        if verdict == 'false':
            # Generate correction based on evidence
            if evidence and evidence[0].get('source') != 'none':
                correct_info = evidence[0].get('content', '')
                return {
                    'needed': True,
                    'type': 'correction',
                    'suggestion': f'Based on available evidence, a more accurate statement would be: {correct_info}',
                    'explanation': 'Claim contradicts verified information.',
                }

        return {
            'needed': True,
            'type': 'review',
            'suggestion': 'This claim should be reviewed and potentially revised.',
            'explanation': 'Verification raised concerns about accuracy.',
        }

    def _generate_reasoning(
        self,
        claim: Dict[str, Any],
        verification_result: Dict[str, Any],
        confidence_analysis: Dict[str, Any]
    ) -> List[str]:
        """Generate transparent reasoning chain."""
        reasoning_steps = []

        # Step 1: Claim analysis
        reasoning_steps.append(
            f"1. Analyzed claim: \"{claim.get('text', '')}\" "
            f"(claim score: {claim.get('claim_score', 0):.2f})"
        )

        # Step 2: Evidence gathering
        evidence = verification_result.get('evidence', [])
        evidence_count = len([e for e in evidence if e.get('relevance', 0) > 0.5])
        reasoning_steps.append(
            f"2. Gathered evidence from {len(evidence)} source(s), "
            f"{evidence_count} highly relevant"
        )

        # Step 3: Ambiguity and bias check
        ambiguity = verification_result.get('ambiguity_score', 0)
        bias_count = len(verification_result.get('bias_indicators', []))
        reasoning_steps.append(
            f"3. Checked for ambiguity (score: {ambiguity:.2f}) "
            f"and bias ({bias_count} indicator(s) found)"
        )

        # Step 4: Evidence evaluation
        breakdown = confidence_analysis.get('breakdown', {})
        reasoning_steps.append(
            f"4. Evaluated evidence quality ({breakdown.get('evidence_quality', 0):.2f}) "
            f"and source reliability ({breakdown.get('source_reliability', 0):.2f})"
        )

        # Step 5: Verdict determination
        verdict = verification_result.get('verdict', 'unverifiable')
        confidence = confidence_analysis.get('confidence_score', 0)
        reasoning_steps.append(
            f"5. Determined verdict: {verdict} with {confidence:.1%} confidence"
        )

        return reasoning_steps

    def _identify_assumptions(self, verification_result: Dict[str, Any]) -> List[str]:
        """Identify assumptions made during verification."""
        assumptions = []

        evidence = verification_result.get('evidence', [])

        if not evidence or evidence[0].get('source') == 'none':
            assumptions.append(
                'Assumed that absence of evidence indicates unverifiability, '
                'not necessarily falsehood'
            )

        if evidence:
            assumptions.append(
                'Assumed that evidence sources are reasonably up-to-date and accurate'
            )

        if verification_result.get('ambiguity_score', 0) > 0.5:
            assumptions.append(
                'Assumed interpretation of ambiguous language based on common usage'
            )

        bias_indicators = verification_result.get('bias_indicators', [])
        if 'unattributed_claim' in bias_indicators:
            assumptions.append(
                'Assumed claim lacks attribution due to missing source citation'
            )

        return assumptions

    def format_for_display(self, explanation: Dict[str, Any]) -> str:
        """
        Format explanation as human-readable text.

        Args:
            explanation: Structured explanation dictionary

        Returns:
            Formatted text output
        """
        output_parts = []

        # Header
        output_parts.append("=" * 60)
        output_parts.append("VERIFICATION RESULT")
        output_parts.append("=" * 60)
        output_parts.append("")

        # Summary
        output_parts.append("SUMMARY:")
        output_parts.append(explanation.get('summary', ''))
        output_parts.append("")

        # Verdict and Confidence
        output_parts.append("VERDICT:")
        output_parts.append(f"  Status: {explanation.get('verdict', 'unknown').upper()}")
        confidence_info = explanation.get('confidence', {})
        output_parts.append(f"  Confidence: {confidence_info.get('score', 0):.1%} ({confidence_info.get('level', 'unknown')})")
        output_parts.append(f"  {confidence_info.get('interpretation', '')}")
        output_parts.append("")

        # Evidence
        output_parts.append("EVIDENCE:")
        output_parts.append(explanation.get('evidence_summary', 'No evidence available'))
        output_parts.append("")

        # Correction
        correction = explanation.get('correction', {})
        if correction.get('needed'):
            output_parts.append("SUGGESTED CORRECTION:")
            output_parts.append(f"  Type: {correction.get('type', 'unknown')}")
            output_parts.append(f"  {correction.get('suggestion', '')}")
            output_parts.append("")

        # Reasoning
        output_parts.append("REASONING PROCESS:")
        for step in explanation.get('reasoning_chain', []):
            output_parts.append(f"  {step}")
        output_parts.append("")

        # Limitations
        limitations = explanation.get('limitations', [])
        if limitations:
            output_parts.append("LIMITATIONS:")
            for limitation in limitations:
                output_parts.append(f"  - {limitation}")
            output_parts.append("")

        # Assumptions
        assumptions = explanation.get('assumptions', [])
        if assumptions:
            output_parts.append("ASSUMPTIONS:")
            for assumption in assumptions:
                output_parts.append(f"  - {assumption}")
            output_parts.append("")

        # Footer
        output_parts.append("=" * 60)

        return "\n".join(output_parts)
