#USERS

from random import randint
from random import choice
from faker import Faker
fake = Faker()
def phone():
    num = f'{fake.msisdn()[3:]}'
    all_gucci = False
    while  not all_gucci:
        if num[0] == '1' or num[0] == '0' or num[3] == '1' or num[3] == '0' or num[3:6] == '911':
            num = f'{fake.msisdn()[3:]}'
        else:
            all_gucci = True
    return num
user_list = []
def generate_users(num_users):
    
    
    for i in range(0, num_users):
        fname = fake.first_name()
        lname = fake.last_name()
        email_bridge = choice(['', choice(['-','_',str(randint(0,9))])])
        email_affectation = choice(['', choice(['','',str(randint(0,9)),'fan',choice(['68', '419', '41968'])])])
        domain = choice(['com','net',choice(['edu','org','gov'])])
        person = {
            "id"            : i + 1,
            "email"         : fname.lower() + f"{email_bridge}{lname.lower()}{email_affectation}{randint(0,100)}@example.{domain}",
            "first_name"    : fname,
            "last_name"     : lname,
            "user_password" : fake.password(),
            "phone"         : phone(),
        }       

        user_list.append(person)
    print(user_list)
generate_users(10)
def print_it():
    string = ""
    values = f"(email, first_name, last_name, user_password, phone)"
    for i in range(len(user_list)):
        string = string + f"INSERT INTO users {values} VALUES('{user_list[i]['email']}', '{user_list[i]['first_name']}', '{user_list[i]['last_name']}', '{user_list[i]['user_password']}', '{user_list[i]['phone']}');\n"
    print(string)
print_it()




#PRODUCTS
from random import randint
from random import choice
from faker import Faker
from faker_food import FoodProvider
fake = Faker()
fake.add_provider(FoodProvider)
product_ids = set()
def generate_product_ids(total_items):
    for i in range(1, total_items):
        upc = ""
        for j in range(1, 12+1):
            upc += str(randint(0, 10))
        product_ids.add(upc)
    print(product_ids)
generate_product_ids(3)
product_ids = list(product_ids)
print(len(product_ids), product_ids)
product_list = []
def generate_products():
    num_products = len(product_ids)
    
    for i in range(0, num_products):
        product = {
            "upc"              : "",
            "prod_name"        : "",
            "brand"            : "",
            "prod_description" : "",
            "category"         : "",
            "price_per_unit"   : "",
            "image_url"        : "",
            "available_stock"  : "",
            "reserved_stock"   : "",
            "shipped_stock"    : "",
        }
        product["upc"]              = product_ids[i]
        product["prod_name"]        = fake.dish()
        product["prod_description"] = fake.dish_description()
        product["brand"]            = fake.vegetable() + " Foods, Inc"
        product["category"]         = choice([fake.ethnic_category(), fake.ingredient()])
        product["price_per_unit"]   = randint(0, 15) + 0.99
        product["image_url"]        = "https://picsum.photos/100/"
        product["available_stock"]  = randint(0, 200)
        product["reserved_stock"]   = randint(0, 30)
        product["shipped_stock"]    = randint(0, 60)         

        product_list.append(product)
    print(product_list)
generate_products()
def print_it():
    print("um")
    string = ""
    values = f"(upc, prod_name, prod_description, brand, category, price_per_unit, image_url, available_stock, reserved_stock, shipped_stock)"
    for i in range(len(product_list)):
        string = string + f"INSERT INTO products VALUES('{product_list[i]['upc']}', '{product_list[i]['prod_name']}', '{product_list[i]['prod_description']}', '{product_list[i]['brand']}', '{product_list[i]['category']}', {product_list[i]['price_per_unit']}, '{product_list[i]['image_url']}', {product_list[i]['available_stock']}, {product_list[i]['reserved_stock']}, {product_list[i]['shipped_stock']},);\n"
        # string = string + f"INSERT INTO products {values} VALUES('{product_list[i]['upc']}', '{product_list[i]['prod_name']}', '{product_list[i]['prod_description']}', '{product_list[i]['brand']}', '{product_list[i]['category']}', {product_list[i]['price_per_unit']}, '{product_list[i]['image_url']}', {product_list[i]['available_stock']}, {product_list[i]['reserved_stock']}, {product_list[i]['shipped_stock']},);\n"
    print(string)
print_it()




#ORDERS
from random import randint, choice, choices
import string
from faker import Faker
from datetime import *
fake = Faker()
print(fake.date())
orders = []
today = date.today()
today = str(today).split("-")
print(today)
next_order_year  = int(today[0])
next_order_month = int(today[1])
next_order_day   = int(today[2])
order_times = []
today = datetime.today()

num_orders = 10
def rand_days():
    return choice([0, randint(0,4)])

for i in range(num_orders):
    ordered = fake.date_between_dates(date_start=datetime(2018,1,1), date_end=datetime(2022,9,16))
    to_ship_time = (ordered + timedelta(days=rand_days()))
    shipped = choices(['NULL', to_ship_time], [100, 99])[0]
    if shipped != 'NULL':
        delivered = choices(['NULL' , shipped + timedelta(days=rand_days())], [200, 98])[0]
    else:
        delivered = 'NULL'
    order_times.append({'ordered': str(ordered), 'shipped': str(shipped), 'delivered': str(delivered)})
    # print('ordered: ', ordered, 'shipped: ', shipped, 'delivered: ', delivered, end = '\n')
print(order_times)
# def date_ordered():
#     order_date = fake.date_between_dates(
#         date_start=datetime.date(
#             next_order_year, 
#             next_order_month, 
#             next_order_day
#         ), 
#         date_end=datetime.date(
#             next_order_year + choice(0, ), 
#             next_order_month, 
#             next_order_day)).year
#         )
def order_status(order_time):
    for date in order_times:
        if order_time['delivered'] != 'NULL':
            return 'DELIVERED'
        elif order_time['shipped'] != 'NULL':
            return 'IN TRANSIT'
        else:
            return 'ORDERED'
def generate_orders(num_orders):
    total_orders = num_orders
    i = 0
    while i < total_orders:
        
        order = {
            "order_id"        : i + 1,
            "user_id"         : i + 1,
            "address_id"      : i + 1,
            "price"           : round(randint(0, 300) + 0.99 * randint(1, 30), 2),
            "credit_card_id"  : i + 1,
            "date_ordered"    : order_times[i]['ordered'],
            "date_shipped"    : order_times[i]['shipped'], #is shipped? if so ship date function
            "date_delivered"  : order_times[i]['delivered'], #is order? if so del date function
            "order_status"    : order_status(order_times[i]),
        }       

        orders.append(order)
        i += 1
    print(orders)
generate_orders(10)
generate_orders(10)
def print_it():
    string = ""
    values = f"(user_id, address_id, price, credit_card_id, date_ordered, date_shipped, date_delivered, order_status)"
    for i in range(len(orders)):
        shipped_val = f"'{orders[i]['date_shipped']}'" 
        delivered_val = f"'{orders[i]['date_delivered']}'" 
        user_id = orders[i]['user_id'] if 'user_id' in orders[i] else i + 1
        # string = string + f"INSERT INTO orders VALUES({orders[i]['order_id']}, {user_id}, {orders[i]['address_id']}, {orders[i]['price']}, {orders[i]['credit_card_id']}, '{orders[i]['date_ordered']}', {'NULL' if orders[i]['date_shipped'] == 'NULL' else f'{shipped_val}'}, {'NULL' if orders[i]['date_delivered'] == 'NULL' else f'{delivered_val}'}, '{orders[i]['order_status']}');\n"
        string = string + f"INSERT INTO orders {values} VALUES({user_id}, {orders[i]['address_id']}, {orders[i]['price']}, {orders[i]['credit_card_id']}, '{orders[i]['date_ordered']}', {'NULL' if orders[i]['date_shipped'] == 'NULL' else f'{shipped_val}'}, {'NULL' if orders[i]['date_delivered'] == 'NULL' else f'{delivered_val}'}, '{orders[i]['order_status']}');\n"
                                                                                                                                                                                             # 'NULL' if orders[i]['date_delivered'] == 'NULL' else f'{delivered_val}'
    print(string)
print_it()



#
