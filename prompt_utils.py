import openai
import os

# Set API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_variants(base_prompt, goal):
    messages = [
        {"role": "system", "content": "You are a prompt engineering expert. Improve prompts for LLMs."},
        {"role": "user", "content": f"""Improve the following prompt based on the user's goal.

Original Prompt: "{base_prompt}"
Goal: "{goal}"

Generate 3 different improved prompt variations. Return as a numbered list."""}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    content = response["choices"][0]["message"]["content"]
    lines = content.split("\n")
    prompts = [line.split(". ", 1)[1] for line in lines if ". " in line]
    return prompts
