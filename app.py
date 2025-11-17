import streamlit as st

from scripts.ba_agent import run_agent as run_ba
from scripts.pm_agent import run_agent as run_pm
from scripts.prd_agent import run_agent as run_prd
from scripts.arch_agent import run_agent as run_arch
from scripts.po_agent import run_agent as run_po
from scripts.sm_agent import run_agent as run_sm
from scripts.task_master_agent import run_agent as run_tma

st.title("Everbooming AWS-Native AI Software Development Kit")

idea = st.text_input("💡 Enter your product idea")

if st.button("Run Full Pipeline"):
    with st.spinner("Running Business Analyst..."):
        ba = run_ba(idea)
        st.subheader("Business Analyst Output")
        st.markdown(ba)

    with st.spinner("Running Product Manager..."):
        pm = run_pm(ba)
        st.subheader("Product Manager Output")
        st.markdown(pm)

    with st.spinner("Generating PRD..."):
        prd = run_prd(ba, pm)
        st.subheader("PRD Output")
        st.markdown(prd)

    with st.spinner("Generating Architecture..."):
        arch = run_arch(prd)
        st.subheader("Architecture Output")
        st.markdown(arch)

    with st.spinner("Generating Backlog (PO)..."):
        po = run_po(arch)
        st.subheader("Product Owner Output")
        st.markdown(po)

    with st.spinner("Generating Sprint Plan (SM)..."):
        sm = run_sm(po)
        st.subheader("Scrum Master Output")
        st.markdown(sm)

    with st.spinner("Generating Technical Tasks..."):
        tma = run_tma(sm)
        st.subheader("Task Master Output")
        st.markdown(tma)
