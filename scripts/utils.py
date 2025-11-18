import os
import json
import boto3


# ---------------------------------------------------------
#  PROMPT LOADER
# ---------------------------------------------------------
def load_prompt(file_name: str) -> str:
    """
    Loads a prompt template from the /prompts directory.
    """
    path = os.path.join("prompts", file_name)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------
#  OUTPUT SAVER
# ---------------------------------------------------------
def save_output(name: str, content: str):
    """
    Saves the agent output into /outputs/<name>.md.
    """
    os.makedirs("outputs", exist_ok=True)

    output_path = os.path.join("outputs", f"{name}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)


# ---------------------------------------------------------
#  AWS BEDROCK CLIENT
# ---------------------------------------------------------
bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")


# ---------------------------------------------------------
#  MODEL INVOCATION
# ---------------------------------------------------------
def generate_response(prompt: str, model: str):
    """
    Sends a prompt to AWS Bedrock's OpenAI gpt-oss-* model
    using the new "messages" API format.
    """

    body = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2048
    }

    response = bedrock.invoke_model(
        body=json.dumps(body),
        modelId=model,
        accept="application/json",
        contentType="application/json"
    )

    result = json.loads(response["body"].read())

    # New OpenAI-style OSS response format
    try:
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        raise ValueError(f"Unexpected response format: {result}") from e
