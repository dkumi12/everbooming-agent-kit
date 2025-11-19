from scripts.utils import load_prompt, generate_response, save_output

def run_agent(idea: str):
    # Load prompt
    prompt_template = load_prompt("ba.md")
    prompt = prompt_template.replace("{{idea}}", idea)

    # CALL MISTRAL
    output = generate_response(prompt, "mistral.mistral-large-2402-v1:0")

    save_output("01_business_analysis", output)
    return output
