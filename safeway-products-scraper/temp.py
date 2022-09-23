import pandas as pd
import re

# df = pd.read_csv("safewayData.csv", sep=",")
# print(df.head())
# print(df["Category"])


def get_product_code(img_url):
    pattern = re.compile(r'ABS/([0-9]*)?')
    matches = re.findall(pattern, img_url)
    return matches[0]

print(get_product_code("images.albertsons-media.com/is/image/ABS/136010121?$ecom-product-card-desktop-jpg$&defaultImage=Not_Available"))

# df = pd.read_csv("safewayData.csv")
# print(len(df))
# df.drop_duplicates(inplace=True)
# print(len(df))
# print(df.head())

