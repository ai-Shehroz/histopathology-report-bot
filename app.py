import streamlit as st
import os
import requests

# Get API key securely from Streamlit secrets
api_key = st.secrets.get("OPENROUTER_API_KEY", "")
if not api_key:
    st.error("⚠️ API key not found in Streamlit secrets. Please set 'OPENROUTER_API_KEY'.")
    st.stop()

# Streamlit UI
st.set_page_config(page_title="Histopathology Report Generator", layout="centered")
st.markdown("## 🔬 Histopathology Report Generator")
st.markdown("#### Developed by **Shehroz Khan Rind**")

st.divider()

with st.expander("👤 Patient Information", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        patient_name = st.text_input("Name")
        age = st.text_input("Age")
    with col2:
        sex = st.selectbox("Sex", ["Male", "Female", "Other"])

with st.expander("🧪 Specimen Details", expanded=True):
    biopsy_type = st.text_input("Type of Specimen (e.g., Prostate biopsy, Colon polyp)")

with st.expander("📋 Clinical History", expanded=True):
    clinical_history = st.text_area("Describe clinical background, symptoms, or suspected diagnosis.")

with st.expander("🔬 Gross Description", expanded=True):
    gross_description = st.text_area("Enter gross description of specimen (e.g., size, color, texture).")

with st.expander("🧫 Microscopic Findings", expanded=True):
    microscopic_findings = st.text_area("Enter detailed microscopic findings.")

# Generate Button
if st.button("🧠 Generate Histopathology Report"):
    with st.spinner("Generating report..."):
        # Prepare full prompt
        prompt = f"""
You are a medical AI specialized in histopathology.

Generate a structured and professional histopathology report based on the following details:

Patient Name: {patient_name}
Age: {age}
Sex: {sex}
Specimen Type: {biopsy_type}

Clinical History:
{clinical_history}

Gross Description:
{gross_description}

Microscopic Findings:
{microscopic_findings}

Ensure proper headings and final diagnosis summary.
        """

        try:
            # Call OpenRouter API
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "mistralai/mistral-7b-instruct:free",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7
                }
            )
            result = response.json()

            if "choices" in result:
                report_text = result["choices"][0]["message"]["content"]
                st.success("✅ Report generated successfully!")
                st.markdown("### 🧾 Generated Report")
                st.text_area("Histopathology Report", value=report_text, height=400)

                # Allow download
                st.download_button("📥 Download Report", report_text, file_name="histopathology_report.txt")
            else:
                st.error(f"❌ API Error: {result}")
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")

