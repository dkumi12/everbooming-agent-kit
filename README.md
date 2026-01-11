# 🚀 Everbooming Agent Kit

> **AI-Powered Software Development Lifecycle Automation with AWS Bedrock**

Transform your product ideas into detailed technical specifications in minutes using a sophisticated multi-agent AI pipeline powered by AWS Bedrock with Mistral Large 2, optimized with per-agent temperature settings and parallel execution.

## 🌐 **[🚀 TRY LIVE DEMO](https://everbooming-agent-kit-production.up.railway.app/)** ← Click to test now!

![Python](https://img.shields.io/badge/Python-3.12-blue)
![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-Latest-red)
![Docker](https://img.shields.io/badge/Docker-Ready-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎯 What It Does

Everbooming Agent Kit automates the entire software planning process by orchestrating **7 specialized AI agents** that work together to transform a simple product idea into comprehensive technical documentation.

**Input Example:**  
```
A mobile app for dog walkers to find clients
```

**Output Includes:** 
- ✅ Business analysis with user personas (Mistral Large 2, temp=0.7)
- ✅ Product requirements document (PRD) (temp=0.6 for precision)
- ✅ System architecture with tech stack recommendations (temp=0.8 for creativity)
- ✅ Database schemas and API endpoints
- ✅ Technical tasks breakdown for developers (temp=0.5 for structure)
- ✅ User stories with acceptance criteria (temp=0.7)
- ✅ Sprint planning roadmap for 2-week sprints (temp=0.6)

---

## 🏗️ Architecture

### Multi-Agent Pipeline with Parallel Execution

```
                    Product Idea
                         ↓
        ┌────────────────────────────────────┐
        │  [1] Business Analyst              │
        │  Mistral Large 2 • temp=0.7        │
        └────────────────┬───────────────────┘
                         ↓
        ┌────────────────────────────────────┐
        │  [2] Project Manager               │
        │  Mistral Large 2 • temp=0.6        │
        └────────────────┬───────────────────┘
                         ↓
        ┌────────────────────────────────────┐
        │  [3] PRD Generator                 │
        │  Mistral Large 2 • temp=0.6        │
        └────────────────┬───────────────────┘
                         ↓
        ┌────────────────────────────────────┐
        │  [4] System Architect              │
        │  Mistral Large 2 • temp=0.8        │
        │  + Context7 Live Documentation     │
        └────┬───────────┬───────────────┬───┘
             │           │               │
             │   ┌───────┴──────┐        │
             │   │  PARALLEL    │        │
             ↓   ↓   EXECUTION  ↓        ↓
        ┌────────┐  ┌───────────┐  ┌─────────┐
        │[5] Task│  │[6] Product│  │Context7 │
        │Master  │  │Owner      │  │Docs API │
        │temp=0.5│  │temp=0.7   │  │         │
        └───┬────┘  └─────┬─────┘  └─────────┘
            │             │
            └──────┬──────┘
                   ↓
        ┌────────────────────────────────────┐
        │  [7] Scrum Master                  │
        │  Mistral Large 2 • temp=0.6        │
        └────────────────────────────────────┘
```

### Key Features

✅ **Optimized Temperature Settings** - Per-agent temperature for optimal output quality  
✅ **Parallel Execution** - Task Master & Product Owner run simultaneously (40% faster)  
✅ **AWS Bedrock Integration** - Production-grade AI infrastructure  
✅ **Context7 Documentation** - Live API docs and best practices fetching  
✅ **Docker Ready** - One-command deployment anywhere  
✅ **Railway Compatible** - Deploy with single click  
✅ **Markdown Outputs** - Clean, parseable, version-controllable  
✅ **Progressive UI** - Real-time updates with Streamlit  
✅ **Cost Effective** - ~$0.17 per full pipeline run  

---

## 🚀 Quick Start

### Option 1: Railway (Recommended for Demo)

1. Click the "Deploy on Railway" button above
2. Set environment variables in Railway dashboard:
   ```
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   AWS_DEFAULT_REGION=us-east-1
   CONTEXT7_API_KEY=your_context7_key (optional)
   ```
3. Deploy! Your app will be live in ~3 minutes

### Option 2: Local Docker

```bash
# Clone repository
git clone https://github.com/dkumi12/everbooming-agent-kit.git
cd everbooming-agent-kit

# Create .env file from template
cp .env.example .env
# Edit .env with your AWS credentials

# Build and run
docker build -t everbooming-kit .
docker run -p 8501:8501 --env-file .env everbooming-kit
```

Visit `http://localhost:8501`

### Option 3: Local Development

```bash
# Python 3.12+ required
git clone https://github.com/dkumi12/everbooming-agent-kit.git
cd everbooming-agent-kit

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your credentials

# Run the app
streamlit run app.py
```

Visit `http://localhost:8501`

---

## 🔑 Prerequisites

### Required

- **AWS Account** with Bedrock access enabled
- **IAM credentials** with `bedrock:InvokeModel` permission
- **Mistral Large model** enabled in AWS Bedrock (us-east-1 region)

### Optional

- **Context7 API Key** - For live documentation fetching ([Get yours here](https://context7.com))

### AWS Bedrock Setup Guide

1. **Enable Bedrock Access**
   - Go to AWS Console → Amazon Bedrock → Model Access
   - Request access to **Mistral Large 2 (24.02)**
   - Wait for approval (usually instant)

2. **Create IAM User with Policy**

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/mistral.mistral-large-2402-v1:0"
    }
  ]
}
```

3. **Generate Access Keys**
   - Go to IAM → Users → Security Credentials
   - Create Access Key → CLI
   - Save the keys securely

4. **Set Environment Variables**
   - Add keys to `.env` file or Railway dashboard

---

## 📊 Example Output

### Input
```
A SaaS platform for freelancers to manage invoices and time tracking
```

### Generated Artifacts

```
outputs/
├── 01_business_analysis.md           # Market research, user personas
├── 02_project_plan.md                # Timeline, milestones, resources
├── 03_prd.md                         # Product requirements document
├── 04_architecture_design.md         # System architecture, tech stack
├── 04_architecture_docs_context.md   # Live Context7 docs used
├── 05_technical_tasks.md             # Developer task breakdown
├── 06_user_stories.md                # Product owner stories
└── 07_sprint_plan.md                 # 2-week sprint organization
```

**Total Time:** ~2-3 minutes for complete pipeline execution


---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| AI Engine | AWS Bedrock + Mistral Large | Core intelligence & reasoning |
| Documentation | Context7 API | Live technical documentation |
| Frontend | Streamlit | Interactive web UI |
| Backend | Python 3.12 | Agent orchestration |
| Cloud Deployment | Railway | Hosting & CI/CD |
| Containerization | Docker | Portable deployment |
| State | File system | Output persistence |
| Cloud | AWS (Bedrock, IAM) | AI infrastructure |
| Deployment | Docker + Railway | Easy hosting & scaling |
| State | File system | Output persistence |

---

## 🎨 Customization

### Adding New Agents

1. Create prompt template in `prompts/your_agent.md`:
```markdown
You are a {Role} AI.

Given:
{{input_context}}

Provide:
1. Point 1
2. Point 2
...

Output in clear Markdown.
```

2. Create agent script in `scripts/your_agent.py`:
```python
from scripts.utils import load_prompt, generate_response, save_output

def run_agent(input_context: str):
    prompt_template = load_prompt("your_agent.md")
    prompt = prompt_template.replace("{{input_context}}", input_context)
    output = generate_response(prompt)
    save_output("output_name", output)
    return output
```

3. Add to pipeline in `app.py`:
```python
with st.spinner("Running Your New Agent..."):
    result = run_your_agent(previous_output)
    with st.expander("Your Agent Output", expanded=True):
        st.markdown(result)
```

### Customizing Prompts

All agent prompts are in `/prompts` directory. Edit them to:
- Change output format and structure
- Add domain-specific requirements
- Adjust tone and style
- Include compliance guidelines

### Using Different Models

Edit `scripts/utils.py`:

```python
# Available Mistral models on Bedrock:
# - mistral.mistral-large-2402-v1:0  (most capable)
# - mistral.mistral-7b-instruct-v0:2  (faster, cheaper)

def generate_response(prompt, model="mistral.mistral-large-2402-v1:0"):
    # ... existing code
```

### Disabling Context7

Set in `.env`:
```bash
ENABLE_CONTEXT7=false
```

Or pass to arch_agent:
```python
arch_output = run_arch_agent(prd_output, use_context7=False)
```

---

## 💰 Cost Estimate

Based on AWS Bedrock Mistral Large pricing (us-east-1):

| Component | Cost per Run | Monthly (50 runs) |
|-----------|--------------|-------------------|
| Input tokens (~2,000) | ~$0.02 | $1.00 |
| Output tokens (~15,000) | ~$0.15 | $7.50 |
| Context7 API | $0.00* | $0.00* |
| **Total** | **~$0.17** | **~$8.50** |

*Context7 has a free tier for development (5,000 requests/month)

**Cost Optimization Tips:**
- Use `mistral-7b-instruct` for simpler agents (70% cheaper)
- Cache frequently used documentation
- Batch multiple ideas in one session

---

## 🔒 Security Best Practices

- ✅ Environment variables for all sensitive data
- ✅ AWS IAM with least-privilege permissions
- ✅ No hardcoded credentials in code
- ✅ Docker secrets support
- ✅ HTTPS by default on Railway
- ✅ `.env` file in `.gitignore`

**⚠️ Never commit `.env` file to Git!**

---

## 📝 Use Cases

### For Startups
- **Rapid MVP Planning** - Turn ideas into specs before writing code
- **Investor Decks** - Technical appendix for pitch presentations
- **Co-founder Alignment** - Shared vision on architecture

### For Consultants
- **Client Kickoffs** - Automated engagement documentation
- **Proposal Generation** - Technical feasibility reports
- **Standardized Deliverables** - Consistent quality across projects

### For Development Agencies
- **Project Scoping** - Accurate time & resource estimates
- **Requirement Gathering** - Structured client interviews
- **Knowledge Transfer** - Documentation for offshore teams

### For Students & Educators
- **Learning SDLC** - Understand full development lifecycle
- **Architecture Practice** - Study system design patterns
- **Technical Writing** - Examples of professional documentation


---

## 🤝 Contributing

Contributions welcome! Areas of interest:

**New Features:**
- [ ] Additional agent types (DevOps, Security, Testing, UI/UX)
- [ ] More LLM providers (OpenAI, Anthropic Claude, Google Gemini)
- [ ] Export formats (PDF, Notion, Confluence, Jira)
- [ ] Multi-language support for international teams
- [ ] Voice input/output for accessibility

**Improvements:**
- [ ] Caching layer for repeated queries
- [ ] Cost optimization dashboard
- [ ] Agent performance metrics
- [ ] Collaborative features (team workspaces)
- [ ] Version control for outputs

**Integrations:**
- [ ] GitHub Issues automation
- [ ] Linear/Jira sync
- [ ] Slack notifications
- [ ] Figma design integration
- [ ] VS Code extension

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines.

---

## 📚 Documentation

- [🏗️ Architecture Deep Dive](./docs/architecture.md) - Technical implementation details
- [✍️ Prompt Engineering Guide](./docs/prompts.md) - Writing effective agent prompts
- [☁️ AWS Bedrock Setup](./docs/aws-setup.md) - Step-by-step configuration
- [📖 Context7 Integration](./docs/context7.md) - Documentation API usage
- [🚂 Railway Deployment](./docs/railway.md) - Production deployment guide

---

## 🎓 Learning Resources

**Built Using Concepts From:**
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [Mistral AI Best Practices](https://docs.mistral.ai/)
