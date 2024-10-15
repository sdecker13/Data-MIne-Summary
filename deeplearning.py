import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import requests
from bs4 import BeautifulSoup

def get_article_from_url(url):
    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    paragraphs = soup.find_all('p')
    article_text = ' '.join([p.get_text() for p in paragraphs])
    
    return article_text

def summarize_article(article_text, max_length=300):
    model_name = "t5-small"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)

    input_text = "summarize: " + article_text

    input_ids = tokenizer.encode(input_text, return_tensors="pt", max_length=512, truncation=True)
    input_ids = input_ids.to(device)

    summary_ids = model.generate(input_ids, max_length=max_length, num_beams=4, length_penalty=2.0, early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary

def summarize_from_url(url, max_length=150):
    article_text = get_article_from_url(url)
    return summarize_article(article_text, max_length)

url = "https://spacenews.com/impulse-space-wins-34-5-million-contract-for-u-s-space-force-missions/"
summary = summarize_from_url(url)
print("Summary:", summary)
