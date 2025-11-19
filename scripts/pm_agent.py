from scripts.utils import load_prompt, generate_response, save_output

def run_agent(ba_output: str):
    """
    Takes Business Analysis output and creates a Project Management Plan.
    """
    # Load the template (Ensure 'prompts/pm.md' exists)
    template = load_prompt("pm.md")

    # Inject the Business Analysis result
    prompt = template.replace("{{ba_output}}", ba_output)

    # CALL MISTRAL
    output = generate_response(prompt, "mistral.mistral-large-2402-v1:0")

    # Save output
    save_output("02_pm_plan", output)
    return output
