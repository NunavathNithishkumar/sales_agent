import streamlit as st
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os 
import re
import google.generativeai as genai


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
load_dotenv()

# Configure API keys
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
FIRECRAWL_API_KEY = os.getenv('FIRECRAWL_API_KEY')
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY 
genai.configure(api_key=GOOGLE_API_KEY)

def scrape_data(url):
    app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
    scraped_data = app.scrape_url(url)
    
    # Check if 'markdown' key exists in the scraped data
    if 'markdown' in scraped_data:
        return scraped_data['markdown']
    else:
        raise KeyError("The key 'markdown' does not exist in the scraped data.")

def clean_text(text):
    # Remove URLs
    text = re.sub(r'http\S+', '', text) 
    text = text.replace('\n', ' ').strip()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(Overview|Specifications|Dimensions|Weight|Features|Details):', r'\n\1:', text)
    return text


def clean_product_info(data):
    # Handle the case where data is a string
    if isinstance(data, str):
        return clean_text(data)
    
    cleaned_data = {}
    for key, value in data.items():
        cleaned_data[key] = clean_text(value) if value != "Product info not found." else value
    return cleaned_data


def generate_answer(question, context):
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(f"Answer the following question based on the context provided:\n\nContext: {context}\n\nQuestion: {question}")
    return response.text

def main():
    st.title("AI Sales Agent")
    
   
    url = st.text_input("Enter the product URL")
    
    # File uploader for questions
    uploaded_file = st.file_uploader("Upload a file containing questions", type="txt")
    
    if st.button("Generate Answers") and url and uploaded_file:
        # Scrape data from URL
        try:
            scraped_markdown = scrape_data(url)
            final_text = clean_product_info(scraped_markdown)
                        
            # Read and process the uploaded file
            questions = uploaded_file.read().decode("utf-8").splitlines()
            
            # Generate answers
            for question in questions:
                if question.strip():
                    answer = generate_answer(question, final_text)
                    st.subheader(f"Question: {question}")
                    st.write(f"Answer: {answer}")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
