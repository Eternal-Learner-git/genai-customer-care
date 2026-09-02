"""
Wraps a HuggingFace text-generation model as the LLM used for generating
suggested responses.

Uses google/flan-t5-base - an instruction-tuned model that's small enough
(~250M params) to run on a laptop CPU without needing a GPU, unlike larger
LLMs. Quality is decent for short, templated responses like this project
needs; if your team later has GPU access or an API budget, swapping in a
larger/hosted model here (e.g. via HuggingFace Inference API) is a drop-in
change - only this file needs to change, since the rest of the pipeline
just calls generate_response().
"""

from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline

MODEL_NAME = "google/flan-t5-base"

_llm = None


def _get_llm():
    global _llm
    if _llm is None:
        print(f"Loading LLM ({MODEL_NAME})... this downloads once, ~250MB")
        text_generation_pipeline = pipeline(
            "text2text-generation",
            model=MODEL_NAME,
            max_new_tokens=150,
            min_new_tokens=20,
            no_repeat_ngram_size=3,  # stops the model from repeating the same phrase, e.g. "I'm sorry to hear that." twice
            repetition_penalty=1.3,
            num_beams=4,  # beam search gives noticeably more coherent output than greedy decoding for a model this small
        )
        _llm = HuggingFacePipeline(pipeline=text_generation_pipeline)
    return _llm


def generate_response(prompt: str) -> str:
    """Sends a fully-built prompt to the LLM and returns the generated text."""
    llm = _get_llm()
    return llm.invoke(prompt).strip()
