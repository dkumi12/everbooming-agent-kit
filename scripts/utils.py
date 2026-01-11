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
#  MODEL INVOCATION (Multi-Model Support)
# ---------------------------------------------------------

def generate_response(prompt: str, model: str = "mistral.mistral-large-2402-v1:0"):
    """
    Invoke AI models on AWS Bedrock with multi-model support.
    
    Supported Models:
    - Mistral Large: mistral.mistral-large-2402-v1:0
    - GPT-OSS 20B: arn:aws:bedrock:us-east-1::foundation-model/gpt-oss-20b
    
    Model-Specific Formatting:
    - Mistral: <s>[INST] {prompt} [/INST]
    - GPT-OSS: Direct prompt (no special formatting)
    """
    
    # Determine model type
    is_mistral = "mistral" in model.lower()
    is_gpt_oss = "gpt-oss" in model.lower()
    
    # Format prompt based on model
    if is_mistral:
        # Mistral requires specific instruction tags
        formatted_prompt = f"<s>[INST] {prompt} [/INST]"
        payload = {
            "prompt": formatted_prompt,
            "max_tokens": 2000,
            "temperature": 0.7,
            "top_p": 0.9
        }
    elif is_gpt_oss:
        # GPT-OSS uses standard messages format
        payload = {
            "prompt": prompt,
            "max_tokens": 2000,
            "temperature": 0.7,
            "top_p": 0.9
        }
    else:
        # Default: treat as Mistral-compatible
        formatted_prompt = f"<s>[INST] {prompt} [/INST]"
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

        # Parse Response
        data = json.loads(response["body"].read())

        # Handle different response formats
        if is_mistral and "outputs" in data and len(data["outputs"]) > 0:
            # Mistral Output: { "outputs": [ { "text": "..." } ] }
            return data["outputs"][0]["text"].strip()
        elif is_gpt_oss:
            # GPT-OSS may use different format - adapt as needed
            if "text" in data:
                return data["text"].strip()
            elif "completion" in data:
                return data["completion"].strip()
            elif "outputs" in data and len(data["outputs"]) > 0:
                return data["outputs"][0]["text"].strip()
        
        # Fallback for unknown format
        if "outputs" in data and len(data["outputs"]) > 0:
            return data["outputs"][0]["text"].strip()
        elif "text" in data:
            return data["text"].strip()
            
        raise ValueError(f"Unexpected response structure from {model}: {data.keys()}")

    except Exception as e:
        return f"Error invoking model ({model}): {str(e)}"
