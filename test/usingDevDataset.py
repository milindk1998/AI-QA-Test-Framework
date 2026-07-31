import json
from deepeval import evaluate
from deepeval.dataset import EvaluationDataset, Golden
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase

from chatbot import ask_llm
from LLMModeAsJudge import DeepEvalLLM
from langchain_core.messages import SystemMessage, HumanMessage

judge = DeepEvalLLM()

# Step 1: creating a dataset from the dev.json file
dataset = EvaluationDataset()

with open("../dev.json", "r") as f:
    data = json.load(f)

for article in data["data"]:
    for para in article["paragraphs"]:
        context = para["context"]
        for qa in para["qas"]:
            expected_output = qa["answers"][0]["text"] if qa["answers"] else None
            dataset.add_golden(
               Golden(
                    input=qa["question"],
                    expected_output=expected_output,
                    retrieval_context=[context]
               )
            )


# dataset.push('dev_dataset')

# Step 2: Convert the golden test cases into LLMTestCase objects and evaluate them
for golden in dataset.goldens[:2]:  # Limiting to the first 2 golden dataset for demonstration
    context_text = "\n\n".join(golden.retrieval_context) if golden.retrieval_context else ""
    messages = [
        SystemMessage(content=f"Use the following context to answer the question: \n\n {context_text} If the answer is not present in the context, respond with 'I don't know.'"),
        HumanMessage(content=f"{golden.input}")
    ]
    test_case = LLMTestCase(
                input=golden.input, 
                actual_output=ask_llm(messages),
                expected_output=golden.expected_output,
                retrieval_context=golden.retrieval_context
            )
    dataset.add_test_case(test_case)

metrics = [
    AnswerRelevancyMetric(
        model=judge,
        threshold=0.7,
        include_reason=True
    ),
    FaithfulnessMetric(
        model=judge,
        threshold=0.7,
        include_reason=True
    )
]

evaluate(
    test_cases=dataset.test_cases,
    metrics=metrics,
)