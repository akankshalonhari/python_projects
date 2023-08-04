import openai
import pandas as pd
import numpy as np
import json
import os
from tenacity import retry, wait_random_exponential, stop_after_attempt

openai.api_key = "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"
COMPLETIONS_MODEL = "text-davinci-002"

#transactions = pd.read_csv('./data/25000_spend_dataset_current.csv', encoding= 'unicode_escape')
transactions = pd.read_csv('./data/airline_train.csv', encoding= 'unicode_escape')
#print(len(transactions))

#print(transactions.head())
#print(transactions.columns)

@retry(wait=wait_random_exponential(min=1, max=40), stop=stop_after_attempt(1))
def request_completion(prompt):
    
    completion_response =   openai.Completion.create(
                            prompt=prompt,
                            temperature=0,
                            max_tokens=5,
                            top_p=1,
                            frequency_penalty=0,
                            presence_penalty=0,
                            model=COMPLETIONS_MODEL
                            )
        
    return completion_response

def classify_transaction(transaction,prompt):
    
    prompt = prompt.replace('TWEET_LINE',transaction['tweet'])
    prompt = prompt.replace('AIRLINES_LIST',transaction['airlines'])
    
    classification = request_completion(prompt)['choices'][0]['text'].replace('\n','')
    
    return classification

zero_shot_prompt = '''You are a data expert working for the National Library of Scotland. 
You are analysing all transactions over £25,000 in value and classifying them into one of five categories.
The five categories are Building Improvement, Literature & Archive, Utility Bills, Professional Services and Software/IT.
If you can't tell what it is, say Could not classify
                      
Transaction:
                      
Supplier: SUPPLIER_NAME
Description: DESCRIPTION_TEXT
Value: TRANSACTION_VALUE
                      
The classification is:'''

# Get a test transaction
transaction = transactions.iloc[0]

# Interpolate the values into the prompt
prompt = zero_shot_prompt.replace('TWEET_TEXT',transaction['tweet'])
prompt = prompt.replace('AIRLINES_LIST',transaction['airlines'])

# Use our completion function to return a prediction
completion_response = request_completion(prompt)
print(completion_response)
print(completion_response['choices'][0]['text'])

test_transactions = transactions.iloc[:25]
test_transactions['Classification'] = test_transactions.apply(lambda x: classify_transaction(x,zero_shot_prompt),axis=1)
print(test_transactions['Classification'].value_counts())
print(test_transactions.head(25))
