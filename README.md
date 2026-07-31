# AI Engineering Evaluation — Python

A project for evaluating LLM outputs using [DeepEval](https://docs.confident-ai.com/) with a Streamlit chatbot as the system under test.

---

## Summary

This project connects a Streamlit-based chatbot (`chatbot.py`) to an automated evaluation pipeline powered by DeepEval. The LLM responses are assessed against two metrics — **Answer Relevancy** and **Faithfulness** — using a separate LLM-as-Judge (`DeepEvalLLM`). Test datasets can be defined locally or pulled directly from [Confident AI](https://app.confident-ai.com/).

### Key components

| File | Purpose |
|---|---|
| `chatbot.py` | Streamlit UI + `ask_llm()` function (system under test) |
| `test/deepEvalLLM.py` | Custom DeepEval judge wrapping an OpenAI-compatible client |
| `test/conftest.py` | pytest setup — loads `.env` and logs into Confident AI |
| `test/multipleMetricTest.py` | Evaluation using locally defined Goldens |
| `test/pullingDatasetLLMTest.py` | Evaluation by pulling a dataset from Confident AI |

---

## Architecture

```
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
                  chatbot.py
                ask_llm(golden.input)
                           │
                           ▼
                       LLM Model
                  (testmodel via OpenAI)
                           │
                           ▼
                     actual_output
                           │
                           ▼
                      LLMTestCase
       ┌──────────────────────────────────┐
       │ input        = golden.input      │
       │ actual_output = response         │
       │ expected_output = golden.expected│
       │ retrieval_context                │
       └──────────────────────────────────┘
                           │
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
```

---

## Setup

1. **Create and activate the virtual environment**
   ```bash
   python -m venv ai-env
   ai-env\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install streamlit openai deepeval python-dotenv
   ```

3. **Configure environment variables** — create a `.env` file in the project root:
   ```env
   grok_api_key=<your-api-key>
   base_url=<openai-compatible-base-url>
   testmodel=<model-name-for-chatbot>
   modelAsJudge=<model-name-for-judge>
   confident-api-key=<your-confident-ai-key>
   ```

---

## Running the Chatbot

```bash
streamlit run chatbot.py
```

Opens at `http://localhost:8501`.

---

## Running Evaluations

```bash
# Evaluate using locally defined Goldens
pytest test/multipleMetricTest.py

# Evaluate using a dataset pulled from Confident AI
pytest test/pullingDatasetLLMTest.py
```

Results are printed to the console and synced to [Confident AI](https://app.confident-ai.com/).
