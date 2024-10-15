import re
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
import os

def simple_word_tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

def simple_sentence_tokenize(text):
    return re.split(r'(?<=[.!?])\s+', text)

def preprocess_text(text):
    stop_words = set(['the', 'a', 'an', 'in', 'on', 'at', 'for', 'to', 'of', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'be', 'been'])
    words = simple_word_tokenize(text)
    return [word for word in words if word not in stop_words]

def summarize_article(text, num_sentences=5):
    sentences = simple_sentence_tokenize(text)
    preprocessed_text = preprocess_text(text)
    
    word_frequencies = defaultdict(int)
    for word in preprocessed_text:
        word_frequencies[word] += 1
    
    sentence_scores = defaultdict(int)
    for sentence in sentences:
        for word in preprocess_text(sentence):
            if word in word_frequencies:
                sentence_scores[sentence] += word_frequencies[word]
    
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:num_sentences]
    summary_sentences = sorted(summary_sentences, key=sentences.index)
    summary = ' '.join(summary_sentences)
    
    return summary

def fetch_article(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script in soup(["script", "style"]):
            script.decompose()
        
        paragraphs = soup.find_all('p')
        text = ' '.join([p.get_text() for p in paragraphs])
        
        text = re.sub(r'\s+', ' ', text) 
        text = text.strip()
        
        return text
    except requests.RequestException as e:
        print(f"Error fetching the article: {e}")
        return None

def summarize_from_url(url, num_sentences=5):
    article_text = fetch_article(url)
    if article_text:
        summary = summarize_article(article_text, num_sentences)
        return summary
    else:
        return "Failed to fetch or summarize the article."

def save_summary_to_file(summary, filename="summary.txt"):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(summary)
        print(f"Summary saved to {filename}")
    except IOError as e:
        print(f"Error saving summary to file: {e}")


url = "https://spacenews.com/falcon-9-launches-esas-hera-asteroid-mission/"
summary = summarize_from_url(url, num_sentences=3)
print(summary)

save_summary_to_file(summary)
