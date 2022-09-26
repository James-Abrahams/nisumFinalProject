from random import randint, choice, choices
from faker import Faker
from faker_food import FoodProvider
from math import floor, sqrt
from datetime import *
import string
fake = Faker()


#region GENERAL
num_users = 200


#endregion


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

# region CREDIT
cards = []


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

def ship_bill():
    return [True, True]

def street_parser():
    get_street = fake.street_address()
    street_arr = get_street.split()
    street1 = " ".join(street_arr[0:3])
    street2 = 'NULL'
    if len(street_arr) > 3:
        street2 = " ".join(street_arr[3:])
    return [street1, street2]
states = [ 'AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY' ];

def recipient_name(first_name = fake.first_name(), last_name = fake.last_name()): 
    fname = first_name
    lname = last_name
    return f"{fname} {lname}"

def generate_addresses_for_user(num_addresses, user):
    i = 0
    while i < num_addresses:
        shipping_billing = ship_bill()
        parsed_street = street_parser()
        address = {
            "address_id"     : i + 1, #CHANGE
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
        random_int = randint(1,100)
        if random_int < 84:
            address['recipient_name'] = recipient_name(user['first_name'], user['last_name'])
        elif random_int < 94:
            address['recipient_name'] = recipient_name(last_name = user['last_name'])
        else:
            address['recipient_name'] = recipient_name()
        addresses.append(address)
        i += 1

def generate_addresses(num_users):
    addresses.clear()
    i = 0
    while i < num_users:
        user = user_list[i]
        num_addresses_for_user = choice([1,1,1,2,3])
        # num_addresses_for_user = 10
        generate_addresses_for_user(num_addresses_for_user, user)
        i += 1

def print_addresses():
    string = ""
    values = f"(user_id, recipient_name, street, street2, city, state, zip, is_shipping, is_billing)"
    for i in range(len(addresses)):
        street2_val = f"'{addresses[i]['street2']}'"
        string = string + f"INSERT INTO addresses {values} VALUES({addresses[i]['address_id']}, {addresses[i]['user_id'] if 'user_id' in addresses[i] else i + 1}, '{addresses[i]['recipient_name']}', '{addresses[i]['street']}', {'NULL' if addresses[i]['street2'] == 'NULL' else f'{street2_val}'}, '{addresses[i]['city']}', '{addresses[i]['state']}', '{addresses[i]['zip']}', {addresses[i]['is_shipping']}, {addresses[i]['is_billing']});\n"
    print(string)

generate_addresses(num_users)
print_addresses()
# print(len(addresses))
# endregion



########TO DO BELOW




# # region PRODUCTS
# fake.add_provider(FoodProvider)
# product_ids = set()

# def generate_product_ids(total_items):
#     for i in range(1, total_items):
#         upc = ""
#         for j in range(1, 12+1):
#             upc += str(randint(0, 10))
#         product_ids.add(upc)
#     print(product_ids)

# generate_product_ids(3)
# product_ids = list(product_ids)
# print(len(product_ids), product_ids)
# product_list = []

# def generate_products():
#     #CHANGE TO SCRAPER
#     num_products = len(product_ids)
#     for i in range(0, num_products):
#         product = {
#             "upc"              : product_ids[i],
#             "prod_name"        : fake.dish(),
#             "brand"            : fake.dish_description(),
#             "prod_description" : fake.vegetable() + " Foods, Inc",
#             "category"         : choice([fake.ethnic_category(), fake.ingredient()]),
#             "price_per_unit"   : randint(0, 15) + 0.99,
#             "image_url"        : "https://picsum.photos/100/",
#             "available_stock"  : randint(0, 200),
#             "reserved_stock"   : randint(0, 30),
#             "shipped_stock"    : randint(0, 60)         ,
#         }

#         product_list.append(product)
#     print(product_list)

# generate_products()

# def print_products():
#     print("um")
#     string = ""
#     values = f"(upc, prod_name, prod_description, brand, category, price_per_unit, image_url, available_stock, reserved_stock, shipped_stock)"
#     for i in range(len(product_list)):
#         string = string + f"INSERT INTO products VALUES('{product_list[i]['upc']}', '{product_list[i]['prod_name']}', '{product_list[i]['prod_description']}', '{product_list[i]['brand']}', '{product_list[i]['category']}', {product_list[i]['price_per_unit']}, '{product_list[i]['image_url']}', {product_list[i]['available_stock']}, {product_list[i]['reserved_stock']}, {product_list[i]['shipped_stock']},);\n"
#     print(string)

# # endregion

# # region ORDERS
# print(fake.date())
# orders = []
# today = date.today()
# today = str(today).split("-")
# print(today)
# next_order_year  = int(today[0])
# next_order_month = int(today[1])
# next_order_day   = int(today[2])
# order_times = []
# today = datetime.today()

# num_orders = 10
# def rand_days():
#     return choice([0, randint(0,4)])

# for i in range(num_orders):
#     ordered = fake.date_between_dates(date_start=datetime(2018,1,1), date_end=datetime(2022,9,16))
#     to_ship_time = (ordered + timedelta(days=rand_days()))
#     shipped = choices(['NULL', to_ship_time], [100, 99])[0]
#     if shipped != 'NULL':
#         delivered = choices(['NULL' , shipped + timedelta(days=rand_days())], [200, 98])[0]

# print(order_times)

# def order_status(order_time):
#     for date in order_times:
#         if order_time['delivered'] != 'NULL':
#             return 'DELIVERED'
#         elif order_time['shipped'] != 'NULL':
#             return 'IN TRANSIT'
#         else:
#             return 'ORDERED'

# def generate_orders(num_orders):
#     total_orders = num_orders
#     i = 0
#     while i < total_orders:
        
#         order = {
#             "order_id"        : i + 1,
#             "user_id"         : i + 1,
#             "address_id"      : i + 1,
#             "price"           : round(randint(0, 300) + 0.99 * randint(1, 30), 2),
#             "credit_card_id"  : i + 1,
#             "date_ordered"    : order_times[i]['ordered'],
#             "date_shipped"    : order_times[i]['shipped'], #is shipped? if so ship date function
#             "order_status"    : order_status(order_times[i]),
#         }       

#         orders.append(order)
#         i += 1
#     print(orders)
# generate_orders(10)
# generate_orders(10)
# def print_orders():
#     string = ""
#     values = f"(user_id, address_id, price, credit_card_id, date_ordered, date_shipped, date_delivered, order_status)"
#     for i in range(len(orders)):
#         shipped_val = f"'{orders[i]['date_shipped']}'" 
#         delivered_val = f"'{orders[i]['date_delivered']}'" 
#         user_id = orders[i]['user_id'] if 'user_id' in orders[i] else i + 1
#         string = string + f"INSERT INTO orders {values} VALUES({user_id}, {orders[i]['address_id']}, {orders[i]['price']}, {orders[i]['credit_card_id']}, '{orders[i]['date_ordered']}', {'NULL' if orders[i]['date_shipped'] == 'NULL' else f'{shipped_val}'}, {'NULL' if orders[i]['date_delivered'] == 'NULL' else f'{delivered_val}'}, '{orders[i]['order_status']}');\n"
#     print(string)
# # endregion

# # region ORDER ITEMS
# order_items = []

# def generate_order_items(num_orders, total_items):
#     for i in range(1, total_items):
#         order_item = {
#             "order_id": randint(1, num_orders),
#             "product": choice(product_ids),
#             "quantity": randint(1, 100)
#         }
#         order_items.append(order_item)
#     print(order_items)

# generate_order_items(4, 20)

# def sort_order_items():
#     order_items.sort(key = lambda order_items: order_items["order_id"])
#     print(order_items)
# sort_order_items()

# def merge_duplicate_items_per_order():
#     count_dupes = 0
#     for i in range(len(order_items)):
#         for j in range(i +1, len(order_items)):
#             if (order_items[i]['order_id'] == order_items[j]['order_id']) and (order_items[i]['product'] == order_items[j]['product']): #and quantity not 0
#                 order_items[i]['quantity'] += order_items[j]['quantity']
#                 order_items[j]['quantity'] = 0
#                 count_dupes += 1
#     print(count_dupes, order_items)
# merge_duplicate_items_per_order()

# def delete_duplicate_items_per_order():
#     deleted_count = 0
#     for i in reversed(range(len(order_items))):
#         if order_items[i]['quantity'] == 0:
#             del order_items[i]
#             deleted_count += 1
#     print(deleted_count, order_items)


# delete_duplicate_items_per_order()

# def give_ids_to_order_items():
#     for i in range(len(order_items)):
#         order_items[i]['id'] = i + 1
#     print(order_items)
# give_ids_to_order_items()

# def reorder_dictionary_for_consistency():
#     for i in range(len(order_items)):
#         obj = order_items[i]
#         new_key_order = ['id', 'order_id', 'quantity', 'product']
#         reordered_obj = {k: obj[k] for k in new_key_order}
#         order_items[i] = reordered_obj
#     print(order_items)

# reorder_dictionary_for_consistency()


# def print_order_items():
#     print("um")
#     string = ""
#     values = f"(order_id, quantity, upc)"
#     for i in range(len(order_items)):
#         string = string + f"INSERT INTO order_items {values} VALUES({order_items[i]['order_id']}, {order_items[i]['quantity']}, '{order_items[i]['product']}');\n"
#     print(string)


# # endregion

# # region CART
# carts = []
# total_users = 16 # change to get from user generation file
# def users_with_carts(total_users):
#     active_users = set()
#     for i in range(floor(sqrt(total_users))):
#         active_users.add(randint(1, total_users))
#     return list(active_users)
# print(users_with_carts(total_users))

# def generate_cart(total_items):
#     for i in range(1, total_items):
#         cart_item = {
#             "user_id"       : choice(users_with_carts(total_users)),
#             "product"       : choice(products),
#             "quantity"      : randint(1, 100)
#         }
#         carts.append(cart_item)
# print(len(carts), generate_cart(10), carts)

# def merge_duplicate_items_per_cart():
#     count_dupes = 0
#     for i in range(len(carts)):
#         for j in range(i +1, len(carts)):
#             if (carts[i]['user_id'] == carts[j]['user_id']) and (carts[i]['product'] == carts[j]['product']):
#                 carts[i]['quantity'] += carts[j]['quantity']
#                 carts[j]['quantity'] = 0
#                 count_dupes += 1
#     print(count_dupes, carts)
# merge_duplicate_items_per_cart()

# def delete_duplicate_items_per_order():
#     deleted_count = 0
#     for i in reversed(range(len(carts))):
#         if carts[i]['quantity'] == 0:
#             del carts[i]
#             deleted_count += 1
#     # print(deleted_count, carts)

# delete_duplicate_items_per_order()

# def give_ids_to_order_items():
#     for i in range(len(carts)):
#         carts[i]['cart_item_id'] = i + 1
#     print(carts)
# give_ids_to_order_items()

# def print_carts():
#     print("um")
#     string = ""
#     values = f"(user_id, quantity, product)"
#     for i in range(len(carts)):
#         string = string + f"INSERT INTO carts {values} VALUES({carts[i]['user_id']}, {carts[i]['quantity']}, '{carts[i]['product']}');\n"
#     print(string)

# # endregion

# def print_all():
#     print_users()
#     print_addresses()
#     print_credit_cards()
#     print_products()
#     print_orders()
#     print_order_items()
#     print_carts()
