import torch
from transformers import pipeline


def init_model():
    hf_name = 'pszemraj/led-large-book-summary'

    summarizer = pipeline(
        "summarization",
        hf_name,
        device=0 if torch.cuda.is_available() else -1,
    )
    return summarizer


def inference(summarizer, text):
    # if text is list, return a summary for each text in the list
    # if text is string, return a summary for the text
    summary = summarizer(text, min_length=16, max_length=48)
    return summary[0]['summary_text']
