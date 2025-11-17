from scripts.utils import load_prompt, generate_response, save_output

def run_agent(ba_output):
    prompt = load_prompt("prompts/pm.md").replace("{{ba_output}}", ba_output)
    output = generate_response(prompt, "openai.gpt-oss-20b-1:0")
    save_output("02-PM.md", output)
    return output
