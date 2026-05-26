import ollama

def generate_answer_with_llm(question, context):
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
        ],
        stream=True
    )

    for chunk in response:
        content = chunk["message"]["content"]

        if content:
            print(content, end="", flush=True)
            yield content