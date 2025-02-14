from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from time import sleep
import urllib.parse
from PIL import Image, ImageChops
from webdriver_manager.chrome import ChromeDriverManager
import os

def render_html(combined_html):
    output_path='images/generated_component.png'

    # os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Set up Chrome options to run in headless mode
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Initialize the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Encode the HTML content to avoid rendering issues
    encoded_html = urllib.parse.quote(combined_html)
    driver.get(f'data:text/html;charset=utf-8,{encoded_html}')

    # Wait for the page to render
    sleep(3)

    # Debugging: Print the loaded page content
    # print(driver.page_source)
    driver.save_screenshot(output_path)  # Save as PNG image


    # Close the WebDriver
    driver.quit()

def compare_images(rendered_image_path, reference_image_path):
    # Open both the rendered image and the reference image
    rendered_image = Image.open(rendered_image_path).convert("RGB")  # Convert to RGB
    reference_image = Image.open(reference_image_path).convert("RGB")  # Convert to RGB

    # Generate the difference between the two images
    diff_image = ImageChops.difference(rendered_image, reference_image)

    # Check if the diff image has any non-zero values (indicating a difference)
    diff_stats = diff_image.getbbox()  # Get the bounding box of non-zero regions

    if diff_stats:
        print(f"Images are different! Differences found.")
        # diff_image.show()  # Optionally, show the diff image
        diff_image.save("images/diff_image.png")
    else:
        print("Images match!")