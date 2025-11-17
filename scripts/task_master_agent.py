from scripts.utils import load_prompt, generate_response, save_output

def run_agent(sm_output):
    prompt = load_prompt("prompts/tma.md").replace("{{sm_output}}", sm_output)
    output = generate_response(prompt, "openai.gpt-oss-20b-1:0")
    save_output("06-TMA.md", output)
    return output
