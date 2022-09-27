import pandas as pd
import requests
import multiprocessing as mp
import time
from bs4 import BeautifulSoup
from lxml import etree


class SafewayDescriptionsScraper:
    def __init__(self):
        self.out_fn = "safewayData.csv"
        self.df = pd.read_csv(self.out_fn)
        self.cols = list(self.df.columns.values)

        self.df_list = self.df.values.tolist()
        self.prod_code_index = self.df.columns.get_loc("ProdCode")
        self.prod_dx_index = self.df.columns.get_loc("ProdDescription")

        start_time = time.time()
        p = mp.Pool(mp.cpu_count())
        results = p.map(self.get_description, self.df_list)
        end_time = time.time()
        print(f"Time to scrape product descriptions: {end_time - start_time}")

        self.df = pd.DataFrame(columns=self.cols, data=results)

        self.to_csv()

    def get_description(self, row):

        # if row corresponding to prod_code already has a description, return row as is
        if row[self.prod_dx_index] != '-':
            return row

        # else grab description from safeway's website using requests and BeautifulSoup
        prod_code = row[self.prod_code_index]
        url = f"https://www.safeway.com/shop/product-details.{prod_code}.html"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        dom = etree.HTML(str(soup))
        try:
            dx_top = dom.xpath('/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[3]/div/div[3]/div[2]/div[1]/p[1]')[0].text.strip()
            dx_bot = dom.xpath('/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[3]/div/div[3]/div[2]/div[1]/p[2]')[0].text.strip()
        except IndexError:
            print("Could not find description for:", prod_code)
            dx = "-"
        else:
            dx = dx_top + '\n' + dx_bot

        # replace '-' in ProdDescription with its description if found; set as '-' if not found
        row[self.prod_dx_index] = dx
        return row

    # write updated df to csv
    def to_csv(self):
        self.df.to_csv(self.out_fn,
                       mode='w+',  # overwrite existing data file
                       header=True,
                       index=False,
                       sep=",")

        print(f"Descriptions written to {self.out_fn}")



