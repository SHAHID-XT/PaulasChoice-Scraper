# PaulasChoice Scraper

This project is a web scraper for the Paula's Choice ingredient dictionary. It collects details about various ingredients from the Paula's Choice website and saves the data in a JSON file.

## Table of Contents

- [PaulasChoice Scraper](#paulaschoice-scraper)
  - [Table of Contents](#table-of-contents)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Functions](#functions)
    - [run\_until\_it\_found](#run_until_it_found)
    - [get\_driver](#get_driver)
    - [remove\_dialog](#remove_dialog)
    - [find\_element](#find_element)
    - [load\_json](#load_json)
    - [save\_json](#save_json)
    - [Runner](#runner)
    - [get\_links\_](#get_links_)
    - [details](#details)
    - [get\_unavailable](#get_unavailable)
    - [get\_details](#get_details)
  - [Note](#note)

## Requirements

- Python 3.x
- Selenium
- BeautifulSoup4

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/paulaschoice-scraper.git
   cd paulaschoice-scraper
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the scraper:**
   ```bash
   python paulaschoice.py
   ```

The script will start a Chrome browser, navigate to the Paula's Choice ingredient dictionary, and begin scraping data.

## Functions

### run_until_it_found

This function keeps running until a modal dialog on the webpage is closed.

**Parameters:**

- `driver` (webdriver.Chrome): The Selenium WebDriver instance.

**Returns:** None

### get_driver

Initializes and configures a Chrome WebDriver instance.

**Returns:** 
- `webdriver.Chrome`: The configured Chrome WebDriver instance.

### remove_dialog

Removes any dialogs or pop-ups that appear on the webpage.

**Parameters:**

- `driver` (webdriver.Chrome): The Selenium WebDriver instance.

**Returns:** None

### find_element

Finds an element on a webpage using a specific locator.

**Parameters:**

- `driver` (webdriver.Chrome): The Selenium WebDriver instance.
- `BY` (selenium.webdriver.common.by.By): The type of locator (e.g., By.XPATH).
- `SELECTOR` (str): The locator string.
- `timeout` (int, optional): Maximum time to wait. Defaults to 5 seconds.

**Returns:** 
- `selenium.webdriver.remote.webelement.WebElement`: The found element or `None` if not found.

### load_json

Loads JSON data from a file.

**Parameters:**

- `filename` (str): The name of the file.

**Returns:** 
- `list`: The loaded JSON data or an empty list if the file does not exist.

### save_json

Saves JSON data to a file.

**Parameters:**

- `file_path` (str): The file name. Defaults to "data.json".
- `data` (list): The data to be saved.

**Returns:** None

### Runner

The main function that runs the web scraping process.

**Returns:** None

### get_links_

Scrapes all ingredient links from the webpage.

**Parameters:**

- `driver` (webdriver.Chrome): The Selenium WebDriver instance.

**Returns:** 
- `list`: A list of ingredient links.

### details

Retrieves detailed information about an ingredient from a given URL.

**Parameters:**

- `driver` (webdriver.Chrome): The Selenium WebDriver instance.
- `url` (str): The URL of the ingredient page.

**Returns:** 
- `dict`: A dictionary containing the ingredient details.

### get_unavailable

Retrieves unavailable ingredient data from the current webpage.

**Parameters:**

- `driver` (webdriver.Chrome): The Selenium WebDriver instance.

**Returns:** 
- `list`: A list of dictionaries with unavailable ingredient details.

### get_details

Extracts detailed information about an ingredient from a BeautifulSoup object.

**Parameters:**

- `soup` (BeautifulSoup): The BeautifulSoup object.

**Returns:** 
- `dict`: A dictionary with ingredient details.

## Note

- Make sure you have Google Chrome installed.
- The scraper might take some time to collect all data.
- The script handles pop-ups and other interruptions automatically.