"""
Misinformation Platform - AI-powered Real-Time Analysis & Correction Platform

This package provides tools for analyzing digital content, identifying misinformation,
and suggesting evidence-based corrections.
"""

__version__ = "1.0.0"

from .claim_analyzer import ClaimAnalyzer
from .verification_engine import VerificationEngine
from .confidence_scorer import ConfidenceScorer
from .explanation_generator import ExplanationGenerator

__all__ = [
    'ClaimAnalyzer',
    'VerificationEngine',
    'ConfidenceScorer',
    'ExplanationGenerator',
]
