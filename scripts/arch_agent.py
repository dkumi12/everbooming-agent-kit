from scripts.utils import load_prompt, generate_response, save_output

def run_agent(prd_output):
    prompt = load_prompt("prompts/arch.md").replace("{{prd_output}}", prd_output)
    output = generate_response(prompt, "openai.gpt-oss-120b-1:0")
    save_output("03-Arch.md", output)
    return output
