from random import randint, choice, choices
from faker import Faker
from faker_food import FoodProvider
import pandas as pd
from math import floor, sqrt
from datetime import datetime, timedelta, date
import string
fake = Faker()

num_users = 5
num_products_more_or_less = 15
today = date.today()
print("today: ", today)

orders = []
carts = []
order_items = []
products = []
user_list = []
cards = []


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

# region CREDIT



def cardholder_name(first_name = fake.first_name(), last_name = fake.last_name(), middle_name = None): 
    fname = first_name
    if middle_name == None:
        mname = choice(['' , '', ' ' + ''.join(choices([choice(list(string.ascii_letters.upper())), fake.first_name()], [4, 1])[0])])
    else:
        mname = choice(['' , '', ' ' + ''.join(choices([middle_name[0], middle_name], [4, 1])[0])])
    lname = last_name
    return f"{fname}{mname} {lname}"

def generate_cards_for_user(num_cards, user):
    i = 0
    while i < num_cards:
        random_int = randint(1,100)
        exp = fake.credit_card_expire().split("/")
        card = {
            "card_id"               : i + 1,
            "user_id"               : user['user_id'], #CHANGEME make this depend on shipping and billing results + chance of extra
            "cardholder_name"       : "", #later tie this to person name with logic, chance of other esp if extra
            "last_four_card_number" : str(fake.credit_card_number())[-4:],
            "expiration_year"       : exp[1],
            "expiration_month"      : exp[0]
        } 
        if random_int < 91:
            card['cardholder_name'] = cardholder_name(user['first_name'], user['last_name'], user['middle_name'])
        elif random_int < 97:
            card['cardholder_name'] = cardholder_name(last_name = user['last_name'])
        else:
            card['cardholder_name'] = cardholder_name()
        cards.append(card)
        i += 1

def generate_credit_cards(num_users):
    cards.clear()
    i = 0
    while i < num_users:
        user = user_list[i]
        num_cards_for_user = choice([1,1,1,1,2,3])
        # num_cards_for_user = 10
        generate_cards_for_user(num_cards_for_user, user)
        i += 1

def print_credit_cards():
    string = ""
    values = f"(user_id, cardholder_name, last_four_card_number, expiration_year, expiration_month)"
    for i in range(len(cards)):
        user_id = cards[i]['user_id'] if 'user_id' in cards[i] else i + 1
        string = string + f"INSERT INTO credit_cards {values} VALUES ({user_id}, '{cards[i]['cardholder_name']}', '{cards[i]['last_four_card_number']}', '{cards[i]['expiration_year']}', '{cards[i]['expiration_month']}');\n"
    print(string)

generate_credit_cards(num_users)
print_credit_cards()
# print(len(cards))
# endregion

# region ADDRESSES
addresses = []
states = [ 'AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY' ];

def street_parser():
    get_street = fake.street_address()
    street_arr = get_street.split()
    street1 = " ".join(street_arr[0:3])
    street2 = 'NULL'
    if len(street_arr) > 3:
        street2 = " ".join(street_arr[3:])
    return [street1, street2]

def recipient_name(first_name = fake.first_name(), last_name = fake.last_name()): 
    fname = first_name
    lname = last_name
    return f"{fname} {lname}"

def who_is_recipient(user):
    random_int = randint(1,100)
    is_self = False
    name = ''
    if random_int < 85:
        name = recipient_name(user['first_name'], user['last_name'])
        is_self = True
    elif random_int < 94:
        name = recipient_name(last_name = user['last_name'])
    else:
        name = recipient_name()    
    return [name, is_self]


def ship_bill(is_shipping = False, is_billing = False):
    return [is_shipping, is_billing]

def generate_addresses_for_user(num_addresses, user):
    i = 0
    has_shipping = 0
    has_billing = 0

    while (has_shipping == 0 or has_billing == 0) or i < num_addresses:
        if num_addresses == 1:
            shipping_billing = ship_bill(1,1)
        else:
            shipping_billing = ship_bill(0,0)

        parsed_street = street_parser()
        address = {
            "address_id"     : i + 1,
            "user_id"        : user['user_id'],
            "recipient_name" : '',
            "street"         : parsed_street[0],
            "street2"        : parsed_street[1],
            "city"           : fake.city(),
            "state"          : choice(states),
            "zip"            : fake.postcode(),
            "is_shipping"    : shipping_billing[0],
            "is_billing"     : shipping_billing[1],
        }
        who_receives = who_is_recipient(user)
        address['recipient_name'] = who_receives[0]
        shipping_billing_split = [0,1,1]
        if who_receives[1] == False or (who_receives[1] == True and i > 0):
            address['is_shipping'] = shipping_billing_split.pop(choice([0,1,1]))
            address['is_billing'] = choice(shipping_billing_split)
        addresses.append(address)
        
        if address['is_shipping'] == 1:
            has_shipping = 1
        if address['is_billing'] == 1:
            has_billing = 1
        i += 1

def generate_addresses(num_users):
    addresses.clear()
    i = 0
    while i < num_users:
        num_addresses = choice([1,1,1,1,1,2,2])
        user = user_list[i]
        generate_addresses_for_user(num_addresses, user)
        i += 1

def print_addresses():
    string = ""
    values = f"(user_id, recipient_name, street, street2, city, state, zip, is_shipping, is_billing)"
    for i in range(len(addresses)):
        street2_val = f"'{addresses[i]['street2']}'"
        string = string + f"INSERT INTO addresses {values} VALUES({addresses[i]['user_id'] if 'user_id' in addresses[i] else i + 1}, '{addresses[i]['recipient_name']}', '{addresses[i]['street']}', {'NULL' if addresses[i]['street2'] == 'NULL' else f'{street2_val}'}, '{addresses[i]['city']}', '{addresses[i]['state']}', '{addresses[i]['zip']}', {addresses[i]['is_shipping']}, {addresses[i]['is_billing']});\n"
    print(string)

generate_addresses(num_users)
print_addresses()
# print(len(addresses))
# endregion



####
def generate_products():
    df = pd.read_csv('../safeway-products-scraper/safewayData.csv',index_col=False)

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
        products.append(product)
    # print(products)


def print_products():
    print("um")
    string = ""
    values = f"(upc, prod_name, prod_description, brand, category, price_per_unit, image_url, available_stock, reserved_stock, shipped_stock)"
    for i in range(len(products)):
        string = string + f"INSERT INTO products VALUES('{products[i]['upc']}', '{products[i]['prod_name']}', '{products[i]['prod_description']}', '{products[i]['brand']}', '{products[i]['category']}', {products[i]['price_per_unit']}, '{products[i]['image_url']}', {products[i]['available_stock']}, {products[i]['reserved_stock']}, {products[i]['shipped_stock']},);\n"
        # string = string + f"INSERT INTO products {values} VALUES('{products[i]['upc']}', '{products[i]['prod_name']}', '{products[i]['prod_description']}', '{products[i]['brand']}', '{products[i]['category']}', {products[i]['price_per_unit']}, '{products[i]['image_url']}', {products[i]['available_stock']}, {products[i]['reserved_stock']}, {products[i]['shipped_stock']},);\n"
    print(string)
# print_products()
generate_products()













####
def getOrderAddress(userId):
    possAddresses = []
    for address in addresses:
        if address['user_id'] == userId:
            possAddresses.append(address['address_id'])
    #return random address from user
    return choice(possAddresses)

def getOrderCard(userId):
    possCards = []
    for card in cards:
        if card['user_id'] == userId:
            possCards.append(card['card_id'])
    #return random address from user
    return choice(possCards)


def generate_order_items(order_id, numItems):
    totalPrice = 0
    for i in range(numItems):
        quantity = randint(1, 10)
        print(products)
        product = choice(products)
        order_item = {
            "order_id": order_id,
            "product_id": product['product_id'],
            "quantity": quantity
        }
        totalPrice += (quantity*product['price'])
        order_items.append(order_item)
        print(order_item)
    return round(totalPrice, 2)

def generate_carts():
    i = 0
    for user in user_list:
        numCartItems = choices([randint(1,15), 0], [50, 50])[0]
        usedProducts = set()
        if numCartItems != 0:
            for i in range(numCartItems):
                product = choice(products)
                #disallow products already in cart#
                while product in usedProducts:
                    product = choice(products)
                #disallow products already in cart#
                   
                cart_item = {
                    "user_id": (user['user_id']), 
                    "product": product,
                    "quantity": randint(1, 10)
                    }
            carts.append(cart_item)








###

def date_ordered(order_num):
    day_variation = randint(-15, 15)
    if order_num == 1 and day_variation <= 0: return today
    
    months_back_in_days = (order_num * 30) - 30
    date_delta_val = day_variation + months_back_in_days
    date_delta = timedelta(date_delta_val)
    order_date = today - date_delta
    return order_date


def date_shipped(order_date):
    d100 = randint(1, 100)
    if d100 < 4: return ['NULL', "CANCELLED"]
    if (d100 < 50) and today == order_date: return ['NULL', "PENDING"]
    if (d100 >= 50) and today == order_date: return [today, "SHIPPED"]
    if (d100 > 95): return [choice([order_date, order_date + timedelta(1)]), "CANCELLED"]
    if (d100 > 85): return [order_date + timedelta(1), "SHIPPED"]
    return [order_date, "SHIPPED"]


def generate_order_for_user(order_num, user, order_date, shipping_date, order_status): #, date_ordered, date_shipped):
    order = {
        "order_id"        : None,
        "user_id"         : user['user_id'],
        "address_id"      : getOrderAddress(user['user_id']),
        "price"           : -1,
        "credit_card_id"  : getOrderCard(user['user_id']),
        'preliminary_id'  : order_num, 
        "date_ordered"    : order_date,
        "date_shipped"    : shipping_date,
        "order_status"    : order_status,
    }      
    # id = order['preliminary_id']
    # price = generate_order_items_per_order(order[id])
    num_order_items = randint(1,20)
    price = generate_order_items(order_num, num_order_items)
    orders[order_num]['price'] = price
    orders.append(order)



def generate_orders(num_users):
    orders.clear()
    user_id = 1
    order_num = 1
    user = user_list[user_id]

    while user_id < num_users:
        did_all_orders = False
        while not did_all_orders:
            d100 = randint(1,100)
            order_date = date_ordered(order_num)
            date_shipped_and_status = date_shipped(order_date)
            shipping_date = date_shipped_and_status[0]
            order_status = date_shipped_and_status[1]
            generate_order_for_user(order_num, user, order_date, shipping_date, order_status)
            
            if d100 > 91:
                did_all_orders = True
                user_id += 1

            order_num = 1

generate_orders(num_users)

# print(orders)



def print_orders():
    string = ""
    values = f"(user_id, address_id, price, credit_card_id, date_ordered, date_shipped, date_delivered, order_status)"
    for i in range(len(orders)):
        shipped_val = f"'{orders[i]['date_shipped']}'" 
        user_id = orders[i]['preliminary_id'] if 'user_id' in orders[i] else i + 1
        # string = string + f"INSERT INTO orders {values} VALUES({user_id}, {orders[i]['address_id']}, {orders[i]['price']}, {orders[i]['credit_card_id']}, '{orders[i]['date_ordered']}', {'NULL' if orders[i]['date_shipped'] == 'NULL' else f'{shipped_val}'}, {'NULL' if orders[i]['date_delivered'] == 'NULL' else f'{delivered_val}'}, '{orders[i]['order_status']}');\n"
        string = string + f"{user_id}, '{orders[i]['date_ordered']}', {'NULL' if orders[i]['date_shipped'] == 'NULL' else f'{shipped_val}'}, '{orders[i]['order_status']}';\n"
    print(string)

print_orders(num_users)