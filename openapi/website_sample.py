import openai

openai.api_key = "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"

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {
      "role": "user",
      "content": "Make a single page website that shows off different neat javascript features for drop-downs and things to display information. The website should be an HTML file with embedded javascript and CSS."
    }
  ],
  temperature=0,
  max_tokens=2048,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0
)

result = response['choices'][0]['message']['content']
print(result)
