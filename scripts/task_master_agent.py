from scripts.utils import load_prompt, generate_response, save_output

def run_agent(arch_output: str):
    """
    Takes System Architecture and breaks it down into actionable technical tasks.
    """
    # Load the template (Ensure 'prompts/tm.md' exists)
    template = load_prompt("tm.md")

    # Inject the Architecture result
    prompt = template.replace("{{arch_output}}", arch_output)

    # CALL MISTRAL
    output = generate_response(prompt, "mistral.mistral-large-2402-v1:0")

    # Save output
    save_output("07_task_breakdown", output)
    return output
