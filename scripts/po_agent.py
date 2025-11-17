from scripts.utils import load_prompt, generate_response, save_output

def run_agent(arch_output):
    prompt = load_prompt("prompts/po.md").replace("{{arch_output}}", arch_output)
    output = generate_response(prompt, "openai.gpt-oss-20b-1:0")
    save_output("04-PO.md", output)
    return output

