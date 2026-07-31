
                       conftest.py
                   deepeval.login(api_key)
                           │
           ┌───────────────┴───────────────┐
           │                               │
           ▼                               ▼
  multipleMetricTest.py         pullingDatasetLLMTest.py
           │                               │
  Define Goldens locally         dataset.pull(alias=
  (input, expected_output,       "Dataset for AI Test")
   retrieval_context)                      │
           │                               │
  EvaluationDataset(goldens)    EvaluationDataset (remote)
           │                               │
           └───────────────┬───────────────┘
                           │
              for golden in dataset.goldens:
                           │
                           ▼
                  chatbot.py  ──────────────────────┐
                ask_llm(golden.input)               │
                           │                        │  Streamlit UI
                           ▼                        │  (streamlit run chatbot.py)
                       LLM Model                    │
                  (testmodel via OpenAI)            │
                           │                        │
                           ▼                        │
                     actual_output                  │
                           │                        │
                           ▼                        │
                      LLMTestCase                   │
       ┌──────────────────────────────────┐         │
       │ input        = golden.input      │         │
       │ actual_output = response         │         │
       │ expected_output = golden.expected│         │
       │ retrieval_context                │         │
       └──────────────────────────────────┘         │
                           │                        │
                           ▼
            evaluate(test_cases, metrics)
                           │
           ┌───────────────┴───────────────┐
           ▼                               ▼
 AnswerRelevancyMetric          FaithfulnessMetric
  (threshold=0.7)                (threshold=0.7)
  include_reason=True            include_reason=True
           │                               │
           └───────────────┬───────────────┘
                           ▼
                     DeepEvalLLM
              ┌──────────────────────────┐
              │ OpenAI client            │
              │ api_key = model_api_key  │
              │ base_url = base_url      │
              │ model   = modelAsJudge   │
              │ generate() / a_generate()│
              └──────────────────────────┘
                           │
                           ▼
                  LLM Model as Judge
                  (temperature=0)
                           │
                           ▼
               Score • Reason • Pass/Fail
                           │
                           ▼
                Console + Confident AI