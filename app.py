import streamlit as st
from datetime import datetime
import zipfile
from io import BytesIO
import markdown
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# Import all agent functions
from scripts.ba_agent import run_agent as run_ba
from scripts.pm_agent import run_agent as run_pm
from scripts.prd_agent import run_agent as run_prd
from scripts.arch_agent import run_agent as run_arch
from scripts.po_agent import run_agent as run_po
from scripts.sm_agent import run_agent as run_sm
from scripts.task_master_agent import run_agent as run_tma


def create_pdf(content, idea, timestamp):
    """Generate PDF from markdown content"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                          topMargin=0.75*inch, bottomMargin=0.75*inch,
                          leftMargin=0.75*inch, rightMargin=0.75*inch)
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='#1f77b4',
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor='#2c3e50',
        spaceAfter=10,
        spaceBefore=10
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        leading=14,
        spaceAfter=8
    )
    
    story = []
    
    # Title page
    story.append(Paragraph("🚀 Everbooming Agent Kit", title_style))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph(f"<b>Product Idea:</b> {idea}", body_style))
    story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", body_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(PageBreak())
    
    # Process markdown content - simple conversion
    lines = content.split('\n')
    for line in lines:
        if line.startswith('# '):
            story.append(Paragraph(line[2:], title_style))
        elif line.startswith('## '):
            story.append(Paragraph(line[3:], heading_style))
        elif line.startswith('### '):
            story.append(Paragraph(line[4:], styles['Heading3']))
        elif line.strip().startswith('---'):
            story.append(Spacer(1, 0.2*inch))
        elif line.strip():
            # Clean the line for PDF
            clean_line = line.replace('**', '<b>').replace('**', '</b>')
            clean_line = clean_line.replace('*', '<i>').replace('*', '</i>')
            try:
                story.append(Paragraph(clean_line, body_style))
            except:
                # If paragraph fails, just add as plain text
                pass
        else:
            story.append(Spacer(1, 0.1*inch))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

st.set_page_config(page_title="Everbooming Agent Kit", layout="wide")
st.title("🚀 Everbooming Agent Kit")

# Input
idea = st.text_input("💡 Enter your product idea", "A mobile app for dog walkers to find clients")

if st.button("Run Full Pipeline"):
    
    # Store all outputs for download
    all_outputs = {}
    
    # 1. Business Analyst
    with st.spinner("Running Business Analyst..."):
        ba = run_ba(idea)
        all_outputs["01_Business_Analysis"] = ba
        with st.expander("📊 Business Analyst Output", expanded=True):
            st.markdown(ba)

    # 2. Project Manager
    with st.spinner("Running Project Manager..."):
        pm = run_pm(ba)
        all_outputs["02_Project_Plan"] = pm
        with st.expander("📋 Project Manager Output", expanded=True):
            st.markdown(pm)

    # 3. Product Requirements (PRD)
    with st.spinner("Generating PRD..."):
        prd = run_prd(idea, pm) 
        all_outputs["03_PRD"] = prd
        with st.expander("📄 PRD Output", expanded=True):
            st.markdown(prd)

    # 4. System Architect
    with st.spinner("Generating Architecture..."):
        arch = run_arch(prd)
        all_outputs["04_Architecture"] = arch
        with st.expander("🏗️ Architecture Output", expanded=True):
            st.markdown(arch)

    # 5. Task Master (Technical Tasks)
    with st.spinner("Generating Technical Tasks (Task Master)..."):
        tasks = run_tma(arch)
        all_outputs["05_Technical_Tasks"] = tasks
        with st.expander("⚙️ Technical Tasks Breakdown", expanded=True):
            st.markdown(tasks)

    # 6. Product Owner (User Stories)
    with st.spinner("Generating User Stories (PO)..."):
        po = run_po(arch)
        all_outputs["06_User_Stories"] = po
        with st.expander("👥 Product Owner Output", expanded=True):
            st.markdown(po)

    # 7. Scrum Master (Sprints)
    with st.spinner("Planning Sprints (Scrum Master)..."):
        sm = run_sm(po)
        all_outputs["07_Sprint_Plan"] = sm
        with st.expander("🏃 Scrum Master Output", expanded=True):
            st.markdown(sm)

    st.success("🚀 Pipeline Completed Successfully!")
    
    # Create combined markdown document
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    combined_content = f"""# Everbooming Agent Kit - Complete Output
**Product Idea:** {idea}  
**Generated:** {datetime.now().strftime("%B %d, %Y at %I:%M %p")}

---

## 📊 Business Analysis
{ba}

---

## 📋 Project Management Plan
{pm}

---

## 📄 Product Requirements Document
{prd}

---

## 🏗️ System Architecture
{arch}

---

## ⚙️ Technical Tasks Breakdown
{tasks}

---

## 👥 User Stories
{po}

---

## 🏃 Sprint Plan
{sm}

---

*Generated by Everbooming Agent Kit - AI-Powered SDLC Automation with AWS Bedrock*
"""

    # Create ZIP file with all outputs
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add combined document
        zip_file.writestr(f"Complete_Output_{timestamp}.md", combined_content)
        
        # Add individual files
        for filename, content in all_outputs.items():
            zip_file.writestr(f"{filename}.md", content)
    
    zip_buffer.seek(0)
    
    # Download buttons
    st.divider()
    
    # Generate PDF
    pdf_buffer = create_pdf(combined_content, idea, timestamp)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label="📄 Download Complete Report (PDF)",
            data=pdf_buffer.getvalue(),
            file_name=f"Everbooming_Complete_Report_{timestamp}.pdf",
            mime="application/pdf",
            use_container_width=True,
            type="primary"
        )
    
    with col2:
        st.download_button(
            label="📦 Download Separate Files (ZIP)",
            data=zip_buffer.getvalue(),
            file_name=f"everbooming_outputs_{timestamp}.zip",
            mime="application/zip",
            use_container_width=True
        )

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p style='font-size: 14px; margin: 0;'>
            AI-Powered SDLC Automation with AWS Bedrock
        </p>
        <p style='font-size: 12px; margin: 5px 0 0 0;'>
            Powered by Mistral Large 2 • Built with Streamlit • Deployed on Railway
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
