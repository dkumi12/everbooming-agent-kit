"""
AWS Bedrock Model Configuration
Available models and their use cases
"""

# Available AWS Bedrock Models (as of January 2025)
AVAILABLE_MODELS = {
    # Mistral AI Models
    "mistral-large": "mistral.mistral-large-2402-v1:0",
    "mistral-small": "mistral.mistral-small-2402-v1:0",
    
    # Amazon Titan Models
    "titan-text-express": "amazon.titan-text-express-v1",
    "titan-text-lite": "amazon.titan-text-lite-v1",
    
    # Anthropic Claude Models
    "claude-3-sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
    "claude-3-haiku": "anthropic.claude-3-haiku-20240307-v1:0",
    
    # AI21 Labs Jurassic Models
    "jurassic-2-ultra": "ai21.j2-ultra-v1",
    "jurassic-2-mid": "ai21.j2-mid-v1",
    
    # Cohere Command Models
    "command": "cohere.command-text-v14",
    "command-light": "cohere.command-light-text-v14",
}

# Agent-to-Model Mapping
AGENT_MODELS = {
    "ba": "mistral-large",           # Business Analyst
    "pm": "mistral-large",           # Project Manager  
    "prd": "mistral-large",          # PRD Generator
    "arch": "mistral-large",         # System Architect
    "tma": "mistral-large",          # Task Master
    "po": "mistral-large",           # Product Owner
    "sm": "mistral-large",           # Scrum Master
}

# Model-Specific Temperature Settings
TEMPERATURE_SETTINGS = {
    "ba": 0.7,      # Balanced for business analysis
    "pm": 0.6,      # Lower for structured planning
    "prd": 0.6,     # Lower for precise requirements
    "arch": 0.8,    # Higher for creative architecture
    "tma": 0.5,     # Lower for structured task breakdown
    "po": 0.7,      # Balanced for user stories
    "sm": 0.6,      # Lower for structured sprint planning
}

def get_model_for_agent(agent_key: str) -> str:
    """Get the model ID for a specific agent"""
    model_name = AGENT_MODELS.get(agent_key, "mistral-large")
    return AVAILABLE_MODELS[model_name]

def get_temperature_for_agent(agent_key: str) -> float:
    """Get the temperature setting for a specific agent"""
    return TEMPERATURE_SETTINGS.get(agent_key, 0.7)
