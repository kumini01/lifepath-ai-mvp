from openai import OpenAI


def ask_life_coach(api_key, question, profile, events, todos):
    client = OpenAI(api_key=api_key)
    context = f"Profile: {dict(profile) if profile else 'not registered'}\nLife events: {[dict(x) for x in events[:10]]}\nTodos: {[dict(x) for x in todos[:10]]}"
    response = client.responses.create(
        model="gpt-5.6-sol",
        instructions="You are a Korean-language life planning assistant. Use only the user-provided profile, events, and tasks as context. Give concise priorities and next actions. For medical, legal, or financial topics, distinguish general information from matters that require a qualified professional.",
        input=f"{context}\n\nQuestion: {question}",
    )
    return response.output_text
