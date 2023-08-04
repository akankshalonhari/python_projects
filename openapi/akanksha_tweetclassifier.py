import os
import openai

openai.api_key = "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"

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "system",
      "content": "You will be provided with a dataset of tweets about airlines and task is to extract airline names."
    },
    {
      "role": "user",
      "content": "What are the airlines in this tweet?"
    }
  ],
  temperature=0,
  max_tokens=256,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

result = response['choices'][0]['message']['content']
print(result)
