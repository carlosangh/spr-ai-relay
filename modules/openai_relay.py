import os
from dotenv import load_dotenv

load_dotenv()  # 🔥 Isso garante que ele carregue as variáveis do .env

import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_openai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[OpenAI Error]: {e}"
