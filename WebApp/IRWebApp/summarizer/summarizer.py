# source: https://huggingface.co/kriton/greek-text-summarization
from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("kriton/greek-text-summarization")
model = AutoModelForSeq2SeqLM.from_pretrained("kriton/greek-text-summarization")

from transformers import pipeline

summarizer = pipeline("summarization", model="kriton/greek-text-summarization")

def generate_summary(article: str, max_length=512):
    inputs = tokenizer(
        'summarize: ' + article, 
        return_tensors="pt", 
        max_length=1024, 
        truncation=True,
        padding="max_length",
    )

    outputs = model.generate(
        inputs["input_ids"], 
        max_length=max_length, 
        min_length=130, 
        length_penalty=3.0, 
        num_beams=8, 
        early_stopping=True,
        repetition_penalty=3.0,
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# print(genarate_summary(article))