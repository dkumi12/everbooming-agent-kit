from scripts.utils import load_prompt, generate_response, save_output

def run_agent(idea: str):
    # Load prompt
    prompt_template = load_prompt("ba.md")
    prompt = prompt_template.replace("{{idea}}", idea)

    # CALL GPT-OSS-20B
    output = generate_response(prompt, "openai.gpt-oss-20b-1:0", temperature=0.7)

    save_output("01_business_analysis", output)
    return output
