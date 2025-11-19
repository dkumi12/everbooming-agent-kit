from scripts.utils import load_prompt, generate_response, save_output

def run_agent(po_output: str):
    # FIX: Removed "prompts/" from the filename
    prompt = load_prompt("sm.md").replace("{{po_output}}", po_output)

    output = generate_response(prompt, "mistral.mistral-large-2402-v1:0")

    save_output("06_SM_sprints", output)
    return output
