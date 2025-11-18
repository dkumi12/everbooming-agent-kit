import boto3
import json
from botocore.config import Config

# Increase timeouts for large models
config = Config(
    read_timeout=180,         # from 60 → 180 seconds
    connect_timeout=10,
    retries={'max_attempts': 3}
)

bedrock = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    config=config
)

def generate_response(prompt, model):
    body = {
        "input_text": prompt,
        "model": model,
        "max_tokens": 4000,
        "temperature": 0.3
    }

    response = bedrock.invoke_model(
        modelId=model,
        body=json.dumps(body)
    )

    output = json.loads(response["body"].read())
    return output["output_text"]
