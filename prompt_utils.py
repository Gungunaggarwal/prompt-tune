import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_variants(base_prompt, goal):
    system = "You are a prompt engineering expert. Improve prompts for LLMs."
    user = f"""Improve the following prompt based on the user's goal.

Original Prompt: "{base_prompt}"
Goal: "{goal}"

Generate 3 different improved prompt variations. Return as a numbered list."""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}]
    )

    lines = response['choices'][0]['message']['content'].split("\n")
    prompts = [line[line.find('. ')+2:] for line in lines if '. ' in line]
    return prompts

def evaluate_variants(variants, original_prompt, goal):
    results = []
    for prompt in variants:
        user = f"""You are a helpful AI trained to evaluate prompt quality.

Original Prompt: "{original_prompt}"
Improved Prompt: "{prompt}"
Goal: "{goal}"

Evaluate how well the improved prompt meets the goal.
Give a brief review and rate from 1 to 10 (10 = perfect). Format:
Review: <your review>
Score: <number>
"""
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user}]
        )
        content = response['choices'][0]['message']['content']
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
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating response: {e}"