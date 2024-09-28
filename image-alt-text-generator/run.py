import os
from openai import OpenAI
from dotenv import load_dotenv
import base64
import mimetypes
import tkinter as tk
from tkinter import filedialog

# Load environment variables from .env file
load_dotenv()

# Set up the OpenAI API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_description(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        mt = mimetypes.guess_type(image_path)
        image_url = f"data:{mt[0]};base64,{encoded_string}"

    # Use GPT-4 to generate a description based on the image
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are an AI that generates descriptive text for images based on their features."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "What is this an image of?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ])

    # Extract and return the generated alt text
    alt_text = response.choices[0].message.content
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
            ("All Files", "*.*")
        ]#,
        # initialdir='/mnt/c/Users/jsega/Downloads/'
    )
    return file_path

image_path = select_file()
if image_path:
    description = generate_description(image_path)
    print(f"Generated Description: {description}")
else:
    print("No file selected.")
