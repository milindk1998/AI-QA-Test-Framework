from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.dataset import EvaluationDataset, Golden


from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
)

from chatbot import ask_llm
from LLMModeAsJudge import DeepEvalLLM

judge = DeepEvalLLM()

# chatbot response
question1 = "What is Deep Evals in one sentence? \nothink"
question2 = "What is Goldens, Test cases and Dataset in one sentence? \nothink"
# question3 = "What is Generative AI? \nothink"

# actual_response1 = ask_llm(question1)
# actual_response2 = ask_llm(question2)
#actual_response3 = ask_llm(question3)

# expected responses is optional, if not provided, the evaluation will be based on the retrieval context only
expected_response1 = "Deep Evals is a framework for evaluating the performance of AI models."
expected_response2 = "Goldens are the correct answers used for evaluation, Test cases are individual evaluations, and Dataset is a collection of test cases."
#expected_response3 = "Generative AI refers to a class of artificial intelligence techniques that generate new content, such as text, images, or music, based on learned patterns from existing data."

retrieval_context = [
    """
    Deep Evals is a framework for evaluating the performance of AI models, particularly in the context of natural language processing and generative AI. It provides tools and metrics to assess the quality, relevance, and faithfulness of model outputs.
    Goldens are the correct answers or reference outputs used for evaluation.
    Test cases are individual evaluations that compare model outputs against goldens.
    Dataset is a collection of test cases used for systematic evaluation of AI models.

    """
]

goldens = [
    Golden(
        input=question1,
        expected_output=expected_response1,
        retrieval_context=retrieval_context
    ),
    Golden(
        input=question2,
        expected_output=expected_response2,
        retrieval_context=retrieval_context
    )
]

dataset = EvaluationDataset(goldens=goldens)

# print("Evaluating the model with multiple test cases...")
# print("Number of test cases:", len(dataset.goldens))
# print("Dataset is:", dataset)

# pushing datasets to confidentAI
# dataset.push(alias="Dataset for AI Test", finalized=True)

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

# test_case_1 = LLMTestCase(
#     input=question1,
#     actual_output=actual_response1,
#     expected_output=expected_response1,
#     retrieval_context=retrieval_context
# )

# test_case_2 = LLMTestCase(
#     input=question2,
#     actual_output=actual_response2,
#     expected_output=expected_response2,
#     retrieval_context=retrieval_context
# )

# test_case_3 = LLMTestCase(
#     input=question3,
#     actual_output=actual_response3,
#     expected_output=expected_response3,
#     retrieval_context=retrieval_context
# )

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
    # test_cases=[test_case_1, test_case_2],
    test_cases=test_cases,
    metrics=metrics,
)
