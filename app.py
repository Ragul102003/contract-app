import streamlit as st
import re
from datetime import datetime

st.set_page_config(page_title="GenAI Legal Assistant", layout="centered")

st.title("⚖️ GenAI-Powered Legal Assistant for SMEs")
st.caption("Understand contracts • Identify risks • Make better decisions")

# ---------- File Upload ----------
file = st.file_uploader(
    "Upload Contract (TXT only for now)",
    type=["txt"]
)

def detect_contract_type(text):
    text = text.lower()
    if "employment" in text or "employee" in text:
        return "Employment Agreement"
    if "lease" in text or "rent" in text:
        return "Lease Agreement"
    if "vendor" in text or "supplier" in text:
        return "Vendor Contract"
    if "partnership" in text:
        return "Partnership Deed"
    return "Service Contract / General Agreement"

def split_clauses(text):
    clauses = re.split(r"\n\d+\.|\n[A-Z][A-Za-z ]+:", text)
    return [c.strip() for c in clauses if len(c.strip()) > 40]

def analyze_clause(clause):
    clause_lower = clause.lower()
    risk = "Low"
    reasons = []

    if "penalty" in clause_lower:
        risk = "High"
        reasons.append("Penalty clause detected")

    if "terminate" in clause_lower:
        risk = "High"
        reasons.append("Unilateral termination risk")

    if "indemnify" in clause_lower:
        risk = "Medium"
        reasons.append("Indemnity obligation")

    if "arbitration" in clause_lower:
        risk = "Medium"
        reasons.append("Arbitration clause present")

    explanation = f"This clause means: {clause[:150]}..."

    return risk, reasons, explanation

# ---------- Main Processing ----------
if file:
    text = file.read().decode("utf-8")

    st.subheader("📄 Contract Overview")

    contract_type = detect_contract_type(text)
    st.write(f"**Detected Contract Type:** {contract_type}")

    clauses = split_clauses(text)

    st.subheader("📊 Risk Analysis")

    overall_score = {"High": 0, "Medium": 0, "Low": 0}

    for idx, clause in enumerate(clauses, 1):
        risk, reasons, explanation = analyze_clause(clause)
        overall_score[risk] += 1

        with st.expander(f"Clause {idx} | Risk: {risk}"):
            st.write("**Clause Text:**")
            st.write(clause)

            st.write("**Explanation (Plain Language):**")
            st.write(explanation)

            if reasons:
                st.write("**Risk Reasons:**")
                for r in reasons:
                    st.write(f"- {r}")

    st.subheader("⚠️ Overall Contract Risk Summary")
    st.json(overall_score)

    st.subheader("📝 Audit Log")
    st.write(f"Analysis completed at: {datetime.now()}")
