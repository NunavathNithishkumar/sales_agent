This Streamlit application serves as an AI Sales Agent that generates answers to questions based on product information scraped from a given URL. The application does the web scraping and the Google Generative AI API for generating text-based answers.

## Overview

The application allows users to:
1. Enter a product URL to scrape product information.
2. Upload a file containing questions about the product.
3. Generate and display answers to those questions based on the scraped product information.

## Features

- Web Scraping: Uses the Firecrawl to extract product details from a given URL.
- Text Cleaning: Processes and cleans the scraped text data to make it suitable for generating answers.
- Answer Generation: Uses Google Generative AI to generate answers to user-uploaded questions based on the cleaned product information.
- Streamlit Interface: Provides a simple and interactive web interface for user input and output.

#Installation
git clone https://github.com/your/repository.git
cd repository

#Install dependencies:
pip install -r requirements.txt

#Run the Application:

streamlit run app.py


Deployed Link:https://ai-sales-agent.streamlit.app/
