import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_answer_with_ai(question, context):
    prompt = f"""
    You are a helpful assistant.
    Use ONLY the context below.

    Context:
    {context}

    Question:
    {question}
    """

    response = client.models.generate_content(
        model="gemini-1.5-flash-latest",
        contents=prompt
    )

    return response.text