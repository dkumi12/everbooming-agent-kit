from scripts.utils import load_prompt, generate_response, save_output

def run_agent(po_output):
    prompt = load_prompt("prompts/sm.md").replace("{{po_output}}", po_output)
    output = generate_response(prompt, "openai.gpt-oss-20b-1:0")
    save_output("05-SM.md", output)
    return output
