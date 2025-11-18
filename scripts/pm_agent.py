from scripts.utils import load_prompt, generate_response, save_output

def run_agent(idea: str, ba_output: str):
    template = load_prompt("pm.md")
    prompt = (
        template.replace("{{idea}}", idea)
                .replace("{{ba_output}}", ba_output)
    )

    output = generate_response(prompt, "openai.gpt-oss-20b-1:0")
    save_output("pm_output", output)

    return output
