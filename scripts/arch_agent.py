from scripts.utils import load_prompt, generate_response, save_output

def run_agent(prd_output: str):
    template = load_prompt("arch.md")
    prompt = template.replace("{{prd_output}}", prd_output)

    output = generate_response(prompt, "openai.gpt-oss-20b-1:0")
    save_output("architecture_output", output)

    return output
