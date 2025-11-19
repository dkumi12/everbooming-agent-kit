from scripts.utils import load_prompt, generate_response, save_output

def run_agent(arch_output: str):
    # Note: Ensure prompts/po.md exists
    prompt = load_prompt("prompts/po.md").replace("{{arch_output}}", arch_output)

    # CALL MISTRAL
    output = generate_response(prompt, "mistral.mistral-large-2402-v1:0")

    save_output("05_PO_stories", output)
    return output
