import json
from pathlib import Path
import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="TPD Intelligence Dashboard",
    layout="wide",
)

# =========================
# LOAD DATA (READ-ONLY)
# =========================
PROGRAMS_PATH = Path("data/final/programs.json")
SUMMARIES_PATH = Path("data/final/program_summaries_timeaware.json")

programs = json.load(open(PROGRAMS_PATH))
summaries = json.load(open(SUMMARIES_PATH))

# Index summaries for fast lookup
summary_index = {
    (s["company"].lower(), s["program_name"]): s
    for s in summaries
}

# =========================
# HEADER
# =========================
st.title("🧬 TPD Intelligence Dashboard")
st.caption("Time-aware, evidence-backed program summaries")

# =========================
# SIDEBAR FILTERS
# =========================
companies = sorted(set(p["company"] for p in programs))
company = st.sidebar.selectbox("Company", companies)

company_programs = sorted(
    [p for p in programs if p["company"] == company],
    key=lambda x: x["program_name"]
)

program_names = [p["program_name"] for p in company_programs]
program_name = st.sidebar.selectbox("Program", program_names)

program = next(
    p for p in company_programs if p["program_name"] == program_name
)

summary = summary_index.get((company.lower(), program_name))

# =========================
# MAIN CONTENT
# =========================
st.subheader(program_name)

# ---------- SUMMARY ----------
if summary:
    st.markdown(summary["summary"])
else:
    st.warning("No summary available for this program.")

st.divider()

# ---------- PROGRAM FACTS ----------
st.subheader("Program Facts")

def render_list(title, items):
    if items:
        st.markdown(f"**{title}:**")
        for i in sorted(items):
            st.markdown(f"- {i}")

render_list("Targets", program.get("targets"))
render_list("Modalities", program.get("modalities"))
render_list("E3 Ligases", program.get("e3_ligases"))
render_list("Indications", program.get("indications"))
render_list("Therapeutic Areas", program.get("therapeutic_areas"))
render_list("Clinical Phases", program.get("clinical_phases"))

st.divider()

# ---------- SOURCE EVIDENCE ----------
st.subheader("Source Evidence")

evidence = program.get("evidence", [])
if evidence:
    for e in evidence:
        st.markdown(f"- **{e['document']}**, slide {e['slide']}")
else:
    st.info("No source evidence available.")

