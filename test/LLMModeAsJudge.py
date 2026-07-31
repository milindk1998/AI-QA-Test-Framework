import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from deepeval.models.base_model import DeepEvalBaseLLM

load_dotenv()

# LLM as a judge for evaluation
class DeepEvalLLM(DeepEvalBaseLLM):

    def __init__(self):
        self._model_name = os.getenv("modelAsJudge")
        self.client = ChatOpenAI(
            model=self._model_name,
            api_key=os.getenv("grok_api_key"),
            base_url=os.getenv("base_url"),
            temperature=0,
        )

    def load_model(self):
        return self.client

    def get_model_name(self):
        return self._model_name

    def generate(self, prompt: str) -> str:
        response = self.client.invoke([HumanMessage(content=prompt)])
        return response.content

    async def a_generate(self, prompt: str) -> str:
        response = await self.client.ainvoke([HumanMessage(content=prompt)])
        return response.content
    

def run_streamlit_ui():
    import streamlit as st
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is None:
            print("Run this UI with: streamlit run test/deepEvalLLM.py")
            return
    except Exception:
        pass

    st.set_page_config(page_title="LLM UI", page_icon=":test_tube:", layout="centered")
    st.title("LLM-as-Judge")
    st.write("Enter a prompt and generate a response using your configured model.")

    st.sidebar.markdown(f"**Note:** This Chatbot is powered by the model: `{DeepEvalLLM().get_model_name()}`")
    st.sidebar.markdown("Design and developed by Milind Krishna | © 2026")

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
                st.subheader("Model Response")
                st.write(response)
            except Exception as exc:
                st.error(f"Failed to generate response: {exc}")


if __name__ == "__main__":
    run_streamlit_ui()