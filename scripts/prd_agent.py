from scripts.utils import load_prompt, generate_response, save_output

def run_agent(idea: str, pm_output: str):
    template = load_prompt("prd.md")

    # Replace both placeholders
    prompt = (
        template.replace("{{idea}}", idea)
                .replace("{{pm_output}}", pm_output)
    )

    # CALL MISTRAL
    output = generate_response(prompt, "mistral.mistral-large-2402-v1:0")

    save_output("03_prd_output", output)
    return output
