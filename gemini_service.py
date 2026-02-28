import json
import google.generativeai as genai


def setup_gemini(api_key):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")


def summarize_email(model, email_data):
    prompt = f"""
    Summarize this email in 2 concise bullet points.

    From: {email_data["from"]}
    Subject: {email_data["subject"]}
    Body: {email_data["body"][:3000]}

    Categorize into one of:
    ["Work", "Personal", "Job", "Finance", "Spam", "Other","Advertisement"]

    Prioritize into one of:
    ["High", "Medium", "Low"]

    Return strictly valid JSON:
    {{
        "summary": "",
        "category": "",
        "priority": ""
    }}
    """

    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.2
        )
    )

    try:
        return json.loads(response.text)
    except:
        return {
            "summary": "Failed to parse response",
            "category": "Other",
            "priority": "Low"
        }