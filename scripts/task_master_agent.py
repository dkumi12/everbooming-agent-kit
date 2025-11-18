from scripts.utils import load_prompt, generate_response, save_output

def run_agent(arch_output: str):
    template = load_prompt("tm.md")
    prompt = template.replace("{{arch_output}}", arch_output)

    output = generate_response(prompt, "openai.gpt-oss-20b-1:0")
    save_output("tasks_output", output)

    return output	
