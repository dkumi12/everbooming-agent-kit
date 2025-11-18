import os
import json
import boto3
from botocore.config import Config

# ---------------------------------------------------------
#  BEDROCK CLIENT WITH INCREASED TIMEOUTS
# ---------------------------------------------------------

bedrock_config = Config(
    read_timeout=180,      # OSS 20B needs warm-up time
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
    path = os.path.join("prompts", filename)
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_output(name: str, content: str):
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", f"{name}.md")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------
#    OSS MODEL CALL  (CORRECT FORMAT)
# ---------------------------------------------------------

def generate_response(prompt: str, model: str):
    """
    OSS MODELS **DO NOT USE messages[]**
    They require { "text": ... }
    """

    payload = {
        "text": prompt,            # <-- FIX: OSS uses simple text
        "max_tokens": 4000,
        "temperature": 0.3
    }

    response = bedrock.invoke_model(
        modelId=model,
        body=json.dumps(payload),
        accept="application/json",
        contentType="application/json"
    )

    data = json.loads(response["body"].read())

    # OSS returns:  { "output_text": "..." }
    if "output_text" in data:
        return data["output_text"]

    # Fallback for variations
    if "completion" in data:
        return data["completion"]

    raise ValueError(f"Unexpected OSS output format: {data}")
