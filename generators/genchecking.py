from random import randint, choice, choices
from faker import Faker
from faker_food import FoodProvider
from math import floor, sqrt
from datetime import *
import string
fake = Faker()

num_users = 20
num_products_more_or_less = 15
today = datetime.today()
#region nest it all
#region USERS
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
    user_list.clear()
    for i in range(0, num_users):
        fname = fake.first_name()
        mname = fake.first_name()
        lname = fake.last_name()
        email_bridge = choice(['', choice(['-','_',str(randint(0,9))])])
        email_affectation = choice(['', choice(['','',str(randint(0,9)),'fan',choice(['68', '419', '41968'])])])
        domain = choice(['com','net',choice(['edu','org','gov'])])
        person = {
            "user_id"       : i + 1,
            "email"         : fname.lower() + f"{email_bridge}{lname.lower()}{email_affectation}{randint(0,100)}@example.{domain}",
            "first_name"    : fname,
            "middle_name"   : mname,
            "last_name"     : lname,
            "user_password" : fake.password(), #change to hashed password_key
            "phone"         : phone(),
        }       

        user_list.append(person)

def print_users():
    string = ""
    values = f"(email, first_name, last_name, user_password, phone)"
    for i in range(len(user_list)):
        string = string + f"INSERT INTO users {values} VALUES ('{user_list[i]['email']}', '{user_list[i]['first_name']}', '{user_list[i]['last_name']}', '{user_list[i]['user_password']}', '{user_list[i]['phone']}');\n"
    print(string)

generate_users(num_users)
print_users()
# print(user_list)
# print(len(user_list))
# endregion


# region PRODUCTS
fake.add_provider(FoodProvider)
product_ids = set()

def generate_product_ids(total_items):
    for i in range(1, total_items):
        upc = ""
        for j in range(1, 12+1):
            upc += str(randint(0, 10))
        product_ids.add(upc)
    print(product_ids)

generate_product_ids(num_products_more_or_less)


product_ids = list(product_ids)
print(len(product_ids), product_ids)
product_list = []

def generate_products():
    #CHANGE TO SCRAPER
    product_list.clear()
    num_products = len(product_ids)
    for i in range(0, num_products):
        product = {
            "upc"              : product_ids[i],
            "prod_name"        : fake.dish(),
            "brand"            : fake.dish_description(),
            "prod_description" : fake.vegetable() + " Foods, Inc",
            "category"         : choice([fake.ethnic_category(), fake.ingredient()]),
            "price_per_unit"   : randint(0, 15) + 0.99,
            "image_url"        : "https://picsum.photos/100/",
            "available_stock"  : randint(0, 200),
            "reserved_stock"   : randint(0, 30), # define by carts
            "shipped_stock"    : randint(0, 60), # define by orders/ order items
        }

        product_list.append(product)



def print_products():
    print("um")
    string = ""
    values = f"(upc, prod_name, prod_description, brand, category, price_per_unit, image_url, available_stock, reserved_stock, shipped_stock)"
    for i in range(len(product_list)):
        string = string + f"INSERT INTO products VALUES('{product_list[i]['upc']}', '{product_list[i]['prod_name']}', '{product_list[i]['prod_description']}', '{product_list[i]['brand']}', '{product_list[i]['category']}', {product_list[i]['price_per_unit']}, '{product_list[i]['image_url']}', {product_list[i]['available_stock']}, {product_list[i]['reserved_stock']}, {product_list[i]['shipped_stock']},);\n"
    print(string)
generate_products()
print_products()
# endregion


# region ORDERS
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

print(order_times)

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
            "order_status"    : order_status(order_times[i]),
        }       

        orders.append(order)
        i += 1
    print(orders)

# generate_orders(10)

def print_orders():
    string = ""
    values = f"(user_id, address_id, price, credit_card_id, date_ordered, date_shipped, date_delivered, order_status)"
    for i in range(len(orders)):
        shipped_val = f"'{orders[i]['date_shipped']}'" 
        delivered_val = f"'{orders[i]['date_delivered']}'" 
        user_id = orders[i]['user_id'] if 'user_id' in orders[i] else i + 1
        string = string + f"INSERT INTO orders {values} VALUES({user_id}, {orders[i]['address_id']}, {orders[i]['price']}, {orders[i]['credit_card_id']}, '{orders[i]['date_ordered']}', {'NULL' if orders[i]['date_shipped'] == 'NULL' else f'{shipped_val}'}, {'NULL' if orders[i]['date_delivered'] == 'NULL' else f'{delivered_val}'}, '{orders[i]['order_status']}');\n"
    print(string)
# endregion

#endregion

orders = []

x_num_orders = 10
def x_rand_days():
    return choice([0, randint(0,4)])

for i in range(x_num_orders):
    ordered = fake.date_between_dates(date_start=datetime(2018,1,1), date_end=datetime(2022,9,16))
    to_ship_time = (ordered + timedelta(days=rand_days()))
    shipped = choices(['NULL', to_ship_time], [100, 99])[0]
    if shipped != 'NULL':
        delivered = choices(['NULL' , shipped + timedelta(days=rand_days())], [200, 98])[0]
    else:
        delivered = 'NULL'
    order_times.append({'ordered': str(ordered), 'shipped': str(shipped), 'delivered': str(delivered)})
print(order_times)







def generate_order_for_user(user, date_ordered, date_shipped):
    i = 0
    order = {
        # "order_id"        : i + 1,
        # "user_id"         : i + 1,
        # "address_id"      : i + 1,
        # "price"           : 0,
        # "credit_card_id"  : i + 1,
        'preliminary_id'  : i + 1, 
        # "date_ordered"    : order_times[i]['ordered'],
        # "date_shipped"    : order_times[i]['shipped'], #is shipped? if so ship date function
        # "order_status"    : order_status(order_times[i]),
    }      
    id = order['preliminary_id']
    price = generate_order_items_per_order(order[id])
    
    orders.append(order)
    
    
    i += 1

def generate_orders():
    # orders.clear()
    total = 0
    i = 1
    j = 1
    while i < 100:
        did_all_orders = False
        while not did_all_orders:
            d100 = randint(1,100)
            date_ordered = date_ordered(i), 
            date_shipped = date_shipped(i),
            order_status = order_status()
            generate_order_for_user(i, ) #change to user
            
            
            if d100 > 91:
                did_all_orders = True
                i += 1
                print(f"total for person {i}: {j} \n")
                j = 1
            else:
                j += 1
            total += 1

generate_orders()