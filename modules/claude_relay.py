import anthropic
import os

def ask_claude(prompt):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    try:
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4096,
            temperature=0.2,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return message.content[0].text
    except Exception as e:
        return f"[Claude Error]: {e}"
