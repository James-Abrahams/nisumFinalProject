import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree


class SafewayDescriptionsScraper:
    def __init__(self):
        self.out_fn = "safewayData.csv"
        self.df = pd.read_csv(self.out_fn)
        self.errors = 0

        self.scrape()
        self.to_csv()

    def get_description(self, prod_code):
        url= f"https://www.safeway.com/shop/product-details.{prod_code}.html"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        dom = etree.HTML(str(soup))
        dx_top = dom.xpath('/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[3]/div/div[3]/div[2]/div[1]/p[1]')[0].text.strip()
        dx_bot = dom.xpath('/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[3]/div/div[3]/div[2]/div[1]/p[2]')[0].text.strip()
        return dx_top + 2*'\n' + dx_bot

    def scrape(self):
        # iterate through dataframe rows, replace '-' in ProdDescription with its description
        for ind, row in self.df.iterrows():
            # save to csv
            if row['ProdDescription'] == '-':
                try:
                    self.df.loc[ind, 'ProdDescription'] = self.get_description(self.df.loc[ind, 'ProdCode'])
                except IndexError:
                    self.errors += 1
                    print("Index Error at product code", self.df.loc[ind, 'ProdCode'])

        # write updated df to csv
    def to_csv(self):
        self.df.to_csv(self.out_fn,
                       mode='w+',  # overwrite existing data file
                       header=True,
                       index=False,
                       sep=",")

        print(f"Descriptions written to {self.out_fn}.\nFailed to obtain descriptions for {self.errors}/{len(self.df)} items")



