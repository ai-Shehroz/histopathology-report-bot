import streamlit as st
import requests

# App Header
st.set_page_config(page_title="Histopathology Report Generator")
st.title("🔬 Histopathology Report Generator")
st.markdown("**Developed by Shehroz Khan Rind**")

# Check API key
api_key = st.secrets.get("OPENROUTER_API_KEY", "")
if not api_key:
    st.error("⚠️ API key not found in .streamlit/secrets.toml")
    st.stop()

# Input Sections
st.header("🧾 Patient & Specimen Details")
patient_name = st.text_input("Patient Name")
patient_age = st.text_input("Age")
patient_sex = st.selectbox("Sex", ["Male", "Female", "Other"])
specimen_details = st.text_area("Specimen Details (e.g., Prostate needle biopsy)")

st.header("📋 Clinical & Pathology Findings")
clinical_history = st.text_area("Clinical History")
gross_description = st.text_area("Gross Description")
microscopic_findings = st.text_area("Microscopic Findings")

# Combine Inputs
combined_input = f"""
Patient Name: {patient_name}
Age: {patient_age}
Sex: {patient_sex}
Specimen Details: {specimen_details}

Clinical History:
{clinical_history}

Gross Description:
{gross_description}

Microscopic Findings:
{microscopic_findings}
"""

# Button to Generate Report
if st.button("📄 Generate Histopathology Report"):
    with st.spinner("Generating report..."):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "HTTP-Referer": "https://github.com/ai-shehroz",  # Optional
                    "X-Title": "HistopathologyReportBot"
                },
                json={
                    "model": "mistralai/mistral-7b-instruct:free",
                    "messages": [
                        {"role": "system", "content": "You are a histopathology expert who generates professional and detailed reports based on input data."},
                        {"role": "user", "content": combined_input}
                    ]
                }
            )
            result = response.json()
            if "choices" in result:
                report = result["choices"][0]["message"]["content"]
                st.success("✅ Report Generated")
                st.text_area("📄 Final Report", report, height=400)
            else:
                st.error(f"❌ API Error: {result}")
        except Exception as e:
            st.error(f"❌ Request failed: {e}")
