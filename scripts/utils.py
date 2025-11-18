import os
import json
import boto3
from botocore.config import Config

# ---------------------------------------------------------
#  BEDROCK CLIENT WITH INCREASED TIMEOUTS
# ---------------------------------------------------------

bedrock_config = Config(
    read_timeout=180,          # Allow OSS 20B warm-up
    connect_timeout=10,
    retries={"max_attempts": 3}
)

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    config=bedrock_config
)

# ---------------------------------------------------------
#  PROMPT UTILS
# ---------------------------------------------------------

def load_prompt(filename: str) -> str:
    """Load prompt templates from /prompts folder."""
    path = os.path.join("prompts", filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_output(name: str, content: str):
    """Save output in /outputs folder."""
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", f"{name}.md")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------
#  MODEL CALL (OSS MODELS)
# ---------------------------------------------------------

def generate_response(prompt: str, model: str):
    """
    Invoke OSS OpenAI models on AWS Bedrock using the
    updated 'messages' format.
    """

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2000,
        "temperature": 0.3
    }

    response = bedrock.invoke_model(
        modelId=model,
        body=json.dumps(payload),
        accept="application/json",
        contentType="application/json"
    )

    data = json.loads(response["body"].read())

    # Ensure compatible with OSS output format
    try:
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        raise ValueError(f"Unexpected OSS model output format: {data}") from e
