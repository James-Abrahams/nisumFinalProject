from random import randint
from random import choice
import pandas as pd

df = pd.read_csv('../safeway-products-scraper/safewayData.csv',index_col=False)

product_list = []
codes = list(df['ProdCode'])

for code in codes:
    row = df.loc[df['ProdCode'] == code]
    product = {
        "upc": row.iloc[0]['ProdCode'],
        "prod_name": row.iloc[0]['ProdName'],
        "brand": row.iloc[0]['Brand'],
        "prod_description": row.iloc[0]['ProdDescription'],
        "category": row.iloc[0]['Category'],
        "price_per_unit": row.iloc[0]['PricePerUnit'],
        "image_url": row.iloc[0]['ImageURL'],
        "available_stock": randint(0, 200),
        "reserved_stock": randint(0, 30),
        "shipped_stock": randint(0, 60),
    }
    product_list.append(product)

print(product_list)


def print_it():
    print("um")
    string = ""
    values = f"(upc, prod_name, prod_description, brand, category, price_per_unit, image_url, available_stock, reserved_stock, shipped_stock)"
    for i in range(len(product_list)):
        string = string + f"INSERT INTO products VALUES('{product_list[i]['upc']}', '{product_list[i]['prod_name']}', '{product_list[i]['prod_description']}', '{product_list[i]['brand']}', '{product_list[i]['category']}', {product_list[i]['price_per_unit']}, '{product_list[i]['image_url']}', {product_list[i]['available_stock']}, {product_list[i]['reserved_stock']}, {product_list[i]['shipped_stock']},);\n"
        # string = string + f"INSERT INTO products {values} VALUES('{product_list[i]['upc']}', '{product_list[i]['prod_name']}', '{product_list[i]['prod_description']}', '{product_list[i]['brand']}', '{product_list[i]['category']}', {product_list[i]['price_per_unit']}, '{product_list[i]['image_url']}', {product_list[i]['available_stock']}, {product_list[i]['reserved_stock']}, {product_list[i]['shipped_stock']},);\n"
    print(string)
print_it()