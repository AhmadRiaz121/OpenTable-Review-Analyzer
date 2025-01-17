# AI Restaurant Reviews Project

## Overview
This project involves scraping restaurant reviews from OpenTable, analyzing and categorizing the reviews using prompt engineering, and displaying the results in a user-friendly dashboard. Additionally, it includes a competitor analysis feature and a chatbot for querying information about staff/service.

## Features
1. **Web Scraping**:
   - 🕵️‍♂️ Scrapes reviews of a restaurant with over 1500 reviews using BeautifulSoup and Selenium.
   - 📋 Extracts information: Restaurant name, review content, ratings, and dates.
   - 💾 Stores data in JSON/CSV format.

2. **Prompt Engineering**:
   - 💡 Analyzes reviews using provided skeleton code.
   - 🍽️ Categorizes comments about food quality and staff/service.
   - 🚫 Ensures no hallucinations and excludes personal information.
   - 📁 Saves data as a .json file.

3. **GUI Development**:
   - 🌟 Creates a dashboard with Streamlit.
   - 🖼️ Displays all reviews in a user-friendly format.
   - ✨ Highlights food and staff/service comments with different colors.

4. **Competitor Analysis**:
   - 🏆 Enables selection of competitor restaurants.
   - 📊 Scrapes and visualizes ratings over time for both restaurants.
   - 📈 Plots bar graph showing rating trends.

5. **Chatbot Integration**:
   - 🤖 Integrates a chatbot for querying staff/service information.

6. **Flexible Review Extraction**:
   - 🔗 Allows extraction of reviews for any restaurant by providing its link.
