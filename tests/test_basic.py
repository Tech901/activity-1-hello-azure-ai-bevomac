"""Visible tests for Activity 1 - Hello, Azure AI."""
import json
import os
import re

import pytest

RESULT_PATH = os.path.join(os.path.dirname(__file__), "..", "result.json")
MAIN_PATH = os.path.join(os.path.dirname(__file__), "..", "app", "main.py")


@pytest.fixture
def result():
    if not os.path.exists(RESULT_PATH):
        pytest.skip("result.json not found - run 'python app/main.py' first")
    with open(RESULT_PATH) as f:
        return json.load(f)


def test_result_exists():
    """Canary: result.json must exist."""
    assert os.path.exists(RESULT_PATH), (
        "Run 'python app/main.py' to generate result.json"
    )


def test_required_fields(result):
    for field in ("task", "status", "outputs", "metadata"):
        assert field in result, f"Missing required field: {field}"


def test_task_name(result):
    assert result["task"] == "hello_azure_ai"


def test_status_valid(result):
    assert result["status"] in ("success", "partial", "error")


def test_outputs_has_classification(result):
    assert "classification" in result["outputs"]
    assert result["outputs"]["classification"] is not None, (
        "classification is None -- check Step 1"
    )


def test_outputs_has_content_safety(result):
    assert "content_safety" in result["outputs"]
    assert result["outputs"]["content_safety"] is not None, (
        "content_safety is None -- check Step 2"
    )


def test_outputs_has_key_phrases(result):
    assert "key_phrases" in result["outputs"]
    assert result["outputs"]["key_phrases"] is not None, (
        "key_phrases is None -- check Step 3"
    )


def test_classification_confidence_range(result):
    """Confidence should be 0-1 (not a percentage like 95)."""
    classification = result.get("outputs", {}).get("classification")
    if not classification:
        pytest.skip("No classification output yet")
    confidence = classification.get("confidence")
    if confidence is None:
        pytest.skip("No confidence value in classification")
    assert isinstance(confidence, (int, float)), (
        f"confidence should be a number, got {type(confidence).__name__}"
    )
    assert 0.0 <= confidence <= 1.0, (
        f"confidence should be between 0.0 and 1.0, got {confidence} "
        "(did you return a percentage instead of a decimal?)"
    )


def test_key_phrases_is_list_of_strings(result):
    """Key phrases should be a list of strings, not a nested structure."""
    key_phrases = result.get("outputs", {}).get("key_phrases")
    if not key_phrases:
        pytest.skip("No key_phrases output yet")
    assert isinstance(key_phrases, list), (
        f"key_phrases should be a list, got {type(key_phrases).__name__}"
    )
    for i, phrase in enumerate(key_phrases):
        assert isinstance(phrase, str), (
            f"key_phrases[{i}] should be a string, got {type(phrase).__name__}: {phrase!r}"
        )


def test_no_hardcoded_keys():
    with open(MAIN_PATH) as f:
        source = f.read()
    suspicious = [
        r'["\']https?://\S+\.cognitiveservices\.azure\.com\S*["\']',
        r'["\'][A-Fa-f0-9]{32}["\']',
    ]
    for pattern in suspicious:
        matches = re.findall(pattern, source)
        real = [
            m for m in matches
            if "example" not in m.lower() and "your-" not in m.lower()
        ]
        assert len(real) == 0, (
            f"Possible hardcoded credential: {real[0][:50]}"
        )
