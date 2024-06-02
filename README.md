# Async Web Scraper for Inshorts

This project is an asynchronous web scraper that fetches and parses articles from the Inshorts website. It uses Playwright for automated browsing and BeautifulSoup for HTML parsing. The extracted data is stored in CSV, JSON files, and an SQLite database.

## Features

- Asynchronously fetch content from Inshorts
- Click on "Load more" button multiple times to get more articles
- Parse HTML content to extract article details
- Save extracted data in CSV and JSON formats
- Store data in an SQLite database

## Requirements

- Python 3.7+
- Playwright
- BeautifulSoup
- Pandas
- NumPy
- SQLAlchemy (for database handling)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/peterkacmarik/async-web-scraper-inshorts.git
    cd async-web-scraper-inshorts
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Install Playwright and its browser binaries:
    ```sh
    playwright install
    ```

## Usage

To run the scraper, execute the following command:
```sh
python main.py
```

You will be prompted to enter a category to scrape from the predefined set of URLs. For example, you can enter `india`, `business`, `politics`, `sports`, etc.

### Example

```sh
Enter category to scrape like (india, business, politics, sports, etc.): technology
```

The script will fetch the content from the specified URL, click on the "Load more" button multiple times, parse the HTML content, and save the data in CSV, JSON files, and an SQLite database.

## Code Overview

### `fetch_content(url, num_clicks)`

This function fetches the content from a given URL by clicking on the "Load more" button a specified number of times.

### `parse_content(html_content)`

This function parses the HTML content and extracts information about articles, including category, titles, dates, descriptions, and URLs.

### `main()`

This function orchestrates the scraping process, including fetching and parsing content, and saving the resulting data to files and a database.

## Directory Structure

```plaintext
async-web-scraper-inshorts/
├── dataset/
│   ├── inshorts_category_YYYY-MM-DD_HH-MM.csv
│   └── inshorts_category_YYYY-MM-DD_HH-MM.json
├── database/
│   ├── models.py
│   ├── sqlite.db
├── main.py
└── README.md
```

- `dataset/`: Directory where the scraped data will be saved.
- `database/`: Directory containing database models and database sqlite.db.
- `main.py`: Main script to run the web scraper.
- `README.md`: This README file.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
This project is for educational purposes only. Always respect the terms of use of the websites you are scraping.

## Acknowledgements

- [Playwright](https://playwright.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/)

```
