# Intelligent Real-Time Misinformation Analysis & Correction Platform

An AI-powered platform for analyzing digital content in real-time to identify misleading, incomplete, or false information. The system provides evidence-based verification, structured explanations, and suggested corrections with transparent reasoning.

## Features

- **Real-Time Content Analysis**: Analyze textual content to identify and extract verifiable claims
- **Evidence-Based Verification**: Evaluate claims against available evidence sources
- **Confidence Scoring**: Calculate transparent confidence levels with detailed breakdowns
- **Bias Detection**: Identify potential bias indicators including emotional language and loaded terminology
- **Ambiguity Detection**: Measure and account for ambiguous or unclear statements
- **Structured Explanations**: Generate human-readable explanations with reasoning chains
- **Correction Suggestions**: Provide evidence-based corrections and clarifications
- **Transparency**: Document assumptions, limitations, and decision logic
- **REST API**: HTTP endpoints for integration with other systems
- **CLI Tool**: Command-line interface for direct analysis
- **Scalable Architecture**: Modular design supporting extension and customization

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/balamurugan-cse/pec_projectdemo1.git
cd pec_projectdemo1
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install the package:
```bash
pip install -e .
```

## Quick Start

### Using Python API

```python
from misinformation_platform.content_pipeline import ContentPipeline

# Initialize pipeline
pipeline = ContentPipeline()

# Analyze content
content = "The Earth is flat and has been proven by scientists."
result = pipeline.process(content)

# Display results
print(f"Overall Verdict: {result['overall_assessment']['verdict']}")
print(f"Confidence: {result['overall_assessment']['confidence']:.1%}")
```

### Using CLI

```bash
# Analyze content
python -m misinformation_platform.cli analyze "The Earth is flat."

# Verify a single claim
python -m misinformation_platform.cli verify "Water boils at 100 degrees Celsius."

# Output as JSON
python -m misinformation_platform.cli analyze "Some claim" --format json
```

### Using REST API

1. Start the server:
```bash
python -m misinformation_platform.api_server
```

2. Make API requests:
```bash
# Analyze content
curl -X POST http://localhost:5000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"content": "The Earth is round and orbits the Sun."}'

# Verify single claim
curl -X POST http://localhost:5000/api/verify-claim \
  -H "Content-Type: application/json" \
  -d '{"claim": "Water boils at 100 degrees Celsius."}'

# Get statistics
curl http://localhost:5000/api/statistics
```

## Architecture

### Core Components

1. **ClaimAnalyzer**: Extracts and structures claims from textual content
   - Sentence splitting and claim identification
   - Statistical and absolute statement detection
   - Entity extraction
   - Claim scoring

2. **VerificationEngine**: Verifies claims against evidence sources
   - Evidence gathering from knowledge bases
   - Claim evaluation and verdict determination
   - Ambiguity and bias detection
   - Limitation identification

3. **ConfidenceScorer**: Calculates confidence levels for verification results
   - Multi-factor confidence calculation
   - Evidence quality and quantity scoring
   - Source reliability assessment
   - Transparent breakdown of confidence components

4. **ExplanationGenerator**: Generates structured explanations
   - Human-readable explanations
   - Evidence summaries
   - Correction suggestions
   - Reasoning chain documentation
   - Assumption identification

5. **ContentPipeline**: Orchestrates the complete analysis flow
   - End-to-end content processing
   - Component coordination
   - Overall assessment calculation
   - Statistics tracking

### Verdict Types

- **accurate**: Claim is supported by evidence
- **partially_accurate**: Claim is partially true but may lack context
- **misleading**: Claim lacks critical context or is deceptive
- **false**: Claim contradicts available evidence
- **unverifiable**: Insufficient evidence to verify

### Confidence Levels

- **very_high** (≥85%): Strong evidence with minimal uncertainty
- **high** (≥70%): Good evidence with minor limitations
- **medium** (≥50%): Moderate evidence, view with caution
- **low** (≥30%): Limited evidence, significant uncertainty
- **very_low** (<30%): Insufficient evidence, highly uncertain

## API Reference

### REST API Endpoints

#### POST /api/analyze
Analyze content for misinformation.

**Request:**
```json
{
  "content": "Text to analyze",
  "context": {
    "source": "Source name",
    "author": "Author name"
  }
}
```

**Response:**
```json
{
  "status": "success",
  "overall_assessment": {
    "verdict": "predominantly_accurate",
    "confidence": 0.85,
    "total_claims": 3
  },
  "detailed_results": [...],
  "processing_time_seconds": 0.123
}
```

#### POST /api/verify-claim
Verify a single claim.

**Request:**
```json
{
  "claim": "Claim text to verify"
}
```

**Response:**
```json
{
  "status": "success",
  "verification": {...},
  "confidence": {...},
  "explanation": {...}
}
```

#### GET /api/statistics
Get platform statistics.

#### GET /api/health
Health check endpoint.

#### GET /api/documentation
Get API documentation.

## Configuration

The system uses a predefined knowledge base for verification. In production environments, this should be replaced with connections to external fact-checking APIs and databases.

### Extending the Knowledge Base

Edit `misinformation_platform/verification_engine.py`:

```python
KNOWLEDGE_BASE = {
    'topic_name': {
        'facts': ['fact1', 'fact2'],
        'confidence': 0.95,
    },
}
```

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Or using the test runner
python tests/run_tests.py

# Run specific test file
python -m pytest tests/test_claim_analyzer.py
```

## Examples

See the `examples/` directory for complete examples:

- `basic_usage.py`: Demonstrates basic functionality
- `api_usage.py`: Shows how to use the REST API
- Run examples: `python examples/basic_usage.py`

## Limitations and Assumptions

### Current Limitations

1. **Knowledge Base**: Uses a limited predefined knowledge base; production systems should integrate with external APIs
2. **Language**: Currently supports English text only
3. **Entity Recognition**: Uses simple capitalization-based entity extraction; should be enhanced with NLP libraries
4. **Context Understanding**: Limited semantic understanding; may miss nuanced context
5. **Evidence Sources**: Limited to configured sources; real-world deployment requires multiple diverse sources

### Assumptions

1. Evidence sources are reasonably up-to-date and accurate
2. Absence of evidence indicates unverifiability, not falsehood
3. Claims are in English and use standard grammar
4. Text is UTF-8 encoded
5. Interpretation of ambiguous language based on common usage

## Responsible AI Considerations

### Design Principles

1. **Transparency**: All reasoning processes are documented and explainable
2. **Uncertainty Communication**: Confidence levels clearly indicate uncertainty
3. **Limitation Documentation**: System limitations are explicitly stated
4. **Bias Awareness**: Potential biases in content and analysis are identified
5. **No Absolute Claims**: System acknowledges fallibility and need for human oversight

### Best Practices

- Always review automated assessments before acting on them
- Use confidence scores to inform decision-making
- Consider multiple verification sources when possible
- Be aware of potential bias in both content and analysis
- Regularly update knowledge bases and evidence sources
- Monitor system performance and accuracy metrics

## Scalability

### Production Deployment Considerations

1. **Caching**: Implement caching for frequently analyzed content
2. **Rate Limiting**: Add rate limiting to API endpoints
3. **Async Processing**: Use async/await for concurrent claim verification
4. **Database**: Store verification history in persistent storage
5. **Load Balancing**: Deploy multiple instances behind a load balancer
6. **Monitoring**: Add logging, metrics, and alerting
7. **External APIs**: Integrate with fact-checking APIs (Snopes, FactCheck.org, etc.)

## Contributing

Contributions are welcome! Areas for enhancement:

1. Integration with external fact-checking APIs
2. Multi-language support
3. Enhanced NLP with spaCy or similar libraries
4. Machine learning models for claim classification
5. Web interface
6. Database integration for persistent storage
7. Async processing capabilities
8. Enhanced entity recognition

## License

This project is open source and available for educational and research purposes.

## Acknowledgments

This platform is designed for educational purposes to demonstrate AI-powered content analysis and verification techniques. It should be used as part of a comprehensive approach to misinformation detection that includes human oversight and multiple verification sources.

## Contact

For questions, issues, or contributions, please use the GitHub repository issue tracker.