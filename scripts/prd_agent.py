from scripts.utils import load_prompt, generate_response, save_output

def run_agent(idea: str, pm_output: str):
    template = load_prompt("prd.md")
    prompt = (
        template.replace("{{idea}}", idea)
                .replace("{{pm_output}}", pm_output)
    )

    output = generate_response(prompt, "openai.gpt-oss-20b-1:0")
    save_output("prd_output", output)

    return output
