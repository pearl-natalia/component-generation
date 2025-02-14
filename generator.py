import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from render import render_html, compare_images


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
example_prompt = "What is the capital of France?"
example_response = "The capital of France is Paris."

chat_session = model.start_chat(history=[
    # Content(role="user", parts=[Part(text=example_prompt)]),
    # Content(role="model", parts=[Part(text=example_response)])
])

# Prompt
context =   """ 
            You are a generator who takes in html and css code retreived from inspect element, 
            as well as a render of the component. Your goal is to recreate this component. For all image components, don't recreate the content inside the image. Just fill the parent div of the img with grey.
            For any image, comment out the html for the <img> component, add a comment above saying "Place image here". Ensure the css is encapsulated into the html. Rename the divs to be more general.
            And instead, add an svg and text saying "image placeholder". 
            Add a comment at the start and end of the placeholder code saying "placeholder image". For all urls, just convert them into empty strings (i.e. svg = ""). Important: only output the code, no additional text.
            """
# Keep doing actions like these to make the component as general and template like as possible, replacing text with header1, header2, etc etc. 
# Rename the divs etc to make more general and template like. 


html = """<div class="framer-rtm0D framer-18fox64 framer-v-18fox64 highlighted" data-framer-name="Desktop A" style="width: 100%; opacity: 1;"><div class="framer-76sdne" data-framer-name="Tabs" style="opacity: 1;"><div class="framer-qsd4di-container" style="opacity: 1;"><div class="framer-ivjHz framer-j6ddtg framer-v-wonpkm" data-framer-name="Active" data-highlight="true" style="background-color: rgba(97, 97, 97, 0.23); border-radius: 16px; width: 100%; opacity: 1;" tabindex="0"><div class="framer-1ew66qe" data-framer-name="Content" style="opacity: 1;"><div class="framer-1ua0ylq" data-framer-name="Text and supporting text" style="opacity: 1;"><div class="framer-j70d99" data-framer-name="Text" style="outline: none; display: flex; flex-direction: column; justify-content: flex-start; flex-shrink: 0; --extracted-r6o4lv: rgb(255, 255, 255); --framer-paragraph-spacing: 20px; transform: none; opacity: 1;" data-framer-component-type="RichTextContainer"><p style="--font-selector:R0Y7QmUgVmlldG5hbSBQcm8tNTAw;--framer-font-family:&quot;Be Vietnam Pro&quot;, &quot;Be Vietnam Pro Placeholder&quot;, sans-serif;--framer-font-size:22px;--framer-font-weight:500;--framer-letter-spacing:-0.03em;--framer-line-height:135%;--framer-text-color:var(--extracted-r6o4lv, rgb(255, 255, 255))" class="framer-text">Integrate your product development providers</p></div><div class="framer-cchw1j" data-framer-name="Supporting text" style="outline: none; display: flex; flex-direction: column; justify-content: flex-start; flex-shrink: 0; --extracted-r6o4lv: rgb(255, 255, 255); --framer-paragraph-spacing: 0px; transform: none; opacity: 1;" data-framer-component-type="RichTextContainer"><p style="--framer-letter-spacing:-0.02em;--framer-line-height:140%;--framer-text-color:var(--extracted-r6o4lv, rgb(255, 255, 255))" class="framer-text">Connect GitHub, GitLab, Azure DevOps, Bitbucket, Slack and Jira to Mimrr for seamless tracking of code and issue updates.</p></div></div></div></div></div><div class="framer-12bg141-container" style="opacity: 1;"><div class="framer-ivjHz framer-j6ddtg framer-v-j6ddtg" data-framer-name="Default" data-highlight="true" style="background-color: rgba(0, 0, 0, 0); border-radius: 16px; width: 100%; opacity: 1;" tabindex="0"><div class="framer-1ew66qe" data-framer-name="Content" style="opacity: 1;"><div class="framer-1ua0ylq" data-framer-name="Text and supporting text" style="opacity: 1;"><div class="framer-j70d99" data-framer-name="Text" style="outline: none; display: flex; flex-direction: column; justify-content: flex-start; flex-shrink: 0; --extracted-r6o4lv: rgba(255, 255, 255, 0.35); --framer-paragraph-spacing: 20px; transform: none; opacity: 1;" data-framer-component-type="RichTextContainer"><p style="--font-selector:R0Y7QmUgVmlldG5hbSBQcm8tNTAw;--framer-font-family:&quot;Be Vietnam Pro&quot;, &quot;Be Vietnam Pro Placeholder&quot;, sans-serif;--framer-font-size:22px;--framer-font-weight:500;--framer-letter-spacing:-0.03em;--framer-line-height:135%;--framer-text-color:var(--extracted-r6o4lv, rgba(255, 255, 255, 0.35))" class="framer-text">Setup your project and onboard your team</p></div><div class="framer-cchw1j" data-framer-name="Supporting text" style="outline: none; display: flex; flex-direction: column; justify-content: flex-start; flex-shrink: 0; --extracted-r6o4lv: rgba(224, 224, 224, 0.35); --framer-paragraph-spacing: 0px; transform: none; opacity: 1;" data-framer-component-type="RichTextContainer"><p style="--framer-letter-spacing:-0.02em;--framer-line-height:140%;--framer-text-color:var(--extracted-r6o4lv, rgba(224, 224, 224, 0.35))" class="framer-text">Add a code repository, ticket/issues group, communications channel and product team to your project.</p></div></div></div></div></div><div class="framer-1288w3b-container" style="opacity: 1;"><div class="framer-ivjHz framer-j6ddtg framer-v-j6ddtg" data-framer-name="Default" data-highlight="true" style="background-color: rgba(0, 0, 0, 0); border-radius: 16px; width: 100%; opacity: 1;" tabindex="0"><div class="framer-1ew66qe" data-framer-name="Content" style="opacity: 1;"><div class="framer-1ua0ylq" data-framer-name="Text and supporting text" style="opacity: 1;"><div class="framer-j70d99" data-framer-name="Text" style="outline: none; display: flex; flex-direction: column; justify-content: flex-start; flex-shrink: 0; --extracted-r6o4lv: rgba(255, 255, 255, 0.35); --framer-paragraph-spacing: 20px; transform: none; opacity: 1;" data-framer-component-type="RichTextContainer"><p style="--font-selector:R0Y7QmUgVmlldG5hbSBQcm8tNTAw;--framer-font-family:&quot;Be Vietnam Pro&quot;, &quot;Be Vietnam Pro Placeholder&quot;, sans-serif;--framer-font-size:22px;--framer-font-weight:500;--framer-letter-spacing:-0.03em;--framer-line-height:135%;--framer-text-color:var(--extracted-r6o4lv, rgba(255, 255, 255, 0.35))" class="framer-text">Finally, See Mimrr in action</p></div><div class="framer-cchw1j" data-framer-name="Supporting text" style="outline: none; display: flex; flex-direction: column; justify-content: flex-start; flex-shrink: 0; --extracted-r6o4lv: rgba(224, 224, 224, 0.35); --framer-paragraph-spacing: 0px; transform: none; opacity: 1;" data-framer-component-type="RichTextContainer"><p style="--framer-letter-spacing:-0.02em;--framer-line-height:140%;--framer-text-color:var(--extracted-r6o4lv, rgba(224, 224, 224, 0.35))" class="framer-text">Effortlessly automate unit test, codebase documentation, writing tickets, reporting requirements, PR reviews, etc.</p></div></div></div></div></div></div><div class="framer-45n3gc" data-framer-name="Image Container" style="border-radius: 13px; opacity: 1;"><div class="framer-v06fyg" data-border="true" data-framer-name="tab_image_01" style="--border-bottom-width: 2px; --border-color: rgb(97, 97, 97); --border-left-width: 2px; --border-right-width: 2px; --border-style: solid; --border-top-width: 2px; border-radius: 12px; opacity: 1;"><div style="position:absolute;border-radius:inherit;top:0;right:0;bottom:0;left:0" data-framer-background-image-wrapper="true"><img decoding="async" loading="lazy" sizes="max((min(73.4286vw - 160px, 1280px) - 56px) / 2, 1px)" srcset="https://framerusercontent.com/images/5TQFlpnABJ8MmFnqwnDnO5Mo7c.png?scale-down-to=1024 1023w,https://framerusercontent.com/images/5TQFlpnABJ8MmFnqwnDnO5Mo7c.png?scale-down-to=2048 2047w,https://framerusercontent.com/images/5TQFlpnABJ8MmFnqwnDnO5Mo7c.png 2051w" src="https://framerusercontent.com/images/5TQFlpnABJ8MmFnqwnDnO5Mo7c.png?scale-down-to=1024" alt="" style="display:block;width:100%;height:100%;border-radius:inherit;object-position:center;object-fit:cover" class=""></div></div></div></div>"""
css = """{
  "backgroundColor": "rgba(0, 0, 0, 0)",
  "border": "0px none rgb(0, 0, 0)",
  "borderRadius": "0px",
  "color": "rgb(0, 0, 0)",
  "fontFamily": "sans-serif",
  "fontSize": "12px",
  "fontWeight": "400",
  "height": "612.586px",
  "margin": "0px",
  "padding": "0px",
  "width": "1279.99px"
} """

task =  """ 
        Here is the html: {html}. Here is the css: {css}. 
        The rendered image provided is how the component should look.
        """ 

# Multimodal: Upload Image
image_path = "images/tmp.png" 
try:
    image = Image.open(image_path)
except FileNotFoundError:
    print(f"Error: Image file not found at {image_path}")
    exit()
except Exception as e:
    print(f"Error opening image: {e}")
    exit()


# Send prompt
prompt = "Here is your role: {context}. Here is your task: {task}."  
def load_file_content(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:  # Explicit encoding
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None

tmp_html = load_file_content('./sample.html')
tmp_css = load_file_content('./sample.css')
contents = [
    # context,
    # prompt,
    "generate me html and css to recreate the following component. {tmp_html} {tmp_css}. Integrate css into html. Replace all <img> components with a plain div that says 'placeholder'. Do not recreate the <img> components.",
    image
]

print('Sending...')
generated_html = chat_session.send_message(contents).text
render_html(generated_html)
print(generated_html)
compare_images("images/generated_component.png", image_path)
