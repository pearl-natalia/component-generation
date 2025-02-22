import os, re
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from render import render_html, load_file_content

# Setup
load_dotenv()
gemini_api_key = os.getenv("GEMINI_FLASH_API_KEY")
genai.configure(api_key=gemini_api_key)
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Model initialization
model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
)

# Setting up generator
history = [] 
reference_img_path = "data/reference.png"
generated_image_path = "data/generated.png"
generated_html_path = "data/generated.html"
reference_img = Image.open(reference_img_path)

def generate_history_prompt(): 
    history_prompt = f"Review the previous iterations to understand what changes have already been made. Here is the chat history:"
    for i, message in enumerate(history, start=1):
        history_prompt += f"\nIteration {i}: {message}"
        return history_prompt

# Few shot learning
example_input_html = load_file_content('few-shot-learning/sample1/sample-input1.html')
sample_output_html = load_file_content('few-shot-learning/sample1/sample-output1.html')
sample_input_img = Image.open('few-shot-learning/sample1/sample-input1.png')
sample_output_img = Image.open('few-shot-learning/sample1/sample-output1.png')

def example_prompt(n):
    exmaple =   f"""
                    <EXAMPLE>
                        INPUT HTML: {example_input_html}
                        INPUT IMAGE is {n+1} attatched image
                        OUTPUT GENERATED HTML: {sample_output_html}
                        OUTPUT GENERATED IMAGE is {n+2} attatched image
                    </EXAMPLE>
                """
    return exmaple

chat_session = model.start_chat(history=[
    # genai.Message(role="user", text=sample_prompt),
    # genai.Message(role="model", text=sample_output_html)
])

# ----- Iteration 1 -----
print('1')
input_html = load_file_content('data/reference.html')
prompt =f"""
            You are an expert front end web developer. Your job is to generate html and css to recreate the following component: {input_html} 
            and ensure it looks like the render of the component (attached image). Only output html+css as it output will directly be rendered.
        """
instruction_1 = f""" 
                    Integrate css into html. 
                    Replace all <img> components with a plain div that says 'placeholder' in the center, in a contrasting colour to the div colour. 
                    Do not recreate the <img> components. Ensure all the colours match the image, including the font colours. 
                    Ensure the dimensions are the same relative to the image and match the image. 
                    Do not hardcode pixel sizes, use relative positioning and sizing to make the component responsive. 
                    The goal is to recreate the image with html + css.
                """
contents = [
    prompt,
    instruction_1,
    example_prompt(1),
    reference_img,
    sample_input_img,
    sample_output_img

]

# Processing results
generated_html = re.sub(r'^```html\s*|```$', '', chat_session.send_message(contents).text)
history.append({"request": instruction_1, "response": generated_html})
with open(generated_html_path, "w", encoding="utf-8") as file:
    file.write(generated_html)
render_html(generated_html, generated_image_path, reference_img_path)


# ----- Iteration 2 -----
print('2')
input_html = load_file_content(generated_html_path)
input_img = Image.open(generated_image_path)

prompt =f"""
            You are an expert front end web developer. Your job is to adjust the following html/css: {input_html} 
            so that it's corresponding render (the first attached image) resembles the target render of the component (the second attached image) better: {reference_img}.
        """

instruction_2 = f"""Adjust the html structure css colours. Extract pixels to get the exact same font colours. 
                    Use inline style elements to directly change the colour of the text. 
                    Ensure the dimensions and positioning of the elements also resemble the image.
                """

contents = [
    prompt,
    instruction_2,
    generate_history_prompt(),
    example_prompt(2),
    input_img,
    reference_img,
    reference_img,
    sample_input_img,
    sample_output_img

]

# Processing results
generated_html = re.sub(r'^```html\s*|```$', '', chat_session.send_message(contents).text)
history.append({"request": instruction_2, "response": generated_html})
with open(generated_html_path, "w", encoding="utf-8") as file:
    file.write(generated_html)
render_html(generated_html, generated_image_path, reference_img_path)


# ----- Iteration 3 -----
print('3')
input_html = load_file_content(generated_html_path)
input_img = Image.open(generated_image_path)
instruction_3 = f"Adjust the fonts, and colours in the html/css if needed to make the generated render (first image attached) resemble the target render of the component (second attached image)."

contents = [
    prompt,
    instruction_3,
    generate_history_prompt(),
    example_prompt(2),
    input_img,
    reference_img,
    sample_input_img,
    sample_output_img
]

# Processing results
generated_html = re.sub(r'^```html\s*|```$', '', chat_session.send_message(contents).text)
history.append({"request": instruction_3, "response": generated_html})
with open(generated_html_path, "w", encoding="utf-8") as file:
    file.write(generated_html)
render_html(generated_html, generated_image_path, reference_img_path)