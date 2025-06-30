import openai
import os

# Set API key (Streamlit Cloud will inject this from secrets)
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_variants(base_prompt, goal):
    system_message = {"role": "system", "content": "You are a prompt engineering expert. Improve prompts for LLMs."}
    user_message = {"role": "user", "content": f"""Improve the following prompt based on the user's goal.

Original Prompt: "{base_prompt}"
Goal: "{goal}"

Generate 3 different improved prompt variations. Return as a numbered list."""}

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[system_message, user_message]
    )

    content = response["choices"][0]["message"]["content"]
    lines = content.split("\n")
    prompts = [line.split(". ", 1)[1] for line in lines if line.strip() and ". " in line]
    return prompts

def evaluate_variants(variants, original_prompt, goal):
    results = []
    for prompt in variants:
        messages = [
            {"role": "system", "content": "You are a helpful AI trained to evaluate prompt quality."},
            {"role": "user", "content": f"""Original Prompt: "{original_prompt}"
Improved Prompt: "{prompt}"
Goal: "{goal}"

Evaluate how well the improved prompt meets the goal.
Give a brief review and rate from 1 to 10 (10 = perfect). Format:
Review: <your review>
Score: <number>"""}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        content = response["choices"][0]["message"]["content"]
        try:
            review = content.split("Review:")[1].split("Score:")[0].strip()
            score = int(content.split("Score:")[1].strip())
        except:
            review = content
            score = 5
        results.append({"prompt": prompt, "review": review, "score": score})
    return results

def get_response(prompt):
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error generating response: {e}"
