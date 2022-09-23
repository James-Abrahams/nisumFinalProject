import pandas as pd
import requests
from bs4 import BeautifulSoup
from lxml import etree


class SafewayDescriptionsScraper:
    def __init__(self):
        self.data_fn = "safewayData.csv"
        self.df = pd.read_csv(self.data_fn)

        self.scrape()

    def get_description(self, prod_code):
        url= f"https://www.safeway.com/shop/product-details.{prod_code}.html"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        dom = etree.HTML(str(soup))
        dx = dom.xpath('/html/body/div[2]/div/div/div[2]/div/div/div/div/div/div/div/div[2]/div[3]/div/div[3]/div[2]/div[1]/p[2]')[0].text.strip()
        return dx

    def scrape(self):
        # iterate through dataframe rows, replace '-' in ProdDescription with its description
        errors = 0
        for ind, row in self.df.iterrows():
            # if count >= 10: break
            if row['ProdDescription'] == '-':
                try:
                    self.df.loc[ind, 'ProdDescription'] = self.get_description(self.df.loc[ind, 'ProdCode'])
                except IndexError:
                    errors += 1
                    print("Index Error at product code", self.df.loc[ind, 'ProdCode'])

        # write updated df to csv
        self.df.to_csv(self.data_fn,
                  mode='w+',  # overwrite existing data file
                  header=True,
                  index=False,
                  sep=",")

        print(f"Descriptions written to {self.data_fn}.\nFailed to obtain descriptions for {errors} items")



