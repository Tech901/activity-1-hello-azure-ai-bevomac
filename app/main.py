"""
Activity 1 - Hello, Azure AI
AI-102: First API calls to Azure AI services

Your task:
  1. Load environment variables and validate Azure credentials
  2. Call Azure OpenAI to classify a Memphis 311 service request
  3. Call Azure Content Safety to check text for harmful content
  4. Call Azure AI Language to extract key phrases from a complaint
  5. Write result.json with responses from all three services

Output: result.json with required fields (task, status, outputs, metadata)
"""
import json
import os
import sys
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv()

# Resolve activity root so result.json lands in the right place regardless of CWD
_ACTIVITY_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _get_sdk_version() -> str:
    try:
        from importlib.metadata import version
        return version("openai")
    except Exception:
        return "unknown"


# ---------------------------------------------------------------------------
# Lazy client initialization
# ---------------------------------------------------------------------------
_openai_client = None
_content_safety_client = None
_language_client = None


def _get_openai_client():
    """Lazily initialize the Azure OpenAI client."""
    global _openai_client
    if _openai_client is None:
        # TODO: Uncomment and configure
        #   from openai import AzureOpenAI
        #   _openai_client = AzureOpenAI(
        #       azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        #       api_key=os.environ["AZURE_OPENAI_API_KEY"],
        #       api_version="2024-10-21",
        #   )
        raise NotImplementedError("Configure the Azure OpenAI client")
    return _openai_client


def _get_content_safety_client():
    """Lazily initialize the Azure Content Safety client."""
    global _content_safety_client
    if _content_safety_client is None:
        # NOTE: The Content Safety SDK handles API versioning internally --
        # no api_version parameter is needed (unlike the OpenAI SDK).
        # TODO: Uncomment and configure
        #   from azure.ai.contentsafety import ContentSafetyClient
        #   from azure.core.credentials import AzureKeyCredential
        #   _content_safety_client = ContentSafetyClient(
        #       endpoint=os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"],
        #       credential=AzureKeyCredential(os.environ["AZURE_CONTENT_SAFETY_KEY"]),
        #   )
        raise NotImplementedError("Configure the Content Safety client")
    return _content_safety_client


def _get_language_client():
    """Lazily initialize the Azure AI Language client."""
    global _language_client
    if _language_client is None:
        # NOTE: The Language SDK handles API versioning internally --
        # no api_version parameter is needed (unlike the OpenAI SDK).
        # TODO: Uncomment and configure
        #   from azure.ai.textanalytics import TextAnalyticsClient
        #   from azure.core.credentials import AzureKeyCredential
        #   _language_client = TextAnalyticsClient(
        #       endpoint=os.environ["AZURE_AI_LANGUAGE_ENDPOINT"],
        #       credential=AzureKeyCredential(os.environ["AZURE_AI_LANGUAGE_KEY"]),
        #   )
        raise NotImplementedError("Configure the AI Language client")
    return _language_client


# ---------------------------------------------------------------------------
# TODO: Step 1 - Classify a 311 request with Azure OpenAI
# ---------------------------------------------------------------------------
def classify_311_request(request_text: str) -> dict:
    """Send a Memphis 311 service request to Azure OpenAI for classification.

    Args:
        request_text: The citizen's complaint text.

    Returns:
        dict with keys: category, confidence, reasoning
    """
    # TODO: Step 1.1 - Get the OpenAI client
    # TODO: Step 1.2 - Call client.chat.completions.create() with:
    #   model=os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    #   A system message that classifies into: Pothole, Noise Complaint,
    #   Trash/Litter, Street Light, Water/Sewer, Other
    #   response_format={"type": "json_object"}, temperature=0
    # TODO: Step 1.3 - Parse the JSON response with json.loads()
    raise NotImplementedError("Implement classify_311_request in Step 1")


# ---------------------------------------------------------------------------
# TODO: Step 2 - Check content safety
# ---------------------------------------------------------------------------
def check_content_safety(text: str) -> dict:
    """Check text for harmful content using Azure Content Safety.

    Args:
        text: Text to analyze.

    Returns:
        dict with keys: safe (bool), categories (dict of category: severity)
    """
    # TODO: Step 2.1 - Get the Content Safety client
    # TODO: Step 2.2 - Call client.analyze_text() with AnalyzeTextOptions
    # TODO: Step 2.3 - Return safety results
    raise NotImplementedError("Implement check_content_safety in Step 2")


# ---------------------------------------------------------------------------
# TODO: Step 3 - Extract key phrases
# ---------------------------------------------------------------------------
def extract_key_phrases(text: str) -> list[str]:
    """Extract key phrases from text using Azure AI Language.

    Args:
        text: Text to analyze.

    Returns:
        List of key phrase strings.
    """
    # TODO: Step 3.1 - Get the Language client
    # TODO: Step 3.2 - Call client.extract_key_phrases([text])
    # TODO: Step 3.3 - Return the list of key phrases
    raise NotImplementedError("Implement extract_key_phrases in Step 3")


def main():
    """Main function -- call all three Azure AI services."""

    # Optionally load a complaint from data/sample_requests.json
    # Pass an index as a CLI argument: python app/main.py 2
    data_path = os.path.join(_ACTIVITY_DIR, "data", "sample_requests.json")
    if len(sys.argv) > 1 and os.path.exists(data_path):
        with open(data_path) as f:
            samples = json.load(f)
        idx = int(sys.argv[1]) % len(samples)
        sample_request = samples[idx]["text"]
        print(f"Using sample request #{samples[idx]['id']}: {sample_request[:60]}...")
    else:
        sample_request = (
            "There's a huge pothole on Poplar Avenue near the "
            "Walgreens that damaged my tire"
        )

    # Each step is wrapped in try/except so result.json is always written,
    # even if you haven't completed every step yet.

    # Step 1: Classify with Azure OpenAI
    classification = None
    try:
        classification = classify_311_request(sample_request)
        print(f"Step 1 complete: classified as {classification.get('category', 'unknown')}")
    except NotImplementedError:
        print("Step 1 not implemented yet -- skipping classification")
    except Exception as e:
        print(f"Step 1 error: {e}")

    # Step 2: Content safety check
    safety = None
    try:
        safety = check_content_safety(sample_request)
        print(f"Step 2 complete: content safety analyzed ({len(safety.get('categories', {}))} categories)")
    except NotImplementedError:
        print("Step 2 not implemented yet -- skipping content safety")
    except Exception as e:
        print(f"Step 2 error: {e}")

    # Step 3: Key phrase extraction
    key_phrases = None
    try:
        key_phrases = extract_key_phrases(sample_request)
        print(f"Step 3 complete: extracted {len(key_phrases)} key phrases")
    except NotImplementedError:
        print("Step 3 not implemented yet -- skipping key phrases")
    except Exception as e:
        print(f"Step 3 error: {e}")

    # Determine status
    has_classification = (
        isinstance(classification, dict) and classification.get("category")
    )
    has_safety = isinstance(safety, dict) and "safe" in safety
    has_phrases = isinstance(key_phrases, list) and len(key_phrases) > 0

    if has_classification and has_safety and has_phrases:
        status = "success"
    elif has_classification or has_safety or has_phrases:
        status = "partial"
    else:
        status = "error"

    result = {
        "task": "hello_azure_ai",
        "status": status,
        "outputs": {
            "classification": classification,
            "content_safety": safety,
            "key_phrases": key_phrases,
        },
        "metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": os.environ.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4o"),
            "sdk_version": _get_sdk_version(),
        },
    }

    result_path = os.path.join(_ACTIVITY_DIR, "result.json")
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\nResult written to {result_path}")
    _print_dispatch_ticket(sample_request, result)


def _print_dispatch_ticket(complaint_text: str, result: dict):
    """Display result.json as a human-readable Memphis 311 dispatch ticket."""
    outputs = result.get("outputs", {})
    classification = outputs.get("classification") or {}
    safety = outputs.get("content_safety") or {}
    key_phrases = outputs.get("key_phrases") or []

    category = classification.get("category", "—")
    confidence = classification.get("confidence", "—")
    reasoning = classification.get("reasoning", "—")

    if safety.get("safe") is True:
        safety_status = "CLEAR"
    elif safety.get("safe") is False:
        safety_status = "FLAGGED"
    else:
        safety_status = "—"

    phrases_str = ", ".join(key_phrases) if key_phrases else "—"
    complaint_preview = (complaint_text[:70] + "...") if len(complaint_text) > 70 else complaint_text

    print("=" * 60)
    print("  MEMPHIS 311 -- AI DISPATCH TICKET")
    print("=" * 60)
    print(f"  Complaint: {complaint_preview}")
    print("-" * 60)
    print(f"  Category:    {category}")
    print(f"  Confidence:  {confidence}")
    print(f"  Reasoning:   {reasoning}")
    print(f"  Safety:      {safety_status}")
    print(f"  Key phrases: {phrases_str}")
    print("-" * 60)
    print(f"  Status: {result.get('status', 'unknown').upper()}")
    print("=" * 60)


if __name__ == "__main__":
    main()
