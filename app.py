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
# HELPERS
# =========================
def norm(x):
    return x.strip().lower() if isinstance(x, str) else ""

def safe_list(x):
    return x if isinstance(x, list) else []

# =========================
# LOAD DATA (READ-ONLY)
# =========================
DATA_DIR = Path("data/final")

programs = json.load(open(DATA_DIR / "programs.json"))
summaries_timeaware = json.load(open(DATA_DIR / "program_summaries_timeaware.json"))
summaries_static = json.load(open(DATA_DIR / "program_summaries.json"))

# =========================
# INDEX PROGRAMS
# =========================
program_index = {
    (norm(p["company"]), norm(p["program_name"])): p
    for p in programs
}

# =========================
# INDEX TIME-AWARE SUMMARIES
# =========================
timeaware_index = {}
for s in summaries_timeaware:
    c = norm(s.get("company"))
    p = norm(s.get("program_name"))
    if c and p:
        timeaware_index[(c, p)] = s

# =========================
# INDEX STATIC SUMMARIES (SCHEMA-SAFE)
# =========================
static_index = {}
for s in summaries_static:
    c = norm(s.get("company") or s.get("Company"))
    p = norm(s.get("program_name") or s.get("Program"))
    if c and p:
        static_index[(c, p)] = s

# =========================
# SIDEBAR
# =========================
st.sidebar.title("Filters")

companies = sorted({p["company"] for p in programs})
company_display = st.sidebar.selectbox("Company", companies)
company_key = norm(company_display)

company_programs = sorted(
    p["program_name"]
    for p in programs
    if norm(p["company"]) == company_key
)

program_display = st.sidebar.selectbox("Program", company_programs)
program_key = norm(program_display)

key = (company_key, program_key)

# =========================
# HEADER
# =========================
st.title("🧬 TPD Intelligence Dashboard")
st.caption("Time-aware, evidence-backed program summaries")

st.markdown(f"## {program_display}")

# =========================
# SUMMARY (TIMEAWARE → STATIC → NONE)
# =========================
summary_text = None
evidence = []

if key in timeaware_index:
    summary_text = timeaware_index[key].get("summary")
    evidence = safe_list(timeaware_index[key].get("evidence"))

elif key in static_index:
    summary_text = static_index[key].get("summary")
    evidence = safe_list(static_index[key].get("evidence"))

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

        def render(label, values):
            values = safe_list(values)
            if values:
                st.markdown(f"**{label}:** " + ", ".join(values))

        render("Targets", program_data.get("targets"))
        render("Indications", program_data.get("indications"))
        render("Therapeutic Areas", program_data.get("therapeutic_areas"))
        render("Modalities", program_data.get("modalities"))
        render("E3 Ligases", program_data.get("e3_ligases"))
        render("Clinical Phases", program_data.get("clinical_phases"))

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

