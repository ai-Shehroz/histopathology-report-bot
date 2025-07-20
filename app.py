import gradio as gr
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def generate_report(name, age, sex, specimen, history, gross, microscopic):
    prompt = f"""
You are a professional histopathologist. Based on the following inputs, write a detailed histopathology report:

Patient Name: {name}
Age: {age}
Sex: {sex}
Specimen Details: {specimen}
Clinical History: {history}
Gross Description: {gross}
Microscopic Findings: {microscopic}

Write a structured pathology report.
"""

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "https://huggingface.co/spaces/your-username/your-app",  # Optional but recommended
        "X-Title": "histopathology-bot"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.text}"

demo = gr.Interface(
    fn=generate_report,
    inputs=[
        gr.Textbox(label="Patient Name"),
        gr.Number(label="Age"),
        gr.Radio(choices=["Male", "Female", "Other"], label="Sex"),
        gr.Textbox(label="Specimen Details"),
        gr.Textbox(label="Clinical History"),
        gr.Textbox(label="Gross Description"),
        gr.Textbox(label="Microscopic Findings")
    ],
    outputs=gr.Textbox(label="Histopathology Report"),
    title="🔬 Histopathology Report Generator",
    description="AI-powered report generator for pathology using OpenRouter + Mistral-7B"
)

if __name__ == "__main__":
    demo.launch()
