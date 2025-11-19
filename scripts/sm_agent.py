from scripts.utils import load_prompt, generate_response, save_output

def run_agent(po_output: str):
    # Note: Ensure prompts/sm.md exists
    prompt = load_prompt("prompts/sm.md").replace("{{po_output}}", po_output)

    # CALL MISTRAL
    output = generate_response(prompt, "mistral.mistral-large-2402-v1:0")

    save_output("06_SM_sprints", output)
    return output
