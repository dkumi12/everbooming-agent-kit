from scripts.utils import load_prompt, generate_response, save_output

def run_agent(prd_output: str):
    template = load_prompt("arch.md")
    prompt = template.replace("{{prd_output}}", prd_output)

    # CALL MISTRAL
    output = generate_response(prompt, "mistral.mistral-large-2402-v1:0")

    save_output("04_architecture_output", output)
    return output
