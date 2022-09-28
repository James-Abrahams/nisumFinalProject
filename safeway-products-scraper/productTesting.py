from random import randint

import pandas as pd

df = pd.read_csv('safewayData.csv',index_col=False)
codes = list(df['ProdCode'])
list = []

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
    list.append(product)

for x in list:
    print("UPC: ", x["upc"])
    print("prod_name: ", x["prod_name"])
    print("brand: ", x["brand"])
    print("prod_description: ", x["prod_description"])
    print("category: ", x["category"])
    print("pricer_per_unit: ", x["price_per_unit"])
    print("image_url: ", x["image_url"])
    print("--------------------------------------------------------------------------------------------------------")