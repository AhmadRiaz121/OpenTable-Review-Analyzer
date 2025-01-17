import streamlit as st
import pandas as pd
import csv
import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from groq import Groq


driver=webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
df=pd.read_csv("reviews.csv")

# Define function to call Groq API
client=Groq(
    api_key="API_KEY"
)

def chat_with_groq(message):
    chat_completion=client.chat.completions.create(
        messages=[{
            "role": "user",
            "content": message,
        }],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content


# Streamlit app configuration
st.set_page_config(page_title="Gary Danko Reviews", page_icon="🍽️", layout="wide")

st.title("Gary Danko Restaurant Reviews Dashboard 🍽️")
st.markdown("""
    <p style="font-size: 1.1rem; color: #555555;">
        Search for reviews of the famous Gary Danko restaurant based on food or staff/service.
        Get insights from real customer feedback and discover what they love most! 😍
    </p>
""", unsafe_allow_html=True)


def create_bar_chart(data):
    plt.figure(figsize=(10, 6))
    plt.bar(data.index, data.values)
    plt.xlabel("Rating")
    plt.ylabel("Count")
    plt.title("Rating Distribution")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt)


def scrap_reviews_from_page(url, restaurant_name):
    driver.get(url)
    soup=BeautifulSoup(driver.page_source, "html.parser")
    reviews=[]

    review_container=soup.find_all('div', class_='MpiILQAMSSg-')
    for review in review_container:
        review_text=review.find('div', class_='_6rFG6U7PA6M-').get_text(strip=True)
        review_rating_text=review.find('li', class_='-k5xpTfSXac-').get_text(strip=True)
        reviews.append({
            'restaurant_name': restaurant_name,
            'review_text': review_text,
            'review_rating': review_rating_text
        })
    return reviews


def scrap_all_reviews(url, restaurant_name, max_page=3):
    all_reviews=[]
    for page_num in range(1, max_page + 1):
        current_url=f"{url}&page={page_num}"
        reviews=scrap_reviews_from_page(current_url, restaurant_name)
        all_reviews.extend(reviews)
        time.sleep(2)
    return all_reviews


def save_reviews_to_csv(reviews, filename='competitor_reviews.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer=csv.writer(file)
        writer.writerow(['restaurant_name', 'review_text', 'review_rating'])
        for review in reviews:
            writer.writerow([review['restaurant_name'], review['review_text'], review['review_rating']])
    
    df=pd.read_csv("competitor_reviews.csv")
    create_bar_chart(df['review_rating'].value_counts())


# Competitor URL and reviews scraping
competitor_url=st.text_input("Enter the competitor restaurant OpenTable URL:")
if st.button("Scrape Reviews"):
    if competitor_url:
        restaurant_name="Competitor Restaurant"
        reviews=scrap_all_reviews(competitor_url, restaurant_name)
        save_reviews_to_csv(reviews)
        st.success(f"Scraped and saved reviews for {restaurant_name}")


def highlight_text(text, search_term, highlight_emoji, highlight_class):
    if isinstance(text, str):
        return text.replace(search_term, f"{highlight_emoji} <span class='{highlight_class}'>{search_term}</span>") 
    return text

create_bar_chart(df['review_rating'].value_counts())


# Chatbot integration in Streamlit sidebar
st.sidebar.title("Gary Danko Reviews Chatbot 🤖")
chat_option=st.sidebar.selectbox("Analyze reviews for:", ["Food 🍔", "Staff/Service 👨‍🍳"])
chat_prompt=st.sidebar.text_area("Enter your query about reviews")
if st.sidebar.button("Ask Chatbot") and chat_prompt:
    response=chat_with_groq(chat_prompt)
    st.sidebar.markdown(f"**Chatbot Response:** {response}")

# Search functionality for reviews
search_option=st.selectbox("Search for:", ["Reviews of Food 🍔", "Reviews of Staff/Service 👨‍🍳"], key="search_option")
filtered_df=df.copy()

if search_option == "Reviews of Food 🍔":
    food_item=st.text_input("Search for a food item in the reviews", placeholder="e.g., 'lobster', 'pasta', 'dessert'")
    if food_item:
        filtered_df=filtered_df[filtered_df["review_text"].str.contains(food_item, case=False, na=False)]

elif search_option == "Reviews of Staff/Service 👨‍🍳":
    service_item=st.text_input("Search for a staff/service mention in the reviews", placeholder="e.g., 'waiter', 'service', 'staff'")
    if service_item:
        filtered_df=filtered_df[filtered_df["review_text"].str.contains(service_item, case=False, na=False)]

if not filtered_df.empty:
    for index, row in filtered_df.iterrows():
        highlighted_review=highlight_text(row["review_text"], "food", "🍽️", "food-highlight")
        highlighted_review=highlight_text(highlighted_review, "service", "👨‍🍳", "service-highlight")
        st.markdown(f"### {row['restaurant_name']} 🍴")
        st.markdown(f"**Rating**: {row['review_rating']} / 5 ⭐")
        st.markdown(f"**Review**: {highlighted_review}", unsafe_allow_html=True)
        st.markdown("---")
else:
    st.write(f"No reviews found for the given search criteria at Gary Danko.")
