import boto3
import json
from pathlib import Path

# Ensure outputs folder exists
Path("outputs").mkdir(exist_ok=True)

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

def load_prompt(path):
    return Path(path).read_text()

def save_output(filename, content):
    Path(f"outputs/{filename}").write_text(content, encoding="utf-8")

def generate_response(prompt, model):
    """
    AWS OpenAI-Compatible GPT-OSS Format (Chat Completions)
    {
        "messages": [{ "role": "user", "content": "..." }],
        "max_tokens": 2048,
        "temperature": 0.3
    }
    """

    body = {
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 2048,
        "temperature": 0.3
    }

    response = bedrock.invoke_model(
        modelId=model,
        body=json.dumps(body),
        accept="application/json",
        contentType="application/json"
    )

    data = json.loads(response["body"].read())

    # Return the chat message content
    return data["choices"][0]["message"]["content"]
