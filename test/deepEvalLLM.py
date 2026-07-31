import os
from dotenv import load_dotenv
from openai import OpenAI
from deepeval.models.base_model import DeepEvalBaseLLM

load_dotenv()

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

# # Test with a prompt
# test_prompt = "What is DeepEval in one sentence? \nothink"
# try:
#     response = llm.generate(test_prompt)
#     print(f"LLM-as-Judge Response: {response} \n")
# except Exception as e:
#     print(f"Error: {e}")