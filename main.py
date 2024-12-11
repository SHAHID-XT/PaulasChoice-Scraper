from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import threading
import time


class Paulaschoice:

    filename = "paulaschoice.json"
    base_url = "https://www.paulaschoice.com/ingredient-dictionary"
    is_page_done = False
    unavailable_data = []

    def run_until_it_found(self, driver):
        """
        This function is used to keep running until a specific condition is met.
        In this case, it waits for a modal dialog to close on the webpage.

        Parameters:
        driver (webdriver.Chrome): The Selenium WebDriver instance used to interact with the webpage.

        Returns:
        None
        """
        while True:
            try:
                driver.execute_script(
                    'document.querySelectorAll("div[aria-modal=\'true\'")[1].querySelector("span").click()'
                )
            except:
                pass
            if self.is_page_done:
                break
            time.sleep(1)

    def get_driver(self):
        """
        This function initializes and configures a Chrome WebDriver instance.
        It also starts a separate thread to run the `run_until_it_found` method.

        Returns:
        webdriver.Chrome: The configured Chrome WebDriver instance.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-extensions")
        options.add_argument("--log-level=3")
        options.add_experimental_option(
            "excludeSwitches", ["enable-automation", "enable-logging"]
        )
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument("--lang=en-US")
        driver = webdriver.Chrome(options=options)
        threading.Thread(target=self.run_until_it_found, args=(driver,)).start()
        self.driver = driver
        return driver

    def remove_dialog(self, driver):
        """
        This function removes any dialogs or pop-ups that may appear on the webpage.
        It tries to find and click on a button with the text 'Continue to US Site' and then
        tries to close any modal dialogs by executing JavaScript code.

        Parameters:
        driver (webdriver.Chrome): The Selenium WebDriver instance used to interact with the webpage.

        Returns:
        None
        """
        try:
            self.find_element(
                driver, By.XPATH, "//button[text()='Continue to US Site']"
            ).click()
        except:
            pass
        try:
            driver.execute_script(
                'document.querySelectorAll("div[aria-modal=\'true\'")[1].querySelector("span").click()'
            )
        except:
            pass

    def find_element(self, driver, BY, SELECTOR, timeout=5):
        """
        This function is used to find an element on a webpage using a specific locator.
        It uses the WebDriverWait class from the selenium.webdriver.support module to wait for the element to be present.

        Parameters:
        driver (webdriver.Chrome): The Selenium WebDriver instance used to interact with the webpage.
        BY (selenium.webdriver.common.by.By): The type of locator to be used (e.g., By.XPATH, By.ID, etc.).
        SELECTOR (str): The locator string to identify the element on the webpage.
        timeout (int, optional): The maximum time to wait for the element to be present. Defaults to 5 seconds.

        Returns:
        selenium.webdriver.remote.webelement.WebElement: The found element if it is present within the specified timeout.
        None: If the element is not found within the specified timeout.
        """
        try:
            return WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((BY, SELECTOR))
            )
        except:
            return None

    def load_json(self, filename):
        """
        Load JSON data from a file.

        Parameters:
        filename (str): The name of the file to load JSON data from.

        Returns:
        list: A list containing the loaded JSON data. If the file does not exist or is empty, an empty list is returned.
        """

        data = []
        try:
            with open(filename, "r") as json_file:
                data = json.load(json_file)
        except:
            pass
        return data

    def save_json(self, file_path="data.json", data=[]):
        """
        Save JSON data to a file.

        Parameters:
        file_path (str): The name of the file to save JSON data to. Defaults to "data.json".
        data (list): The list of data to be saved as JSON. Defaults to an empty list.

        Returns:
        None

        Note:
        This method currently overwrites the existing file content. If you want to append data to an existing file,
        you need to modify the code accordingly.
        """
        # old_data = self.load_json(file_path)

        # if old_data:
        #     data.extend(old_data)

        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

    def Runner(self):
        """
        The main function to run the web scraping process.

        This function initializes the WebDriver, navigates to the base URL, removes any dialogs,
        selects the 'All' category, retrieves all ingredient links, and then iterates through each link
        to extract detailed information about the ingredients.

        Parameters:
        None

        Returns:
        None
        """
        extracted_data = []
        driver = self.get_driver()
        driver.get(self.base_url)
        time.sleep(2)
        self.remove_dialog(driver)
        driver.find_elements(By.XPATH, "//a[text()='All']")[0].click()
        all_links = self.get_links_(driver)
        print()
        print()
        print("Total links found: %d" % len(all_links))

        if self.unavailable_data:
            self.save_json("unavailable_data.json", self.unavailable_data)

        print(f"Total Unavailable link: {len(self.unavailable_data)}")

        self.save_json("all_links.json", all_links)
        for index, link in enumerate(all_links):
            print(f"Getting data out of : {index+1}/{len(all_links)}")
            try:
                d = self.details(driver, link)
                if d:
                    extracted_data.append(d)
            except KeyboardInterrupt as e:
                print("keyboard interrupt...")
                break
            except Exception as e:
                pass

        self.is_page_done = True
        self.save_json(self.filename, extracted_data)
        try:
            driver.close()
        except:
            pass

    def get_links_(self, driver):
        """
        This function is responsible for scraping all the ingredient links from the webpage.
        It uses a while loop to keep navigating through the pages until no more links are found.
        It also handles potential issues such as loading more content dynamically.

        Parameters:
        driver (webdriver.Chrome): The Selenium WebDriver instance used to interact with the webpage.

        Returns:
        list: A list of all the ingredient links found on the webpage.
        """
        all_links = []
        counts = 0
        all_counts = 0
        while True:
            time.sleep(5)
            read_more_elements = []
            count = 0
            while True:
                read_more_elements = driver.find_elements(
                    By.XPATH, "//*[text()='Read More']"
                )

                if len(driver.find_elements(By.TAG_NAME, "h3")) >= 2000:
                    break
                else:
                    count += 1
                    time.sleep(2)

                if count > 5:

                    break
                next_page = self.find_element(
                    driver, By.XPATH, "//a[@aria-label='Next Page' and text()='>']"
                )
                if not next_page:
                    break

            soup = BeautifulSoup(driver.page_source, "html.parser")
            elements = soup.find_all(string="Read More")
            links = [
                "https://www.paulaschoice.com/" + f.parent.parent.get("href")
                for f in elements
            ]
            d = self.get_unavailable(driver)
            print(f"Getting Links: {len(links)}/{len(d)}")
            all_links.extend(links)
            if not links:
                all_counts += 1
            else:
                all_counts = 0

            if d:
                self.unavailable_data.extend(d)

            next_page = self.find_element(
                driver, By.XPATH, "//a[@aria-label='Next Page' and text()='>']"
            )
            if next_page:
                next_page.click()
            else:
                break
            time.sleep(1)
        return all_links

    def details(self, driver, url):
        """
        This function retrieves detailed information about an ingredient from a given URL.

        Parameters:
        driver (webdriver.Chrome): The Selenium WebDriver instance used to interact with the webpage.
        url (str): The URL of the ingredient page to scrape.

        Returns:
        dict: A dictionary containing the scraped ingredient details.

        Note:
        - If a driver instance is not provided, it will be initialized using the `get_driver` method.
        - The function waits until the page is loaded by finding the presence of an <h1> tag.
        - The scraped details are obtained by parsing the HTML content using BeautifulSoup and calling the `get_details` method.
        - The URL of the ingredient page is added to the returned dictionary.
        """

        if self.driver:
            driver = self.driver

        if not driver:
            driver = self.get_driver()
            self.driver = driver

        driver.get(url)
        self.find_element(driver, By.TAG_NAME, "h1")  # waiting until the page is loaded
        soup = BeautifulSoup(driver.page_source, "html.parser")
        data = self.get_details(soup)
        data["url"] = url
        return data

    def get_unavailable(self, driver):
        """
        This function retrieves unavailable ingredient data from the current webpage.

        Parameters:
        driver (webdriver.Chrome): The Selenium WebDriver instance used to interact with the webpage.

        Returns:
        list: A list of dictionaries, where each dictionary contains the title and description of an unavailable ingredient.

        Note:
        - The function uses BeautifulSoup to parse the HTML content of the current webpage.
        - It finds the <tbody> element in the HTML and then iterates over all <h3> elements within it.
        - If a <h3> element is a child of an <a> element, it is skipped (indicating that it is not an unavailable ingredient).
        - The title and description of each unavailable ingredient are extracted and added to a list of dictionaries.
        """
        data = []
        soup = BeautifulSoup(driver.page_source, "html.parser")
        tbody = soup.find("tbody")
        for line in tbody.find_all("h3"):
            if line.parent.find("a"):
                continue
            title = line.text
            description = line.next_sibling.text
            data.append({"title": title, "description": description})
        return data

    def get_details(self, soup):
        """
        Extracts detailed information about an ingredient from a BeautifulSoup object.

        Parameters:
        soup (BeautifulSoup): A BeautifulSoup object containing the HTML content of the ingredient page.

        Returns:
        dict: A dictionary containing the extracted details. The dictionary will have the following keys:
            - 'rating': The rating of the ingredient.
            - 'category': The category of the ingredient.
            - 'benefits': The benefits of the ingredient.
            - 'description': A list of paragraphs describing the ingredient.
            - 'eferences': A list of references for the ingredient.
            - 'glance': A list of points summarizing the ingredient.

        Note:
        - This method assumes that the HTML structure of the ingredient page is consistent with the structure used in the provided code.
        """
        data = {}
        large7 = soup.find_all(class_="large7")
        for large in large7:
            t = large.parent.text
            if "Rating" in t:
                data["rating"] = t.replace("Rating:", "")
            if "Categories" in t:
                data["category"] = t.replace("Categories:", "")
            if "Benefits" in t:
                data["benefits"] = t.replace("Benefits:", "")
        h2 = soup.find_all("h2")
        for line in h2:
            if "Description" in line.text:
                dlist = []
                for p in line.parent.next_sibling.find_all("p"):
                    dlist.append(p.text)
                data["description"] = dlist
            if "References" in line.text:
                rlist = []

                for p in line.parent.next_sibling.find_all("div"):
                    rlist.append(p.text)
                data["references"] = rlist

            if "Glance" in line.text:
                glist = []
                for p in line.next_sibling.find_all("li"):
                    glist.append(p.text)

                data["glance"] = glist

        return data


if __name__ == "__main__":
    p = Paulaschoice()
    p.Runner()
