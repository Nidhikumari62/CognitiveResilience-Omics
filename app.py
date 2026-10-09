
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="CognitiveResilience-Omics",
    page_icon="🧠",
    layout="wide"
)

DATA = Path(__file__).parent / "data"

def load_csv(filename):
    path = DATA / filename
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

summary = load_csv("ROSMAP_Master_Results_Summary.csv")
flow = load_csv("ROSMAP_Study_Cohort_Flow.csv")
candidates = load_csv("ROSMAP_Final_Molecular_Candidate_Panel.csv")
themes = load_csv("ROSMAP_Cross_Omics_Biological_Themes.csv")
proteins = load_csv("ROSMAP_Top_Proteomics_Candidates.csv")

st.title("🧠 CognitiveResilience-Omics")
st.subheader(
    "Multi-Omics Characterization and Machine Learning-Based "
    "Prediction of Cognitive Resilience in Alzheimer's Disease Using ROSMAP"
)

st.info(
    "Academic research dashboard. Findings are exploratory and "
    "are not intended for clinical diagnosis."
)

page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Cohort Flow",
        "Molecular Candidates",
        "Biological Themes",
        "Master Results"
    ]
)

if page == "Overview":
    st.header("Project Overview")
    a, b, c, d = st.columns(4)
    a.metric("Clinical cohort", "3,584")
    b.metric("Pathology-defined cohort", "830")
    c.metric("RNA cohort", "307")
    d.metric("Paired multi-omics cohort", "43")

    st.markdown("""
    ### Research objectives
    - Characterize cognitive resilience groups.
    - Explore RNA and protein candidates.
    - Summarize machine-learning results.
    - Investigate biological themes across omics datasets.
    """)

elif page == "Cohort Flow":
    st.header("Study Cohort Flow")
    if not flow.empty:
        st.dataframe(flow, use_container_width=True, hide_index=True)
        if "N" in flow.columns and "Cohort" in flow.columns:
            fig = px.bar(
                flow,
                x="Cohort",
                y="N",
                text="N",
                title="Sample size at each analysis stage"
            )
            fig.update_layout(xaxis_tickangle=-25)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Cohort flow data could not be loaded.")

elif page == "Molecular Candidates":
    st.header("Molecular Candidate Panel")
    if not candidates.empty:
        if "Omics" in candidates.columns:
            selected = st.selectbox(
                "Select data type",
                ["All"] + sorted(candidates["Omics"].dropna().unique())
            )
            view = candidates if selected == "All" else candidates[
                candidates["Omics"] == selected
            ]
        else:
            view = candidates
        st.dataframe(view, use_container_width=True, hide_index=True)
        st.download_button(
            "Download candidates CSV",
            view.to_csv(index=False),
            file_name="ROSMAP_Molecular_Candidates.csv",
            mime="text/csv"
        )

    st.subheader("Top Proteomics Candidates")
    if not proteins.empty:
        st.dataframe(proteins, use_container_width=True, hide_index=True)

elif page == "Biological Themes":
    st.header("Cross-Omics Biological Themes")
    if not themes.empty:
        st.dataframe(themes, use_container_width=True, hide_index=True)
    else:
        st.warning("Biological themes data could not be loaded.")

elif page == "Master Results":
    st.header("Master Results Summary")
    if not summary.empty:
        st.dataframe(summary, use_container_width=True, hide_index=True)
        st.download_button(
            "Download master results CSV",
            summary.to_csv(index=False),
            file_name="ROSMAP_Master_Results_Summary.csv",
            mime="text/csv"
        )
    else:
        st.warning("Master results data could not be loaded.")

st.sidebar.markdown("---")
st.sidebar.caption("ROSMAP | Academic research project")
