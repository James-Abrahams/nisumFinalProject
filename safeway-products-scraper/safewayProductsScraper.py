from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import re
import sys
import time
import os
import multiprocessing as mp


class SafewayProductsScraper:
    def __init__(self):
        self.items = self.read_items("items.txt") # txt file containing products to scrape on Safeway's website, line-by-line
        # group items in self.items
        items_per_group = mp.cpu_count()
        self.items = [self.items[n:n + items_per_group] for n in range(0, len(self.items), items_per_group)]
        self.out_fn = "safewayData.csv" # output data filename
        self.cols = ["ProdName", "Brand", "PricePerUnit", "Category", "Rating", "ProdDescription", "ProdCode", "ImageURL"]
        os.environ['WDM_LOG_LEVEL'] = '0' # turn off webdriver logging
        self.options = Options()
        self.options.headless = True # run in headless mode
        self.options.add_argument('--window-size=1920,1080')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"')

        start_time = time.time()

        # for each group of items, read in data from csv data file
        for items in self.items:
            self.df = self.create_dataframe() # read in collected data into df, creates new df if not found
            p = mp.Pool(items_per_group)
            results = p.map(self.scrape, items)
            df_list = [item for sublist in results for item in sublist]
            temp_df = pd.DataFrame(columns=self.cols, data=df_list)
            self.df = pd.concat([self.df, temp_df])

            # remove duplicate rows in df
            self.df.drop_duplicates(keep='first',
                                    subset="ProdName",
                                    inplace=True)
            self.to_csv()
        end_time = time.time()
        print(f"Time to scrape product details: {end_time - start_time}")

    # read items.txt line-by-line
    # return list of items to scrape
    def read_items(self, fn):
        items = []
        try:
            with open(fn, 'r') as f:
                items = f.read().splitlines()
                items = [x for x in items if x]
        except FileNotFoundError:
            print(f"{fn} not found. Creating {fn} ...")
            _ = open(fn, 'x')
            print("Program terminated")
            sys.exit()
        if not items:
            print(f"No items specified in {fn}. Please add items line-by-line.")
            print("Program terminated")
            sys.exit()
        return items

    def create_dataframe(self):
        try:
            df = pd.read_csv(self.out_fn)
        except FileNotFoundError: # no data found, create empty dataframe
            print(f"{self.out_fn} not found, creating empty dataframe")
            df = pd.DataFrame(columns=self.cols) # create empty dataframe with defined cols
        else:
            print("Existing data file found, data read into dataframe")
        return df

    # returns a list of lists of values
    def scrape(self, item):
        print(f"Scraping product data for: {item}")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)
        driver.get(f"https://safeway.com/shop/search-results.html?q={item}") # search item on safeway website

        change_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div/div/div/div[3]/div[2]/div[7]/div/div/div[1]/div[1]/button")
        action = ActionChains(driver)
        action.move_to_element_with_offset(change_button, 400, 600).click().perform()
        # driver.implicitly_wait(3)
        # driver.get(f"https://safeway.com/shop/search-results.html?q={item}") # refresh page to get rid of pop-up

        time.sleep(3)

        # # click load more 3 times
        # for _ in range(3):
        #     time.sleep(3)
        #     # click load more to display even more products
        #     load_more_button = driver.find_element(By.XPATH,
        #         '/html/body/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[4]/div[2]/search-grid/div[4]/button')
        #     actions = ActionChains(driver)
        #     actions.move_to_element(load_more_button)
        #     try:
        #         load_more_button.click()
        #     except NoSuchElementException:
        #         break

        # product name
        name_elements = driver.find_elements(By.CLASS_NAME, 'product-title__name')
        names = [e.text.strip() for e in name_elements]
        if not name_elements:
            print(f"No results found for: {item}")
            return []

        # price per unit
        price_elements = driver.find_elements(By.CLASS_NAME, 'product-price__discounted-price')
        prices = [e.text.replace('Your Price', '')
                        .replace('each', '')
                        .replace('$', '')
                        .replace('\n', '') for e in price_elements]

        # price per unit amount (weight/vol)
        # ppu_elements = driver.find_elements(By.CLASS_NAME, 'product-title__qty')
        # ppus = [e.text.replace('($', '').replace(')', '') for e in ppu_elements]

        # product image url
        img_elements = driver.find_elements(By.CLASS_NAME, 'product-card-container__product-image')
        img_urls = [e.get_attribute("data-src")[2:] for e in img_elements]

        # product category
        try:
            category = driver.find_element(By.XPATH,
                '/html/body/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div[1]/div[1]/search-facets/div/div[7]/div[2]/div[2]/div[2]/department-filter/div/div[1]/div/span').text
        except NoSuchElementException:
            category = 'Other'
        else:
            category = category.strip()
            pattern = re.compile(r'([\s\S]*) \(')
            matches = re.findall(pattern, category)
            category = matches[0]

        # product brand
        brands_list = self.get_brands_list(item, driver)
        brands = [self.get_product_brand(name, brands_list) for name in names]

        # product rating
        ratings = self.get_product_ratings(driver)

        driver.quit()

        current_item_data = list(zip(
                            names,
                            brands,
                            prices,
                            [category] * len(names),
                            ratings,
                            ["-"]*len(names), # dash for product description column
                            [self.get_product_code(url) for url in img_urls], # extract product code from img urls
                            img_urls))

        temp_df = pd.DataFrame(data=current_item_data,
                               columns=self.cols)
        temp_list = temp_df.values.tolist()
        return temp_list

    def get_product_code(self, img_url):
        pattern = re.compile(r'ABS/([0-9]*)\?')
        matches = re.findall(pattern, img_url)
        return matches[0]

    # return list of brands of item (e.g. milk, eggs, etc)
    def get_brands_list(self, item, driver):
        brands = []
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        brand_list = soup.find("div", {"id": "brand"})
        result = brand_list.find_all('span', attrs={'class': "facet__label__text"})
        for x in result:
            brands.append(x.text.strip())
        return brands

    # return product's brand
    def get_product_brand(self, prod_name, brands_list):
        name_words = prod_name.split() # store words in prod_name into list
        for brand in brands_list:
            brand_words = brand.split() # store words in brand name into list

            # compare first word in product name to first word in brand name
            name_first_word = ''.join(filter(str.isalnum, name_words[0])).lower()
            brand_first_word = ''.join(filter(str.isalnum, brand_words[0])).lower()

            if name_first_word == brand_first_word:
                return brand

        # no brand matches, return "-"
        return name_words[0]

    def get_product_ratings(self, driver):
        html = driver.page_source
        soup = BeautifulSoup(html, 'lxml')
        rows = soup.find_all('div', attrs={'class': "product-card-container product-card-container--with-out-ar"})
        ratings = []
        for row in rows:
            rating_element = row.find('div', attrs={'class': "product-card-container__star-icon"})
            if not rating_element:
                rating = "5.0"  # maybe random
            else:
                rating = rating_element.text.strip()
            ratings.append(rating)
        return ratings

    # writes dataframe to csv file
    def to_csv(self):
        self.df.to_csv(self.out_fn,
                       mode='w+', # overwrite existing data file
                       header=True,
                       index=False,
                       sep=",")
        print(f"{len(self.df)} rows saved in {self.out_fn}\n")