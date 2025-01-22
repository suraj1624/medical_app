import os
import base64
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
# api = os.getenv("api")
api_key = st.secrets["api_keys"]["api_key"]

# Function to encode the image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Initialize Groq client
client = Groq(api_key=api_key)

# Define the prompt
def generate_prompt(user_input):
    return f"""Your role here is to read the image and summarize the content given in simple words.
    Also, you need to provide content in hummanize way to it is not detected by AI tools. Additional instruction: {user_input}"""

# Streamlit UI
st.title("Image Description Chatbot")

# User input for image and prompt
uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
user_prompt = st.text_input("Enter your prompt", "Describe the image in simple words.")

# Process the image and prompt
if uploaded_image:
    # Save the uploaded image temporarily
    image_path = "uploaded_image.png"
    with open(image_path, "wb") as f:
        f.write(uploaded_image.getbuffer())

    # Encode the image to base64
    base64_image = encode_image(image_path)

    # Generate the prompt
    prompt = generate_prompt(user_prompt)

    # Call Groq API with the image and prompt
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="llama-3.2-11b-vision-preview",
        )
        
        # Display the model's response
        st.subheader("Response:")
        st.write(chat_completion.choices[0].message.content)

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Please upload an image to get started.")
