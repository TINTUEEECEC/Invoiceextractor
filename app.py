import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os
from PIL import Image
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model=genai.GenerativeModel("models/gemini-1.5-flash")
def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def get_image_bytes_and_mime(uploaded_file):
    # Read file as bytes
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
    
        # Return in list of dictionary
        return [{"data": bytes_data, "mime_type": uploaded_file.type}]
    else:
        raise FileNotFoundError("No file uploaded")


st.set_page_config(page_title="Multi language Invoice Extractor")
st.header("Multi language Invoice Extractor")
input = st.text_input("Input prompt:", key="input")
# File uploader
uploaded_file = st.file_uploader("Choose an image of the invoice...", type=["jpg", "jpeg", "png"])


image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_container_width=True)

submit=st.button("Tell me about invoice")

input_prompt = """ 
You are an expert in understanding invoices. we will upload an image as invoice
and you will have to answer any questions based on the uploaded invoice image
"""

if submit:
    image_data = get_image_bytes_and_mime(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)

