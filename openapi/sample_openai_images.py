import os
import openai
import requests  # used to download images
from PIL import Image  # used to print and edit images cmd : python3 -m pip install Pillow 
from IPython.display import display

openai.organization = "org-o6USUzxWV5fNZJxAVJjAGW1R"
openai.api_key = "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"

openai.Model.list()

# set a directory to save DALL·E images to
image_dir_name = "images"
image_dir = os.path.join(os.curdir, image_dir_name)

# create the directory if it doesn't yet exist
if not os.path.isdir(image_dir):
    os.mkdir(image_dir)

# print the directory to save to
print(f"{image_dir=}")

# create an image

# set the prompt
prompt = "A cyberpunk monkey hacker dreaming of a beautiful bunch of bananas, digital art"

# call the OpenAI API
generation_response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="1024x1024",
    response_format="url",
)

# print response
print(generation_response)

# save the image
generated_image_name = "generated_image.png"  # any name you like; the filetype should be .png
generated_image_filepath = os.path.join(image_dir, generated_image_name)
generated_image_url = generation_response["data"][0]["url"]  # extract image URL from response
generated_image = requests.get(generated_image_url).content  # download the image

with open(generated_image_filepath, "wb") as image_file:
    image_file.write(generated_image)  # write the image to the file

# print the image
print(generated_image_filepath)
display(Image.open(generated_image_filepath))
