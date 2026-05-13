import ollama

def generate_answer(question, context):
    response = ollama.chat(
        model = "llama3.2:3b",
        messages = [
            {
                "role": "system",
                "content": "You are a real estate assistant. Answer ONLY using the provided context."
            },
            {
                "role": "user",
                "content": f"""
                Context:
                {context}
                Question:
                {question}
"""
            }
        ]
    )

    return response["message"]["content"]