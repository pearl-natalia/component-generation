import os, re, time
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
from render import render_html, load_file_content

# CONSTANTS
REFERENCE_IMG_PATH = "results/reference.png"
REFERENCE_HTML_PATH = "results/reference.html"
GENERATED_IMG_PATH = "results/generated.png"
GENERATED_HTML_PATH = "results/generated.html"

def format_css(css):
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

    model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    )
    chat_session = model.start_chat()

    formatter_prompt = "Format the following code to a correct css format and place inside body. Only output the css as it will directly be input into a .css file."
    example_formatting = """
                        Here is an example for reference. Only output the <EXAMPLE OUTPUT> section, without the xml headers.
                        <EXAMPLE INPUT> 
                        {
                            "backgroundColor": "black",
                            "borderColor": "white",
                            "borderRadius": "5px"
                        }
                        </EXAMPLE INPUT>
                        <EXAMPLE OUTPUT> 
                                body{
                                    background-color: black;
                                    border-color: white;
                                    border-radius: 5px;
                                }
                        </EXAMPLE OUTPUT>
                        """
    output = chat_session.send_message([formatter_prompt, example_formatting]).text
    return re.sub(r'^```css\s*|```$', '', output)

def main():
    # Model Setup
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

    model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config=generation_config,
    )
    history = []
    chat_session = model.start_chat()


    # Setting up generator
    reference_img = Image.open(REFERENCE_IMG_PATH)

    def generate_history_prompt(): 
        history_prompt = f"Review the previous iterations to understand what changes have already been made. Here is the chat history:"
        for i, message in enumerate(history, start=1):
            history_prompt += f"\nIteration {i}: {message}"
            return history_prompt

    def process_results(instruction):
        generated_html = re.sub(r'^```html\s*|```$', '', chat_session.send_message(contents).text)
        history.append({"request": instruction, "response": generated_html})
        with open(GENERATED_HTML_PATH, "w", encoding="utf-8") as file:
            file.write(generated_html)
        render_html(generated_html, GENERATED_IMG_PATH, REFERENCE_IMG_PATH)



    # Few shot learning
    example_input_html = load_file_content('few-shot-learning/sample1/sample-input1.html')
    sample_output_html = load_file_content('few-shot-learning/sample1/sample-output1.html')
    sample_input_img = Image.open('few-shot-learning/sample1/sample-input1.png')
    sample_output_img = Image.open('few-shot-learning/sample1/sample-output1.png')

    def example_prompt(n):
        example =   f"""
                        <EXAMPLE>
                            INPUT HTML: {example_input_html}
                            INPUT IMAGE is {n+1} attatched image
                            OUTPUT GENERATED HTML: {sample_output_html}
                            OUTPUT GENERATED IMAGE is {n+2} attatched image
                        </EXAMPLE>
                    """
        return example


    # ----- Iteration 1 -----
    print('1')
    input_html = load_file_content(REFERENCE_HTML_PATH)
    prompt =f"""
                You are an expert front end web developer. Your job is to generate html and css to recreate the following component: (image attatched). 
                you can use the following html as a starting point, but you may move around the structue if needed to better resemble the image. 
                Ensure the generated component looks like the render of the component (attatched image). Here is the html: {input_html}. 
                Only output html+css as it output will directly be rendered.
            """
    instruction_1 = f""" 
                        Integrate css into html. 
                        Replace all <img> components with a plain div that says 'placeholder' in the center, in a contrasting colour to the div colour. Comment out the <img> component and add a 'placeholder image' comment above it. 
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
    process_results(instruction_1)


    # ----- Iteration 2 -----
    print('2')
    input_html = load_file_content(GENERATED_HTML_PATH)
    input_img = Image.open(GENERATED_IMG_PATH)

    prompt =f"""
                You are an expert front end web developer. Your job is to adjust the following html/css: {input_html} 
                so that it's corresponding render (the first attached image) resembles the target render of the component (the second attached image) better: {reference_img}.
            """

    instruction_2 = f"""Adjust the html structure and css colours. Extract pixels to get the exact same font colours. 
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
    process_results(instruction_2)


    # ----- Iteration 3 -----
    print('3')
    input_html = load_file_content(GENERATED_HTML_PATH)
    input_img = Image.open(GENERATED_IMG_PATH)
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
    process_results(instruction_3)

if __name__ == '__main__':
    timer = 10  

    # Stall until reference html and image are loaded or timer runs out
    while timer > 0 and not (os.path.exists(REFERENCE_HTML_PATH) and os.path.exists(REFERENCE_IMG_PATH)):
        print("Waiting for files to appear...")
        time.sleep(1)  
        timer -= 1  

    if timer == 0:
        print("Files not found. Exiting...")
        exit()

    print("Starting generation...")
    main()