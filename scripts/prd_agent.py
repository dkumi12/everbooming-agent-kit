from scripts.utils import load_prompt, generate_response, save_output

def run_agent(ba_output, pm_output):
    prompt = load_prompt("prompts/prd.md") \
        .replace("{{ba_output}}", ba_output) \
        .replace("{{pm_output}}", pm_output)

    output = generate_response(prompt, "openai.gpt-oss-120b-1:0")
    save_output("02-PRD.md", output)
    return output
