import os

import csv
import concurrent
import openai
import os
from tenacity import retry, wait_random_exponential, stop_after_attempt
import tiktoken
from tqdm import tqdm

GPT_MODEL = "gpt-3.5-turbo-0613"

openai.organization = "org-o6USUzxWV5fNZJxAVJjAGW1R"
openai.api_key = "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"

# Set a directory to read all tweets dataset
# Input dataset file 
tweets_dir_filepath = "./data/airline_test.csv"
uniqueairlines_keys = {}

def extract_training_tweets():
    tweets_map = {}
    uniqueairlines_set = set()
    with open(tweets_dir_filepath) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            tweet_key = row[0]
            airlines_value = row[1]
            tweets_map[tweet_key] = airlines_value
            airlines_value = airlines_value.translate({ord(i): None for i in '[]'})   #removing extra brackets
            airline_names = airlines_value.split(", ") 
            for eachairlinename in airline_names:
                if len(eachairlinename) != 0:
                   uniqueairlines_set.add(eachairlinename)
                   split_airlinename = eachairlinename.split(" ")
                   if len(split_airlinename) > 1:
                       keytemp = split_airlinename[0].translate({ord("'"): None}) #removing extra single quotes
                       uniqueairlines_keys[keytemp] = eachairlinename
    return tweets_map

# Split a text into smaller chunks of size n, preferably ending at the end of a tweet
def create_chunks(text, n, tokenizer):
    """Returns successive n-sized chunks from provided tweet text."""
    tokens = tokenizer.encode(text)
    i = 0
    while i < len(tokens):
        # Find the nearest end of tweet within a range of 0.5 * n and 1.5 * n tokens
        j = min(i + int(1.5 * n), len(tokens))
        while j > i + int(0.5 * n):
            # Decode the tokens and check for full stop or comma
            chunk = tokenizer.decode(tokens[i:j])
            if chunk.endswith(".") or chunk.endswith(","):
                break
            j -= 1
        # If no end of tweet found, use n tokens as the chunk size
        if j == i + int(0.5 * n):
            j = min(i + n, len(tokens))
        yield tokens[i:j]
        i = j
        
@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(3))
def extract_chunk(content, template_prompt):
    """This function applies a prompt to some input content. In this case it returns a tweet content text"""
    prompt = template_prompt + content
    response = openai.ChatCompletion.create(
        model=GPT_MODEL, messages=[{"role": "user", "content": prompt}], temperature=0
    )
    return response["choices"][0]["message"]["content"]

def extract_airlines(tweet):
    """This function extracts airline name(s) from each tweet """

    # A prompt to dictate how the recursive tweets should be processed
    initial_prompt = """Extract airline names from given dataset of tweets about airlines. \n\nContent:"""

    all_tweets = extract_training_tweets()
    
    # Initialise tokenizer
    tokenizer = tiktoken.get_encoding("cl100k_base")
    results = ""

    # Chunk up the tweet into 50 token chunks
    chunks = create_chunks(tweet, 50, tokenizer)
    text_chunks = [tokenizer.decode(chunk) for chunk in chunks]
    
    # Parallel process the tweet words
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=len(text_chunks)
    ) as executor:
        futures = [
            executor.submit(extract_chunk, chunk, initial_prompt)
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

#Input line
input_text = "US Airways @AmericanAir stranded in cold Texas and getting sick because you overbooked the flight and gave my seat away. #gooutofbusiness"
print(" Input text : ", input_text)
extract_response = extract_airlines(input_text)
extracted_content = extract_response['choices'][0]['message']['content']
substrings_text = extracted_content.split(" ")
results_list = []
for word in substrings_text:
    if word in uniqueairlines_keys:
        results_list.append(uniqueairlines_keys[word])

print(" Extracted airlines name values are : " , results_list)