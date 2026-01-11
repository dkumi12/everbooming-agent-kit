from scripts.utils import load_prompt, generate_response, save_output
from scripts.context7_client import fetch_tech_docs
import os
import re


def extract_tech_stack(prd_output: str) -> list[str]:
    """
    Extract technology stack mentions from PRD.
    Uses pattern matching to identify common technologies.
    """
    tech_keywords = {
        "react", "nextjs", "next.js", "vue", "angular", "svelte",
        "fastapi", "django", "flask", "express", "nestjs", "nodejs",
        "postgresql", "postgres", "mongodb", "mysql", "redis", "sqlite",
        "docker", "kubernetes", "k8s", "aws", "terraform", "nginx",
        "typescript", "python", "golang", "go", "rust", "java",
        "graphql", "rest", "api", "tailwind", "bootstrap"
    }
    
    # Convert to lowercase for matching
    prd_lower = prd_output.lower()
    
    # Find mentioned technologies
    found_tech = []
    for tech in tech_keywords:
        if tech in prd_lower:
            # Normalize names (next.js -> nextjs, etc)
            normalized = tech.replace(".", "")
            if normalized not in found_tech:
                found_tech.append(normalized)
    
    # Default stack if nothing specific found
    if not found_tech:
        found_tech = ["react", "fastapi", "postgresql", "docker"]
    
    return found_tech[:5]  # Limit to top 5 to avoid token overflow


def run_agent(prd_output: str, use_context7: bool = None):
    """
    Enhanced Architecture Agent with Context7 documentation fetching.
    
    Args:
        prd_output: Output from PRD agent
        use_context7: Whether to fetch live documentation 
                      (default: read from ENABLE_CONTEXT7 env var)
    """
    # Load base prompt
    template = load_prompt("arch.md")
    
    # Determine if Context7 should be used
    if use_context7 is None:
        use_context7 = os.getenv("ENABLE_CONTEXT7", "true").lower() == "true"
    
    # Extract tech stack from PRD
    tech_stack = extract_tech_stack(prd_output)
    
    # Fetch live documentation if enabled
    context7_docs = ""
    if use_context7 and tech_stack:
        try:
            print(f"\n📚 Context7: Fetching documentation for {len(tech_stack)} technologies...")
            print(f"   Technologies: {', '.join(tech_stack)}")
            
            context7_docs = fetch_tech_docs(
                tech_stack, 
                context="Designing system architecture for a production application"
            )
            
            if context7_docs and "unavailable" not in context7_docs.lower():
                print("✅ Context7: Documentation fetched successfully\n")
            else:
                print("⚠️  Context7: No documentation available, proceeding without it\n")
                context7_docs = ""
                
        except Exception as e:
            print(f"⚠️  Context7 fetch failed: {e}")
            print("   Proceeding without live documentation\n")
            context7_docs = ""
    
    # Enhanced prompt with documentation context
    if context7_docs:
        enhanced_prompt = f"""{template}

---

## 📚 LIVE TECHNICAL DOCUMENTATION (Context7)

The following up-to-date documentation has been fetched for the recommended tech stack:

{context7_docs}

---

**IMPORTANT**: Use this live documentation to ensure your architecture recommendations:
- Follow current best practices and patterns
- Use correct API syntax and methods
- Align with latest framework capabilities
- Reflect modern deployment strategies

"""
    else:
        enhanced_prompt = template
    
    # Replace PRD placeholder
    prompt = enhanced_prompt.replace("{{prd_output}}", prd_output)
    
    # Call GPT-OSS-20B for architecture design
    print("🤖 Generating architecture design with GPT-OSS-20B...\n")
    output = generate_response(prompt, "openai.gpt-oss-20b-1:0", temperature=0.8)
    
    # Save outputs
    save_output("04_architecture_design", output)
    
    # Also save what tech docs were used for reference
    if context7_docs:
        save_output("04_architecture_docs_context", context7_docs)
        print("📄 Saved: Architecture design + Context7 documentation reference\n")
    else:
        print("📄 Saved: Architecture design\n")
    
    return output
