from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re


class SafewayProductsScraper:
    def __init__(self):
        self.out_fn = "safewayData.csv" # output data filename
        self.items = ["milk", "chocolate", "juice", "cookies"] # list of items to scrape
        self.cols = ["ProdName", "PricePerUnit", "ProdDescription", "ProdCode", "Category", "ImageURL"]
        self.df = self.create_dataframe() # read in collected data into df, creates new df if not found
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

        self.scrape()
        self.to_csv()
        self.driver.quit()

    def create_dataframe(self):
        try:
            df = pd.read_csv(self.out_fn)
        except FileNotFoundError: # no data found, create empty dataframe
            print(f"{self.out_fn} not found, creating empty dataframe")
            df = pd.DataFrame(columns=self.cols) # create empty dataframe with defined cols
        else:
            print("Existing data file found, data read into dataframe")
        return df

    def scrape(self):
        for i, item in enumerate(self.items):
            self.driver.get(f"https://safeway.com/shop/search-results.html?q={item}") # search item on safeway website

            if i == 0: self.driver.get(f"https://safeway.com/shop/search-results.html?q={item}") # refresh page to get rid of pop-up

            # select each brand name individually
            # /html/body/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div[1]/div[1]/search-facets/div/div[7]/div[2]/div[3]/div[2]/div/div[1]/div[1]/div/input
            # /html/body/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div[1]/div[1]/search-facets/div/div[7]/div[2]/div[3]/div[2]/div/div[1]/div[2]/div/input
            time.sleep(2)
            matches = self.driver.find_elements(By.CLASS_NAME, "facet__label__text")
            _ = [print(x.text) for x in matches]

            # click load more 3 times
            for _ in range(3):
                time.sleep(2)
                # click load more to display even more products
                load_more_button = self.driver.find_element(By.XPATH,
                    '/html/body/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div[2]/div[4]/div[2]/search-grid/div[4]/button')
                actions = ActionChains(self.driver)
                actions.move_to_element(load_more_button)
                try:
                    load_more_button.click()
                except NoSuchElementException:
                    break

            # product name
            name_elements = self.driver.find_elements(By.CLASS_NAME, 'product-title__name')
            names = [e.text for e in name_elements]

            # price per unit
            price_elements = self.driver.find_elements(By.CLASS_NAME, 'product-price__discounted-price')
            prices = [e.text.replace('Your Price', '')
                            .replace('each', '')
                            .replace('$', '')
                            .replace('\n', '') for e in price_elements]

            # price per unit amount (weight/vol)
            # ppu_elements = self.driver.find_elements(By.CLASS_NAME, 'product-title__qty')
            # ppus = [e.text.replace('($', '').replace(')', '') for e in ppu_elements]

            # product image url
            img_elements = self.driver.find_elements(By.CLASS_NAME, 'product-card-container__product-image')
            img_urls = [e.get_attribute("data-src")[2:] for e in img_elements]

            # product category
            category = self.driver.find_element(By.XPATH,
                '/html/body/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div[1]/div[1]/search-facets/div/div[7]/div[2]/div[2]/div[2]/department-filter/div/div[1]/div/span').text
            category = category.strip()
            pattern = re.compile(r'([\s\S]*) \(')
            matches = re.findall(pattern, category)
            category = matches[0]

            current_item_data = list(zip(
                                names,
                                prices,
                                ["-"]*len(names), # dash for product description column
                                [self.get_product_code(url) for url in img_urls], # extract product code from img urls
                                [category]*len(names),
                                img_urls))

            temp_df = pd.DataFrame(data=current_item_data,
                                   columns=self.cols)
            self.df = pd.concat([self.df, temp_df])

        # remove duplicate rows in df
        self.df.drop_duplicates(keep='first',
                                subset="ProdName",
                                inplace=True)

    def get_product_code(self, img_url):
        pattern = re.compile(r'ABS/([0-9]*)\?')
        matches = re.findall(pattern, img_url)
        return matches[0]

    # writes dataframe to csv file
    def to_csv(self):
        self.df.to_csv(self.out_fn,
                       mode='w+', # overwrite existing data file
                       header=True,
                       index=False,
                       sep=",")
        print(f"Data saved in {self.out_fn}")