import streamlit as st
from prompt_utils import generate_variants, evaluate_variants, get_response
import os
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="PromptTune", page_icon="🛠")

st.title("🛠 PromptTune – Prompt Optimizer using GPT")
st.markdown("Enter your base prompt and what you're trying to achieve. Let GPT improve it for you!")

base_prompt = st.text_area("✏️ Your Original Prompt", placeholder="e.g., Summarize the following news article...", height=120)
goal = st.text_input("🎯 Desired Output Goal", placeholder="e.g., Make it concise and still cover all key points")

if st.button("🔄 Optimize Prompt"):
    with st.spinner("Generating prompt variants..."):
        variants = generate_variants(base_prompt, goal)

    with st.spinner("Evaluating prompt variants..."):
        evaluations = evaluate_variants(variants, base_prompt, goal)

    st.subheader("📋 Ranked Prompts")
    best_prompt = sorted(evaluations, key=lambda x: x['score'], reverse=True)[0]

    for i, result in enumerate(sorted(evaluations, key=lambda x: x['score'], reverse=True), 1):
        st.markdown(f"### #{i} — Score: {result['score']}/10")
        st.markdown(f"**Prompt:** {result['prompt']}")
        st.markdown(f"**Evaluation:** {result['review']}")
        with st.expander("🧠 See GPT Output with this prompt"):
            output = get_response(result['prompt'])
            st.markdown(output)
        st.markdown("---")

    st.success(f"✅ Best Prompt: "{best_prompt['prompt']}"")