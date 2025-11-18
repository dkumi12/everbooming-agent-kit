from scripts.utils import load_prompt, generate_response, save_output

def run_agent(idea: str):
    prompt_template = load_prompt("ba.md")
    prompt = prompt_template.replace("{{idea}}", idea)

    output = generate_response(prompt, "openai.gpt-oss-20b-1:0")

    save_output("business_analysis", output)
    return output
