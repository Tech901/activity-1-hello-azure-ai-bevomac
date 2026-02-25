---
title: "SDK vs REST API Reference"
type: reference
version: "1.0.0"
parent_activity: "Activity 1 - Hello, Azure AI"
ai102_objectives:
  - "1.2 - Plan, create and deploy a Microsoft Foundry Service"
---

# SDK vs REST API -- When to Use Which

Azure AI services can be called two ways: with an **SDK** (a Python library) or with **raw HTTP requests** (the REST API). This reference shows both approaches side by side so you can see what the SDK handles for you.

## Side-by-Side: Classify a 311 Request

### Using the OpenAI Python SDK (what you use in Activity 1)

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-10-21",
)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Classify this Memphis 311 request..."},
        {"role": "user", "content": complaint_text},
    ],
    response_format={"type": "json_object"},
    temperature=0,
)

result = json.loads(response.choices[0].message.content)
print(result["category"])  # "Pothole"
```

**Lines of code:** ~15

### Using raw HTTP with `requests`

```python
import requests

url = f"{os.environ['AZURE_OPENAI_ENDPOINT']}/openai/deployments/gpt-4o/chat/completions"
headers = {
    "Content-Type": "application/json",
    "api-key": os.environ["AZURE_OPENAI_API_KEY"],
}
params = {"api-version": "2024-10-21"}

body = {
    "messages": [
        {"role": "system", "content": "Classify this Memphis 311 request..."},
        {"role": "user", "content": complaint_text},
    ],
    "response_format": {"type": "json_object"},
    "temperature": 0,
}

resp = requests.post(url, headers=headers, params=params, json=body, timeout=30)
resp.raise_for_status()

data = resp.json()
result = json.loads(data["choices"][0]["message"]["content"])
print(result["category"])  # "Pothole"
```

**Lines of code:** ~22

---

## What the SDK Handles for You

| Concern | SDK | Raw HTTP |
|---------|-----|----------|
| **URL construction** | Builds the full URL from endpoint + deployment | You construct it manually |
| **Authentication** | Passes `api-key` header automatically | You set headers yourself |
| **API versioning** | Managed via `api_version` parameter | You add `?api-version=` to every request |
| **Retry logic** | Built-in exponential backoff on 429/5xx | You implement retries yourself |
| **Response parsing** | Returns typed objects (`ChatCompletion`) | You parse raw JSON dicts |
| **Error handling** | Raises specific exceptions (`AuthenticationError`, `RateLimitError`) | You check `resp.status_code` manually |
| **Streaming** | `stream=True` gives you an iterator | You handle chunked transfer encoding |
| **Type hints** | Full IDE autocomplete and type checking | No type safety on response fields |

---

## When Would You Use Raw HTTP?

The SDK is the right choice for most production code. But there are legitimate reasons to use the REST API directly:

1. **No SDK exists** -- Some Azure AI features ship a REST endpoint before the SDK is updated. You can start building immediately instead of waiting.

2. **Debugging** -- When something goes wrong, seeing the raw request and response headers can reveal issues (wrong API version, unexpected redirects, auth failures) that the SDK abstracts away.

3. **Custom middleware** -- If you need to route requests through a proxy, add custom logging, or modify headers for compliance, raw HTTP gives you full control.

4. **Lightweight environments** -- In a serverless function with strict package size limits, `requests` (or the built-in `urllib`) adds less overhead than the full Azure SDK chain.

5. **Cross-language consistency** -- If your team works in a language without a mature SDK (e.g., Rust, Elixir), the REST API is the universal interface.

---

## AI-102 Exam Connection

Domain 1.2 tests whether you understand the difference between SDK and REST approaches:

- **Know both patterns**: The exam may show you a code snippet using `requests.post()` and ask what is wrong, or show SDK code and ask which parameter controls behavior.
- **Know the trade-offs**: SDKs provide convenience and safety; REST provides flexibility and transparency.
- **Know the URL structure**: Azure OpenAI REST URLs follow the pattern `{endpoint}/openai/deployments/{model}/chat/completions?api-version={version}`. Cognitive Services endpoints use `{endpoint}/{service-path}?api-version={version}`.

---

## Content Safety: SDK vs REST

For comparison, here is the same pattern with Azure Content Safety:

### SDK

```python
from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.credentials import AzureKeyCredential

client = ContentSafetyClient(
    endpoint=os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AZURE_CONTENT_SAFETY_KEY"]),
)
result = client.analyze_text(AnalyzeTextOptions(text="Some text to check"))
```

### REST

```python
url = f"{os.environ['AZURE_CONTENT_SAFETY_ENDPOINT']}/contentsafety/text:analyze"
headers = {
    "Content-Type": "application/json",
    "Ocp-Apim-Subscription-Key": os.environ["AZURE_CONTENT_SAFETY_KEY"],
}
params = {"api-version": "2024-09-01"}
body = {"text": "Some text to check"}

resp = requests.post(url, headers=headers, params=params, json=body, timeout=30)
```

Notice the differences: the auth header name changes (`api-key` for OpenAI vs `Ocp-Apim-Subscription-Key` for Cognitive Services), the URL structure is different, and the API version is different. The SDK abstracts all of this.

---

## Key Takeaway

Use the SDK unless you have a specific reason not to. The SDK gives you retries, typed responses, and proper error handling -- exactly the things that are easy to forget when writing raw HTTP calls at 2 AM before a deadline.
