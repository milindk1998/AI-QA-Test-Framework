import os
from dotenv import load_dotenv
from openai import OpenAI
from deepeval.models.base_model import DeepEvalBaseLLM
import streamlit as st

load_dotenv()

# LLM as a judge for evaluation
class DeepEvalLLM(DeepEvalBaseLLM):
    
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("grok_api_key"),
            base_url=os.getenv("base_url")
        )
        self.model = os.getenv("modelAsJudge")
        
    def load_model(self):
        return self.client
    
    def get_model_name(self):
        return self.model
    
    def generate(self, prompt: str):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            stream=False
        )
        return response.choices[0].message.content
    

    async def a_generate(self, prompt: str):
        return self.generate(prompt)
    
# llm = DeepEvalLLM()
# test_prompt = "What is DeepEval in one sentence? \nothink"
# response = llm.generate(test_prompt)
# print(f"LLM-as-Judge Response: {response} \n")


def run_streamlit_ui():
    st.set_page_config(page_title="LLM UI", page_icon=":test_tube:", layout="centered")
    st.title("LLM-as-Judge")
    st.write("Enter a prompt and generate a response using your configured model.")
    st.markdown("Design and developed by Milind Krishna | © 2026")

    prompt = st.text_area(
        "Prompt",
        value="What is DeepEval in one sentence?",
        height=140,
        placeholder="Type your evaluation prompt here..."
    )

    if st.button("Generate Response", type="primary"):
        if not prompt.strip():
            st.warning("Please enter a prompt before generating.")
            return

        with st.spinner("Calling model..."):
            try:
                llm = DeepEvalLLM()
                response = llm.generate(prompt)
                st.subheader("LLM-as-Judge Response")
                st.write(response)
            except Exception as exc:
                st.error(f"Failed to generate response: {exc}")


if __name__ == "__main__":
    run_streamlit_ui()