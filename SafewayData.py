from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import numpy as np
import pandas as pd
from openpyxl import load_workbook

import sys
import csv
import os
import time
import urllib
import datetime
# import urllib2
from bs4 import BeautifulSoup
from pprint import pprint
import requests
from datetime import datetime, timedelta

driver = webdriver.Chrome(r"/Users/j/Desktop/work/ascend/data engineers/chromedriver")


products = ['milk', 'eggs', 'bread']


for query in products:

    url = 'https://www.safeway.com/shop/search-results.html?q=' + str(query.strip())

    print(url)

    delay = 2
    driver.get(url)
    time.sleep(delay)

    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'asidediv col-12 col-sm-12 col-md-12 col-lg-9 col-xl-9')))
        print('Ready')
    except TimeoutException:
        print("Loading took too much time!")

    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')


    rows = soup.find_all('div', attrs={'class': "product-card-container product-card-container--with-out-ar"})

    data = []

    for row in rows:
        var = []
        try:
            temp = row.find('div', attrs={'class': "product-title__text"})
            # print("Title: ", temp.text.strip())
            var.append(temp.text.strip())
        except:
            var.append(np.NaN)

        try:
            temp = row.find('div', attrs={'class': "product-card-container__star-icon"})
            # print("Rating: ", temp.text.strip())
            var.append(temp.text.strip())
        except:
            var.append(np.NaN)

        try:
            temp = row.find('div', attrs={'class': "product-price"})
            # print("Price: ",temp.text.strip())
            var.append(temp.text.strip())
        except:
            var.append(np.NaN)

        data.append(var)


    df = pd.DataFrame(data,  columns =['Title', 'Rating', 'Price'])
    df.set_index(['Title'], inplace=True)
    df.to_csv('{}.csv'.format(query))

driver.quit()
