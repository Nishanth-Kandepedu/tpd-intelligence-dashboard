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

DATA_DIR = Path("data/final")
PROGRAMS_FILE = DATA_DIR / "programs.json"
SUMMARIES_FILE = DATA_DIR / "program_summaries_timeaware.json"

# =========================
# NORMALIZATION HELPERS
# =========================
def norm_company(c):
    return c.strip().lower().replace(" ", "_")

def norm_program(p):
    return (
        p.replace("®", "")
         .replace("-", "")
         .replace(" ", "")
         .lower()
    )

# =========================
# LOAD DATA (READ-ONLY)
# =========================
programs = json.load(open(PROGRAMS_FILE))
summaries_raw = json.load(open(SUMMARIES_FILE))

# Build summary lookup with normalized keys
summaries = {
    (norm_company(s["company"]), norm_program(s["program_name"])): s
    for s in summaries_raw
}

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.markdown("## Filters")

companies = sorted({p["company"] for p in programs})
company = st.sidebar.selectbox("Company", companies)

programs_for_company = sorted(
    p["program_name"]
    for p in programs
    if p["company"] == company
)

program = st.sidebar.selectbox("Program", programs_for_company)

# =========================
# HEADER
# =========================
st.markdown(
    "## 🧬 TPD Intelligence Dashboard\n"
    "_Time-aware, evidence-backed program summaries_"
)

st.markdown(f"### {program}")

# =========================
# FETCH SUMMARY
# =========================
summary = summaries.get(
    (norm_company(company), norm_program(program))
)

# =========================
# SUMMARY SECTION
# =========================
if summary and summary.get("summary"):
    st.markdown(summary["summary"])
else:
    st.warning("No summary available.")

# =========================
# SOURCE EVIDENCE
# =========================
st.markdown("### 📄 Source Evidence")

if summary and summary.get("evidence"):
    for e in summary["evidence"]:
        doc = e.get("document", "Unknown document")
        slide = e.get("slide")
        if slide is not None:
            st.markdown(f"- **{doc}**, slide {slide}")
        else:
            st.markdown(f"- **{doc}**")
else:
    st.markdown("_No source evidence available._")

# =========================
# PROGRAM FACTS (OPTIONAL)
# =========================
with st.expander("Program Facts"):
    prog = next(
        p for p in programs
        if p["company"] == company and p["program_name"] == program
    )

    def show_list(label, items):
        if items:
            st.markdown(f"**{label}:** {', '.join(items)}")

    show_list("Targets", prog.get("targets", []))
    show_list("Modalities", prog.get("modalities", []))
    show_list("E3 Ligases", prog.get("e3_ligases", []))
    show_list("Indications", prog.get("indications", []))
    show_list("Therapeutic Areas", prog.get("therapeutic_areas", []))
    show_list("Clinical Phases", prog.get("clinical_phases", []))

st.caption(
    "Generated from publicly available disclosures. "
    "Read-only demo."
)

