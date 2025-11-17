from scripts.utils import load_prompt, generate_response, save_output

def run_agent(idea):
    prompt = load_prompt("prompts/ba.md").replace("{{idea}}", idea)
    output = generate_response(prompt, "openai.gpt-oss-20b-1:0")
    save_output("01-BA.md", output)
    return output

