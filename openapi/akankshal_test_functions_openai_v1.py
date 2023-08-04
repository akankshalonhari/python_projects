import os

import arxiv
import ast
import csv
import concurrent
from csv import writer
from IPython.display import display, Markdown, Latex
import json
import openai
import os
import pandas as pd
from PyPDF2 import PdfReader
import requests
from scipy import spatial
from tenacity import retry, wait_random_exponential, stop_after_attempt
import tiktoken
from tqdm import tqdm
from termcolor import colored
import pprint

GPT_MODEL = "gpt-3.5-turbo-0613"

openai.organization = "org-o6USUzxWV5fNZJxAVJjAGW1R"
openai.api_key = "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"

# Set a directory to read all tweets dataset 
tweets_dir_filepath = "./data/airline_train.csv"
uniqueairlines_dict = {}

def extract_training_tweets():
    alltweets = {}
    uniqueairlines_set = set()
    with open(tweets_dir_filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            key = row[0]
            value = row[1]
            alltweets[key] = value
            value = value.translate({ord(i): None for i in '[]'})
            val_arr = value.split(", ")
            for val in val_arr:
                if len(val) != 0:
                   uniqueairlines_set.add(val)
                   sub_val = val.split(" ")
                   if len(sub_val) > 1:
                       keytemp = sub_val[0].translate({ord("'"): None})
                       uniqueairlines_dict[keytemp] = val

    return alltweets

# Split a text into smaller chunks of size n, preferably ending at the end of a sentence
def create_chunks(text, n, tokenizer):
    """Returns successive n-sized chunks from provided text."""
    tokens = tokenizer.encode(text)
    i = 0
    while i < len(tokens):
        # Find the nearest end of sentence within a range of 0.5 * n and 1.5 * n tokens
        j = min(i + int(1.5 * n), len(tokens))
        while j > i + int(0.5 * n):
            # Decode the tokens and check for full stop or newline
            chunk = tokenizer.decode(tokens[i:j])
            if chunk.endswith(".") or chunk.endswith(","):
                break
            j -= 1
        # If no end of sentence found, use n tokens as the chunk size
        if j == i + int(0.5 * n):
            j = min(i + n, len(tokens))
        yield tokens[i:j]
        i = j
        
@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def extract_chunk(content, template_prompt):
    """This function applies a prompt to some input content. In this case it returns a summarized chunk of text"""
    prompt = template_prompt + content
    response = openai.ChatCompletion.create(
        model=GPT_MODEL, messages=[{"role": "user", "content": prompt}], temperature=0
    )
    return response["choices"][0]["message"]["content"]

def extract_airlines(tweet):
    """This function extracts airline name(s) from each tweet """

    # A prompt to dictate how the recursive summarizations should approach the input paper
    summary_prompt = """Extract airline names from given dataset of tweets about airlines. \n\nContent:"""

    all_tweets = extract_training_tweets()
    
    # Initialise tokenizer
    tokenizer = tiktoken.get_encoding("cl100k_base")
    results = ""

    # Chunk up the document into 1500 token chunks
    chunks = create_chunks(tweet, 1500, tokenizer)
    text_chunks = [tokenizer.decode(chunk) for chunk in chunks]
    
    # Parallel process the summaries
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=len(text_chunks)
    ) as executor:
        futures = [
            executor.submit(extract_chunk, chunk, summary_prompt)
            for chunk in text_chunks
        ]
        with tqdm(total=len(text_chunks)) as pbar:
            for _ in concurrent.futures.as_completed(futures):
                pbar.update(1)
        for future in futures:
            data = future.result()
            results += data

    # Final extraction from input tweet
    response = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {
                "role": "user",
                "content": f"""Extract airline names from given tweet about airlines ::
                        User tweet: {tweet}
                        Airline names:\n{results}\n""",
            }
        ],
        temperature=0,
    )
    return response

extract_response = extract_airlines("US Airways i tried it but doesnt help very much and Reservation seems to be overwhelmed with some issues")
extracted_names = extract_response['choices'][0]['message']['content']
sub_arr = extracted_names.split(" ")
results_list = []
for val in sub_arr:
    if val in uniqueairlines_dict:
        results_list.append(uniqueairlines_dict[val])

print(" Extracted airlines name values are : " , results_list)