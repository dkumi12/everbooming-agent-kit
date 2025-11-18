import os
import json
import boto3
from botocore.config import Config

# ---------------------------------------------------------
#  AWS BEDROCK CLIENT (Optimized for Mistral Models)
# ---------------------------------------------------------

bedrock_config = Config(
    read_timeout=180,
    connect_timeout=10,
    retries={"max_attempts": 3}
)

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    config=bedrock_config
)

# ---------------------------------------------------------
#  PROMPT LOADING
# ---------------------------------------------------------

def load_prompt(filename: str) -> str:
    """
    Load prompt templates from /prompts folder.
    """
    path = os.path.join("prompts", filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------
#  SAVE OUTPUT HELPERS
# ---------------------------------------------------------

def save_output(name: str, content: str):
    """
    Save AI output into /outputs/<name>.md
    """
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", f"{name}.md")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------
#  MISTRAL MODEL INVOCATION
# ---------------------------------------------------------

def generate_response(prompt: str, model: str = "mistral.mistral-large-2402-v1:0"):
    """
    Invoke Mistral models on AWS Bedrock.
    
    Mistral Specifics:
    - Format: <s>[INST] {prompt} [/INST]
    - Input Key: "prompt"
    - Output Key: "outputs"[0]["text"]
    """

    # 1. Format the Prompt (Mistral Instruct Syntax)
    # Mistral requires these specific tags to know where the user input starts/ends
    formatted_prompt = f"<s>[INST] {prompt} [/INST]"

    # 2. Construct Payload
    payload = {
        "prompt": formatted_prompt,
        "max_tokens": 2000,
        "temperature": 0.7,
        "top_p": 0.9
    }

    try:
        response = bedrock.invoke_model(
            modelId=model,
            body=json.dumps(payload),
            accept="application/json",
            contentType="application/json"
        )

        # 3. Parse Response
        data = json.loads(response["body"].read())

        # Mistral Output Schema:
        # { "outputs": [ { "text": "Result string...", ... } ] }
        if "outputs" in data and len(data["outputs"]) > 0:
            # Strip the leading whitespace usually returned by Mistral
            return data["outputs"][0]["text"].strip()
            
        raise ValueError(f"Unexpected Mistral response structure: {data.keys()}")

    except Exception as e:
        return f"Error invoking Mistral ({model}): {str(e)}"
