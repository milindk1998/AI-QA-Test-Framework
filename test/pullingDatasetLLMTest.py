from deepeval import evaluate
from deepeval.dataset import EvaluationDataset
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.test_case import LLMTestCase

from chatbot import ask_llm
from LLMModeAsJudge import DeepEvalLLM

# we have pushed pur dataset to confident ai and now we will just pull it and use it to test LLM

judge = DeepEvalLLM()

dataset = EvaluationDataset()
dataset.pull(alias="Dataset for AI Test", finalized=True)

test_cases = []

for golden in dataset.goldens:
    response = ask_llm(golden.input)
    test_cases.append(
            LLMTestCase(
                input=golden.input, 
                actual_output=response,
                expected_output=golden.expected_output,
                retrieval_context=golden.retrieval_context
            )
    )

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
    test_cases=test_cases,
    metrics=metrics,
)