from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from time import time
from os import path
import re
from bs4 import BeautifulSoup

# There are two models that we tested
# 1. "facebook/bart-large-cnn"
# 2. "philschmid/bart-large-cnn-samsum"

model_fn, text_fn = "facebook/bart-large-cnn", "./npocrawler/site_sarsef_org/text-.txt"
local_model_fn = "./hf_models/" + model_fn.split("/")[1]
s = time()

if not path.exists(local_model_fn):
    print(f"{model_fn} not saved locally, downloading...")
    # Trigger the download by doing this
    summarizer = pipeline("summarization", model=model_fn)
    summarizer.save_pretrained(local_model_fn)

tokenizer = AutoTokenizer.from_pretrained(local_model_fn)
model = AutoModelForSeq2SeqLM.from_pretrained(local_model_fn)
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
print(f"Model located in {time() - s}")

with open(text_fn, "r") as f:
    text = f.read().replace("\n", " ").replace("\t", " ")

# Remove all of the lines with only spaces
text = re.sub("\s\s+", " ", text)

print("-----------------")
print(text)
print("-----------------")


# Chunk everything into num_words so that model can summarize that text
num_words = 512

# Break everything into words
text_array = text.split(" ")

# Break the text into parts for the summarization
parts = []
for i in range(0, len(text_array), num_words):
    parts.append(" ".join(text_array[i:(i+num_words)]))

print(f"- Original text was {len(text)} characters and {len(text_array)} words")
print(f"- Broke text into {len(parts)} batches to support summarization")

for p in parts:
    summary = summarizer(p)
    print(f"Summary: {summary[0]['summary_text']}")
    print("")