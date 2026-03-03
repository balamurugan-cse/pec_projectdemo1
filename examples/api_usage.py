"""
API Usage Example

Demonstrates how to use the REST API server.
"""

import requests
import json


def example_analyze_content():
    """Example: Analyze content using the API."""
    print("\n" + "=" * 70)
    print("API EXAMPLE: Analyze Content")
    print("=" * 70 + "\n")

    url = "http://localhost:5000/api/analyze"

    data = {
        "content": """
            The Earth is round and orbits around the Sun. Water boils at 100
            degrees Celsius at sea level. Some people believe all vaccines
            are dangerous, but this is not supported by scientific evidence.
        """,
        "context": {
            "source": "Example Document",
            "author": "Test User"
        }
    }

    try:
        response = requests.post(url, json=data)
        result = response.json()

        print(f"Status: {response.status_code}")
        print(f"\nOverall Assessment:")
        overall = result.get('overall_assessment', {})
        print(f"  Verdict: {overall.get('verdict')}")
        print(f"  Confidence: {overall.get('confidence'):.1%}")
        print(f"  Total Claims: {overall.get('total_claims')}")

        print(f"\nProcessing Time: {result.get('processing_time_seconds'):.3f} seconds")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server.")
        print("Make sure the server is running: python -m misinformation_platform.api_server")
    except Exception as e:
        print(f"Error: {e}")


def example_verify_claim():
    """Example: Verify a single claim using the API."""
    print("\n" + "=" * 70)
    print("API EXAMPLE: Verify Single Claim")
    print("=" * 70 + "\n")

    url = "http://localhost:5000/api/verify-claim"

    data = {
        "claim": "Water boils at 100 degrees Celsius."
    }

    try:
        response = requests.post(url, json=data)
        result = response.json()

        print(f"Status: {response.status_code}")

        explanation = result.get('explanation', {})
        print(f"\nClaim Verification:")
        print(f"  Verdict: {explanation.get('verdict')}")

        confidence = explanation.get('confidence', {})
        print(f"  Confidence: {confidence.get('score'):.1%} ({confidence.get('level')})")
        print(f"  {confidence.get('interpretation')}")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server.")
        print("Make sure the server is running: python -m misinformation_platform.api_server")
    except Exception as e:
        print(f"Error: {e}")


def example_get_statistics():
    """Example: Get platform statistics."""
    print("\n" + "=" * 70)
    print("API EXAMPLE: Get Statistics")
    print("=" * 70 + "\n")

    url = "http://localhost:5000/api/statistics"

    try:
        response = requests.get(url)
        result = response.json()

        print(f"Status: {response.status_code}")

        stats = result.get('statistics', {})
        print(f"\nPlatform Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")

    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API server.")
        print("Make sure the server is running: python -m misinformation_platform.api_server")
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all API examples."""
    print("\n" + "#" * 70)
    print("# API USAGE EXAMPLES")
    print("# Make sure the API server is running first:")
    print("# python -m misinformation_platform.api_server")
    print("#" * 70)

    example_analyze_content()
    example_verify_claim()
    example_get_statistics()

    print("\n" + "#" * 70)
    print("# Examples complete!")
    print("#" * 70 + "\n")


if __name__ == '__main__':
    main()
