from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import pandas as pd

def scrape_website():
    # Initialize Selenium WebDriver
    driver = webdriver.Chrome()

    # Navigate to the initial URL
    initial_url = "https://www.pmindia.gov.in/en/"
    driver.get(initial_url)

    # Wait for the link with class 'bttn' to appear
    try:
        link_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.bttn'))
        )
    except:
        print("Timeout waiting for the button element to appear.")
        driver.quit()
        return None

    # Extract the link URL using the 'href' attribute
    link_url = link_element.get_attribute("href")

    # Navigate to the extracted link URL
    driver.get(link_url)

    # Initialize the last_height variable
    last_height = driver.execute_script("return document.body.scrollHeight")

    # Initialize a counter for titles scraped
    title_count = 0

    while True:
        # Scroll down to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for the page to load
        time.sleep(2)  # Adjust the wait time as needed

        # Calculate the new page height
        new_height = driver.execute_script("return document.body.scrollHeight")

        # If the page height hasn't changed, break the loop
        if new_height == last_height:
            break

        # Update the last page height
        last_height = new_height
        
        # Increment the title count
        title_count += 1
        
        # If we have scraped 500 titles, break the loop
        if title_count == 500:
            break

    # Initialize a list to store data
    rows = []

    # Get the page source after scrolling and waiting for dynamic content to load
    page_source = driver.page_source

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find all div tags with class "news-description"
    news_divs = soup.find_all('div', class_='news-description')

    # Loop through each div
    for div in news_divs:
        # Extract the date
        span_date = div.find('span', class_='date')
        date = span_date.text.strip() if span_date else None
        
        # Extract the content
        p_tag = div.find('p')
        content = p_tag.text.strip() if p_tag else None
        
        # Extract the title and link
        a_tag = div.find('a')
        title = a_tag.get('title') if a_tag else None
        link = a_tag.get('href') if a_tag else None
        
        # Append data to the rows list
        rows.append({'Title': title,'Date': date, 'Content': content,})

        # Break the loop if 500 titles are scraped
        if len(rows) == 500:
            break

    # Create a DataFrame from the extracted data
    df = pd.DataFrame(rows)

    # Close the WebDriver
    driver.quit()
    
    return df

def save_to_csv(df):
    if df is not None:
        save_path = r"C:\Users\SSC\Desktop\output_scrapping\scraped_data.csv"  # Path to save the CSV file
        try:
            df.to_csv(save_path, index=False)
            print("Data saved successfully to:", save_path)
        except Exception as e:
            print("Error occurred while saving the data:", e)

def main():
    print("Scraping website...")
    df = scrape_website()

    if df is not None:
        save_to_csv(df)

if __name__ == "__main__":
    main()
