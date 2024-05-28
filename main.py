import asyncio
from datetime import datetime
import numpy as np
import pandas as pd
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from database.models import Inshorts, DatabaseManagerSettings


async def fetch_content(url, num_clicks):
    """
    Asynchronously fetches the content from a given URL by clicking on the "Load more" button a specified number of times.

    Args:
        url (str): The URL to fetch the content from.
        num_clicks (int): The number of times to click on the "Load more" button.

    Returns:
        str: The fetched content as a string.

    Raises:
        Exception: If an unhandled exception occurs during the fetching process.

    Note:
        - This function uses Playwright to launch a browser, navigate to the specified URL, and click on the "Load more" button.
        - The function waits for the "Load more" button to be visible before clicking on it.
        - If the element is not visible or available, the function ends the loop.
        - The function closes the browser after fetching the content.

    Example:
        >>> content = await fetch_content("https://example.com", 5)
        Click To 'Load More' 1: The element was clicked successfully.
        Click To 'Load More' 2: The element was clicked successfully.
        Click To 'Load More' 3: The element was clicked successfully.
        Click To 'Load More' 4: The element was clicked successfully.
        Click To 'Load More' 5: The element was clicked successfully.
        Time taken to click: 0:00:05
        >>> print(content)
        "<html><head>...</head><body>...</body></html>"
    """
    try:
        # Content fetching with Playwright
        async with async_playwright() as p:
            # Browser launch
            browser: any = await p.chromium.launch(headless=True)

            # New page creation
            page: any = await browser.new_page()

            # Page navigation
            await page.goto(url)

            # Wait for the element to be visible
            await page.wait_for_selector("div.QMXJlc3R5MMJjDGSV4Jd")

            # Click on the "Load more" button twice
            try:
                start_time_click = datetime.now()
                for click in range(num_clicks):
                    await page.click("div.QMXJlc3R5MMJjDGSV4Jd")
                    print(f"Click To 'Load More' {click + 1}: The element was clicked successfully.")

                    # Delay between clicks
                    await asyncio.sleep(1)  # Short pause between clicks

                end_time_click = datetime.now()
                print(f"Time taken to click: {end_time_click - start_time_click}")
            except AttributeError:
                # If the element is not visible or available, the loop ends
                print("The element is not visible, I'm done.")
            except Exception:
                # Catching any unhandled exceptions
                print("An unhandled exception occurred:")
                raise

            # Page content
            content: str = await page.content()

            # Close browser
            await browser.close()

            # Return content
            return content
    except Exception:
        # Catching any unhandled exceptions
        print("An unhandled exception occurred:")
        raise


async def parse_content(html_content):
    """
    Parses the HTML content and extracts information about articles.

    Args:
        html_content (str): The HTML content to be parsed.

    Returns:
        dict: A dictionary containing the extracted information about the articles. The dictionary has the following keys:
            - "category" (list): The category of each article.
            - "titles" (list): The titles of each article.
            - "date" (list): The dates of each article.
            - "descriptions" (list): The descriptions of each article.
            - "urls" (list): The URLs of each article.

    Raises:
        AttributeError: If a null pointer reference is encountered.
        Exception: If an unhandled exception occurs.

    Note:
        - The function uses BeautifulSoup to parse the HTML content.
        - It searches for specific HTML elements to extract the required information.
        - The extracted information is stored in a dictionary.
        - If an article does not have a URL, a None value is appended to the "urls" list.
        - The "category" list is populated with the same value for all articles.

    Example:
        html_content = "<html><body><div class='article'><h1>Article 1</h1><p>Description 1</p><span class='date'>2022-01-01</span></div><div class='article'><h1>Article 2</h1><p>Description 2</p><span class='date'>2022-01-02</span></div></body></html>"
        result = parse_content(html_content)
        print(result)
        # Output:
        # {
        #     "category": ["category"],
        #     "titles": ["Article 1", "Article 2"],
        #     "date": ["2022-01-01", "2022-01-02"],
        #     "descriptions": ["Description 1", "Description 2"],
        #     "urls": [None, None]
        # }
    """
    try:
        # Content processing with BeautifulSoup
        soup: BeautifulSoup = BeautifulSoup(html_content, "html.parser")

        # Search all links
        titles: list = soup.select("div.VdsPqrmJYY7F2MNUKOwQ span.S2DdZEgzkqC9bYeTJUGw")
        descriptions: list = soup.select("div.Hxtmf9GvkV8Ti6V0GUSn")
        dates: list = soup.select("span.date")

        select_category = soup.select_one("div.EJbGYqFfRQOwX_PmlB2H a")
        category = select_category.get("href").split("/")[-1]

        # Dictionary with data
        detail_data = {
            "category": [],
            "titles": [title.get_text(strip=True) for title in titles if title.get_text(strip=True)],
            "date": [date.get_text(strip=True) for date in dates if date.get_text(strip=True)],
            "descriptions": [description.get_text(strip=True) for description in descriptions if description.get_text(strip=True)],
            "urls": [],
        }
        # Search all url links and append them to the list
        start_point: list = soup.select("div.TfxplVx3RtbilOD2tqd6")
        
        # Add url to the list
        for point in start_point:
            try:
                urls: str = (point.select_one("div.c80ZAVi5M80kecYskLY3 a")["href"] if point.select_one("div.c80ZAVi5M80kecYskLY3 a") else None)
            except AttributeError:
                urls = np.nan
            detail_data["urls"].append(urls)

        # Add category to the list
        for _ in range(len(detail_data["titles"])):
            detail_data["category"].append(category)

        # Return dictionary
        return detail_data
    
    except AttributeError as e:
        # Handle null pointer references
        print(f"A null pointer reference was encountered: {e}")
    except Exception as e:
        # Handle any unhandled exceptions
        print(f"An unhandled exception occurred: {e}")
    return None


async def main():
    """
    Asynchronously fetches and parses content from a given category URL, and saves the resulting DataFrame to a CSV file, JSON file, and SQLite database.

    This function prompts the user to enter a category to scrape from a predefined set of URLs. It then fetches the content from the specified URL using Playwright and clicks on the "Load more" button a specified number of times. The fetched HTML content is then parsed using BeautifulSoup to extract relevant data. The extracted data is stored in a DataFrame and printed to the console. The DataFrame is then saved to a CSV file, JSON file, and an SQLite database. The table in the SQLite database is created using the DatabaseManagerSettings class. Finally, the DataFrame is saved to the SQLite database and the database connection is closed.

    Parameters:
        None

    Returns:
        None
    """
    # Category URL
    category_urls = {
        "india": "https://inshorts.com/en/read/national",
        "business": "https://inshorts.com/en/read/business",
        "politics": "https://inshorts.com/en/read/politics",
        "sports": "https://inshorts.com/en/read/sports",
        "technology": "https://inshorts.com/en/read/technology",
        "startups": "https://inshorts.com/en/read/startup",
        "entertainment": "https://inshorts.com/en/read/entertainment",
        "hatke": "https://inshorts.com/en/read/hatke",
        "international": "https://inshorts.com/en/read/world",
        "automobile": "https://inshorts.com/en/read/automobile",
        "science": "https://inshorts.com/en/read/science",
        "travel": "https://inshorts.com/en/read/travel",
        "miscellaneous": "https://inshorts.com/en/read/miscellaneous",
    }

    # URL to scrape
    category = input("Enter category to scrape like (india, business, politics, sports, etc.): ")
    url = category_urls[category]
    
    # Number of clicks to perform
    num_clicks: int = 10

    # Content fetching with Playwright
    html_content: str = await fetch_content(url, num_clicks)

    # Content parsing with BeautifulSoup
    detail_data = await parse_content(html_content)

    # Create a DataFrame from the dictionary data and print it
    df: pd.DataFrame = pd.DataFrame(detail_data)
    print(df)

    # Save the DataFrame to a CSV file, JSON file, and SQLite database
    date_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
    df.to_csv(f"async-web-scraper-inshorts/dataset/inshorts_{category}_{date_time}.csv", index=False, encoding="utf-8")
    df.to_json(f"async-web-scraper-inshorts/dataset/inshorts_{category}_{date_time}.json", orient="records", indent=4)

    # Create a table in the Sqlite database
    db_manager_settings = DatabaseManagerSettings()
    # db_manager_settings.create_table(Inshorts.__table__)

    # Save the DataFrame to the Sqlite database
    db_manager_settings.insert_data(df, Inshorts)

    # Close the database connection
    db_manager_settings.close_connection()


# Run the main function asynchronously
asyncio.run(main())
