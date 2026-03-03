"""
API Server Module

Flask-based REST API for real-time misinformation analysis.
Provides endpoints for content analysis, claim verification, and system information.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from typing import Dict, Any

from .content_pipeline import ContentPipeline

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize the content pipeline
pipeline = ContentPipeline()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Misinformation Analysis Platform',
        'version': '1.0.0',
        'timestamp': datetime.now().isoformat(),
    })


@app.route('/api/analyze', methods=['POST'])
def analyze_content():
    """
    Analyze content for misinformation.

    Request JSON:
        {
            "content": "text to analyze",
            "context": {  // optional
                "source": "source name",
                "author": "author name",
                "timestamp": "ISO timestamp"
            }
        }

    Response JSON:
        {
            "status": "success",
            "content_metadata": {...},
            "overall_assessment": {...},
            "detailed_results": [...],
            "processing_time_seconds": 0.123,
            "timestamp": "ISO timestamp"
        }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data provided',
            }), 400

        content = data.get('content')
        if not content:
            return jsonify({
                'status': 'error',
                'message': 'Content field is required',
            }), 400

        context = data.get('context', {})

        # Process content through pipeline
        result = pipeline.process(content, context)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}',
            'timestamp': datetime.now().isoformat(),
        }), 500


@app.route('/api/verify-claim', methods=['POST'])
def verify_single_claim():
    """
    Verify a single claim.

    Request JSON:
        {
            "claim": "claim text to verify"
        }

    Response JSON:
        {
            "status": "success",
            "verification": {...},
            "confidence": {...},
            "explanation": {...}
        }
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'status': 'error',
                'message': 'No JSON data provided',
            }), 400

        claim_text = data.get('claim')
        if not claim_text:
            return jsonify({
                'status': 'error',
                'message': 'Claim field is required',
            }), 400

        # Create claim structure
        claim = {
            'id': 'single_claim',
            'text': claim_text,
            'claim_score': 1.0,  # Direct claim verification
        }

        # Verify claim
        verification = pipeline.verification_engine.verify_claim(claim)
        confidence = pipeline.confidence_scorer.calculate_confidence(verification)
        explanation = pipeline.explanation_generator.generate_explanation(
            claim, verification, confidence
        )

        return jsonify({
            'status': 'success',
            'verification': verification,
            'confidence': confidence,
            'explanation': explanation,
            'timestamp': datetime.now().isoformat(),
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}',
            'timestamp': datetime.now().isoformat(),
        }), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Get platform statistics.

    Response JSON:
        {
            "status": "success",
            "statistics": {...}
        }
    """
    try:
        stats = pipeline.get_statistics()

        return jsonify({
            'status': 'success',
            'statistics': stats,
            'timestamp': datetime.now().isoformat(),
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}',
            'timestamp': datetime.now().isoformat(),
        }), 500


@app.route('/api/documentation', methods=['GET'])
def get_documentation():
    """
    Get API documentation.

    Response JSON:
        {
            "status": "success",
            "documentation": {...}
        }
    """
    documentation = {
        'service': 'Misinformation Analysis Platform',
        'version': '1.0.0',
        'description': 'AI-powered platform for real-time misinformation analysis and correction',
        'endpoints': [
            {
                'path': '/api/health',
                'method': 'GET',
                'description': 'Health check endpoint',
            },
            {
                'path': '/api/analyze',
                'method': 'POST',
                'description': 'Analyze content for misinformation',
                'parameters': {
                    'content': 'Text content to analyze (required)',
                    'context': 'Optional context information (source, author, etc.)',
                },
            },
            {
                'path': '/api/verify-claim',
                'method': 'POST',
                'description': 'Verify a single claim',
                'parameters': {
                    'claim': 'Claim text to verify (required)',
                },
            },
            {
                'path': '/api/statistics',
                'method': 'GET',
                'description': 'Get platform processing statistics',
            },
            {
                'path': '/api/documentation',
                'method': 'GET',
                'description': 'Get API documentation',
            },
        ],
        'features': [
            'Real-time content analysis',
            'Claim extraction and verification',
            'Evidence-based fact-checking',
            'Confidence scoring',
            'Bias and ambiguity detection',
            'Transparent reasoning',
            'Structured explanations',
            'Suggested corrections',
        ],
    }

    return jsonify({
        'status': 'success',
        'documentation': documentation,
        'timestamp': datetime.now().isoformat(),
    })


def run_server(host='0.0.0.0', port=5000, debug=False):
    """
    Run the API server.

    Args:
        host: Host address to bind to
        port: Port number to listen on
        debug: Enable debug mode
    """
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    run_server(debug=True)
