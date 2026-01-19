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
#  OUTPUT CLEANING
# ---------------------------------------------------------

def clean_output(text: str) -> str:
    """
    Clean AI output by removing reasoning tags and meta-commentary.
    """
    import re
    
    # Remove <reasoning>...</reasoning> tags and content
    text = re.sub(r'<reasoning>.*?</reasoning>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove <thinking>...</thinking> tags and content
    text = re.sub(r'<thinking>.*?</thinking>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove other common meta tags
    text = re.sub(r'<scratchpad>.*?</scratchpad>', '', text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<draft>.*?</draft>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    # Remove leading "Let me..." or "I'll..." phrases
    text = re.sub(r'^(Let me |I\'ll |I will )[^\n]+\n+', '', text, flags=re.MULTILINE)
    
    # Clean up extra whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text.strip()


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
#  MODEL INVOCATION (Multi-Model Support with Temperature)
# ---------------------------------------------------------

def generate_response(prompt: str, model: str = "mistral.mistral-large-2402-v1:0", temperature: float = 0.7):
    """
    Invoke AI models on AWS Bedrock with customizable parameters.
    
    Supported Models:
    - Mistral Large: mistral.mistral-large-2402-v1:0
    - Mistral Small: mistral.mistral-small-2402-v1:0
    - Amazon Titan: amazon.titan-text-express-v1
    - Claude 3: anthropic.claude-3-sonnet-20240229-v1:0
    - AI21 Jurassic: ai21.j2-ultra-v1
    - Cohere Command: cohere.command-text-v14
    
    Model-Specific Formatting:
    - Mistral: <s>[INST] {prompt} [/INST]
    - Others: Direct prompt (no special formatting)
    """
    
    # Determine model type
    is_mistral = "mistral" in model.lower()
    is_gpt_oss = "gpt-oss" in model.lower() or "openai" in model.lower()
    is_claude = "claude" in model.lower()
    is_titan = "titan" in model.lower()
    is_ai21 = "ai21" in model.lower()
    is_cohere = "cohere" in model.lower()
    
    # Format prompt based on model
    if is_mistral:
        # Mistral requires specific instruction tags
        formatted_prompt = f"<s>[INST] {prompt} [/INST]"
        payload = {
            "prompt": formatted_prompt,
            "max_tokens": 2000,
            "temperature": temperature,
            "top_p": 0.9
        }
    elif is_gpt_oss:
        # GPT-OSS uses OpenAI-style messages format
        payload = {
            "messages": [
                {
                    "role": "system", 
                    "content": """You are a professional AI assistant with GLOBAL perspective and strong research capabilities.

CRITICAL RESEARCH REQUIREMENTS:
- NEVER make up statistics or data - if you don't know, state limitations clearly
- For African, Latin American, and developing markets: use authentic local context (names, cities, payment systems, currencies)
- Identify if concepts are region-specific (e.g., trotro=Ghana only) or universal (e.g., food delivery=global)
- Use real local data sources: African Development Bank, World Bank country reports, local tech publications
- Address real constraints: cash economy, mobile data costs, infrastructure, local regulations

QUALITY STANDARDS:
- Authentic personas with real names from the region (Kwame not John for Ghana)
- Real payment systems (MTN Mobile Money not Stripe for West Africa)
- Real cities and locations (Accra not "urban areas")
- Credible market size estimates with ranges if uncertain
- Local competitive landscape, not just global players

OUTPUT FORMAT:
- Provide direct, clean responses without reasoning tags
- Use proper markdown with generous whitespace
- Include clear section breaks and well-structured tables
- Professional, accessible formatting

Start your response immediately with the requested content."""
                },
                {"role": "user", "content": prompt}
            ],
            "max_completion_tokens": 2000,
            "temperature": temperature,
            "top_p": 0.9,
            "stream": False
        }
    elif is_claude:
        # Claude uses messages format
        payload = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2000,
            "temperature": temperature,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    elif is_titan:
        # Amazon Titan format
        payload = {
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 2000,
                "temperature": temperature,
                "topP": 0.9
            }
        }
    elif is_ai21:
        # AI21 Jurassic format
        payload = {
            "prompt": prompt,
            "maxTokens": 2000,
            "temperature": temperature,
            "topP": 0.9
        }
    elif is_cohere:
        # Cohere Command format
        payload = {
            "prompt": prompt,
            "max_tokens": 2000,
            "temperature": temperature,
            "p": 0.9
        }
    else:
        # Default: treat as Mistral-compatible
        formatted_prompt = f"<s>[INST] {prompt} [/INST]"
        payload = {
            "prompt": formatted_prompt,
            "max_tokens": 2000,
            "temperature": temperature,
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
        elif is_gpt_oss and "choices" in data and len(data["choices"]) > 0:
            # GPT-OSS Output: { "choices": [ { "message": { "content": "..." } } ] }
            output = data["choices"][0]["message"]["content"].strip()
            return clean_output(output)  # Clean reasoning tags from GPT-OSS
        elif is_claude and "content" in data and len(data["content"]) > 0:
            # Claude Output: { "content": [ { "text": "..." } ] }
            return data["content"][0]["text"].strip()
        elif is_titan and "results" in data and len(data["results"]) > 0:
            # Titan Output: { "results": [ { "outputText": "..." } ] }
            return data["results"][0]["outputText"].strip()
        elif is_ai21 and "completions" in data and len(data["completions"]) > 0:
            # AI21 Output: { "completions": [ { "data": { "text": "..." } } ] }
            return data["completions"][0]["data"]["text"].strip()
        elif is_cohere and "generations" in data and len(data["generations"]) > 0:
            # Cohere Output: { "generations": [ { "text": "..." } ] }
            return data["generations"][0]["text"].strip()
        
        # Fallback for unknown format
        if "outputs" in data and len(data["outputs"]) > 0:
            return data["outputs"][0]["text"].strip()
        elif "text" in data:
            return data["text"].strip()
        elif "completion" in data:
            return data["completion"].strip()
            
        raise ValueError(f"Unexpected response structure from {model}: {data.keys()}")

    except Exception as e:
        return f"Error invoking model ({model}): {str(e)}"
