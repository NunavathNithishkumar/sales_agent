import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
import os
import google.generativeai as genai


GOOGLE_API_KEY = "AIzaSyAXikz6RA-CZqLUgPuGf7xawwEs8JV72r4"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

PRODUCT_URL = 'https://www.tp-link.com/in/home-networking/smart-plug/hs100/'

# Function to scrape product information
def scrape_product_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_info = {}

    # Extract data from 'product-info' class
    product_info_section = soup.find('div', {'class': 'product-info'})
    product_info['product_info'] = product_info_section.get_text(strip=True) if product_info_section else "Product info not found."

    # Extract data from 'specifications' class
    specifications_section = soup.find('div', {'class': 'specifications'})
    product_info['specifications'] = specifications_section.get_text(strip=True) if specifications_section else "Specifications not found."

    # Extract data from 'overview' class
    overview_section = soup.find('div', {'class': 'overview'})
    product_info['overview'] = overview_section.get_text(strip=True) if overview_section else "Overview not found."

    return product_info

# Function to clean text
def clean_text(text):
    text = text.replace('\n', ' ').strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(Overview|Specifications|Dimensions|Weight|Features|Details):', r'\n\1:', text)
    return text

# Function to clean product info
def clean_product_info(data):
    cleaned_data = {}
    for key, value in data.items():
        cleaned_data[key] = clean_text(value) if value != "Product info not found." else value
    return cleaned_data

# Function to generate answers using Google Generative AI
def generate_answer(question, context):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(f"Answer the following question based on the context provided :\n\nContext: {context}\n\nQuestion: {question}.")
    return response.text

# Streamlit app
def main():
    st.title("Product Information Q&A")

    # Upload file
    uploaded_file = st.file_uploader("Choose a text file with questions", type="txt")

    if uploaded_file:
        product_info = scrape_product_info(PRODUCT_URL)
        cleaned_data = clean_product_info(product_info)

        questions = uploaded_file.read().decode("utf-8").splitlines()

        # Process questions
        for question in questions:
            context = ' '.join(cleaned_data.values())
            answer = generate_answer(question, context)
            st.write(f"Question: {question}")
            st.write(f"Answer: {answer}")

if __name__ == "__main__":
    main()