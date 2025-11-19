import streamlit as st

# Import all agent functions
from scripts.ba_agent import run_agent as run_ba
from scripts.pm_agent import run_agent as run_pm
from scripts.prd_agent import run_agent as run_prd
from scripts.arch_agent import run_agent as run_arch
from scripts.po_agent import run_agent as run_po
from scripts.sm_agent import run_agent as run_sm
from scripts.task_master_agent import run_agent as run_tma

st.set_page_config(page_title="Everbooming AI Kit", layout="wide")
st.title("Everbooming AWS-Native AI Software Development Kit")

# Input
idea = st.text_input("💡 Enter your product idea", "A mobile app for dog walkers to find clients")

if st.button("Run Full Pipeline"):
    
    # 1. Business Analyst
    with st.spinner("Running Business Analyst..."):
        ba = run_ba(idea)
        with st.expander("Business Analyst Output", expanded=True):
            st.markdown(ba)

    # 2. Project Manager
    with st.spinner("Running Project Manager..."):
        pm = run_pm(ba)  # Pass BA output
        with st.expander("Product Manager Output", expanded=True):
            st.markdown(pm)

    # 3. Product Requirements (PRD)
    with st.spinner("Generating PRD..."):
        # CRITICAL FIX: Pass 'idea' (raw input) and 'pm' (PM Plan)
        prd = run_prd(idea, pm) 
        with st.expander("PRD Output", expanded=True):
            st.markdown(prd)

    # 4. System Architect
    with st.spinner("Generating Architecture..."):
        arch = run_arch(prd) # Pass PRD
        with st.expander("Architecture Output", expanded=True):
            st.markdown(arch)

    # 5. Task Master (Technical Tasks) - Parallel Step A
    with st.spinner("Generating Technical Tasks (Task Master)..."):
        tasks = run_tma(arch) # Pass Architecture
        with st.expander("Technical Tasks Breakdown", expanded=True):
            st.markdown(tasks)

    # 6. Product Owner (User Stories) - Parallel Step B
    with st.spinner("Generating User Stories (PO)..."):
        po = run_po(arch) # Pass Architecture
        with st.expander("Product Owner Output", expanded=True):
            st.markdown(po)

    # 7. Scrum Master (Sprints)
    with st.spinner("Planning Sprints (Scrum Master)..."):
        sm = run_sm(po) # Pass PO Stories
        with st.expander("Scrum Master Output", expanded=True):
            st.markdown(sm)

    st.success("🚀 Pipeline Completed Successfully!")
