import json
import streamlit as st
from pathlib import Path

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="TPD Intelligence Dashboard",
    layout="wide"
)

# =========================
# LOAD DATA (READ-ONLY)
# =========================
DATA_DIR = Path("data/final")

programs = json.load(open(DATA_DIR / "programs.json"))
summaries_timeaware = json.load(open(DATA_DIR / "program_summaries_timeaware.json"))
summaries_static = json.load(open(DATA_DIR / "program_summaries.json"))

# =========================
# INDEX DATA
# =========================
program_index = {(p["company"], p["program_name"]): p for p in programs}
timeaware_index = {(s["company"], s["program_name"]): s for s in summaries_timeaware}
static_index = {(s["company"], s["program_name"]): s for s in summaries_static}

companies = sorted({p["company"] for p in programs})

# =========================
# SIDEBAR
# =========================
st.sidebar.title("Filters")

company = st.sidebar.selectbox("Company", companies)

company_programs = sorted(
    p["program_name"]
    for p in programs
    if p["company"] == company
)

program = st.sidebar.selectbox("Program", company_programs)

key = (company, program)

# =========================
# HEADER
# =========================
st.title("🧬 TPD Intelligence Dashboard")
st.caption("Time-aware, evidence-backed program summaries")

st.markdown(f"## {program}")

# =========================
# SUMMARY (WITH FALLBACK)
# =========================
summary_text = None
evidence = []

if key in timeaware_index:
    summary_text = timeaware_index[key].get("summary")
    evidence = timeaware_index[key].get("evidence", [])

elif key in static_index:
    summary_text = static_index[key].get("summary")
    evidence = static_index[key].get("evidence", [])

if summary_text:
    st.markdown(summary_text)
else:
    st.warning("No summary available for this program.")

# =========================
# PROGRAM FACTS (COLLAPSIBLE, COMMA-SEPARATED)
# =========================
program_data = program_index.get(key)

if program_data:
    with st.expander("Program Facts", expanded=False):

        def render_field(label, values):
            if values:
                st.markdown(
                    f"**{label}:** " + ", ".join(values)
                )

        render_field("Targets", program_data.get("targets"))
        render_field("Indications", program_data.get("indications"))
        render_field("Therapeutic Areas", program_data.get("therapeutic_areas"))
        render_field("Modalities", program_data.get("modalities"))
        render_field("E3 Ligases", program_data.get("e3_ligases"))
        render_field("Clinical Phases", program_data.get("clinical_phases"))

# =========================
# SOURCE EVIDENCE
# =========================
st.markdown("---")
st.markdown("### Source Evidence")

if evidence:
    for e in evidence:
        doc = e.get("document", "Unknown document")
        slide = e.get("slide")
        if slide:
            st.markdown(f"- **{doc}**, slide {slide}")
        else:
            st.markdown(f"- **{doc}**")
else:
    st.caption("No source evidence available.")

st.caption(
    "Generated from publicly available disclosures. Read-only demo."
)

