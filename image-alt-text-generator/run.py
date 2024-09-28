import os
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image
import io
import tkinter as tk
from tkinter import filedialog

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from the .env file
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_image_alt_text(image_path):
    # Load the image
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Open the image using PIL to check its size and format (optional)
    img = Image.open(io.BytesIO(image_data))
    width, height = img.size
    image_format = img.format

    # Prepare the prompt for the LLM
    prompt = f"Generate an alt text for an image with dimensions {width}x{height}, format {image_format}. \
               The image file is described as follows:"

    # Call the GPT-4 API to generate alt text
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates accurate alt text for images."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract and return the generated alt text
    alt_text = response['choices'][0]['message']['content']
    return alt_text

def select_file():
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open a file dialog and return the selected file path
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[
            ("Image Files", ("*.jpg","*.jpeg","*.png","*.gif","*.bmp")),
            ("JPEG Files", "*.jpg"),
            ("PNG Files", "*.png"),
            ("GIF Files", "*.gif"),
            ("BMP Files", "*.bmp"),
            ("All Files", "*.*")  # This line will allow all file types to be shown
        ],
        initialdir='/mnt/c/Users/jsega/Downloads/'
    )
    return file_path

# Example usage
image_path = select_file()
if image_path:  # Check if a file was selected
    alt_text = get_image_alt_text(image_path)
    print(f"Generated Alt Text: {alt_text}")
else:
    print("No file selected.")
