import urllib.parse
from PIL import Image
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def render_html(html, output_image_path, reference_img_path):
    # Setup Selenium WebDriver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Load the reference image to get its dimensions
    reference_img = Image.open(reference_img_path)
    img_width, img_height = reference_img.size

    # Initialize blank canvas
    driver.get("about:blank")

    # Fetch generated html
    encoded_html = urllib.parse.quote(html)
    driver.get(f"data:text/html;charset=utf-8,{encoded_html}")

    # Set the viewport size to match the input image's dimensions
    driver.set_window_size(img_width, img_height)

    # Render component and save screenshot for reference
    sleep(3)
    driver.save_screenshot(output_image_path)
    driver.quit()

def load_file_content(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return None