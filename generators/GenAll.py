from random import randint, choice, choices, shuffle
from datetime import datetime, timedelta, date
from shutil import make_archive
from faker import Faker
import pandas as pd
import string

fake = Faker()
df = pd.read_csv('../safeway-products-scraper/safewayData.csv',index_col=False)
for col in list(df.columns):
    try:
        df[col] = df[col].str.replace(r"'", r"\'")
    except AttributeError:
        print(col)
        continue

# f = open("super_db_seed.txt", "w") #9901
# num_users = 9001
# f = open("super_db_seed_mini.txt", "w") #10 users
# num_users = 10

f = open("super_db_seed_lite.txt", "w") #9901
num_users = 100

states = [ 'AL', 'AK', 'AS', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FM', 'FL', 'GA', 'GU', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MH', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'MP', 'OH', 'OK', 'OR', 'PW', 'PA', 'PR', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VI', 'VA', 'WA', 'WV', 'WI', 'WY' ];


num_products_more_or_less = 15
today = date.today()

orders          = []
carts           = []
order_items     = []
products        = []
users           = []
cards           = []
addresses       = []
reserved_items  = dict()
shipped_items   = dict()


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
    users.clear()
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
            "user_password" : fake.password(),
            "phone"         : phone(),
        }       

        users.append(person)


def print_users():
    string = ""
    values = f"(email, first_name, last_name, user_password, phone)"
    for i in range(len(users)):
        string = string + f"INSERT INTO users {values} VALUES ('{users[i]['email']}', '{users[i]['first_name']}', '{users[i]['last_name']}', '{users[i]['user_password']}', '{users[i]['phone']}');\n"
    f.write(string)
generate_users(num_users)


def cardholder_name(first_name = fake.first_name(), last_name = fake.last_name(), middle_name = None): 
    fname = first_name
    if middle_name == None:
        mname = choice(['' , '', ' ' + ''.join(choices([choice(list(string.ascii_letters.upper())), fake.first_name()], [4, 1])[0])])
    else:
        mname = choice(['' , '', ' ' + ''.join(choices([middle_name[0], middle_name], [4, 1])[0])])
    lname = last_name
    return f"{fname}{mname} {lname}"


def generate_cards_for_user(card_id, num_cards, user):
    i = 0
    while i < num_cards:
        random_int = randint(1,100)
        exp = fake.credit_card_expire().split("/")
        card = {
            "card_id"               : card_id + i,
            "user_id"               : user['user_id'],
            "cardholder_name"       : "",
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
    return i


def generate_credit_cards(num_users):
    cards.clear()
    i = 0
    card_id = 1
    while i < num_users:
        user = users[i]
        num_cards_for_user = choice([1,1,1,1,2,3])
        cards_generated = generate_cards_for_user(card_id, num_cards_for_user, user)
        i += 1
        card_id += cards_generated


def print_credit_cards():
    string = ""
    values = f"(user_id, cardholder_name, last_four_card_number, expiration_year, expiration_month)"
    for i in range(len(cards)):
        user_id = cards[i]['user_id'] if 'user_id' in cards[i] else i + 1
        string = string + f"INSERT INTO credit_cards {values} VALUES ({user_id}, '{cards[i]['cardholder_name']}', '{cards[i]['last_four_card_number']}', '{cards[i]['expiration_year']}', '{cards[i]['expiration_month']}');\n"
    f.write(string)

generate_credit_cards(num_users)


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


def generate_addresses_for_user(address_id, num_addresses, user):
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
            "address_id"     : address_id + i,
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
    return i


def generate_addresses(num_users):
    addresses.clear()
    i = 0
    address_id = 1
    while i < num_users:
        num_addresses = choice([1,1,1,1,1,2,2])
        user = users[i]
        addresses_generated = generate_addresses_for_user(address_id, num_addresses, user)
        i += 1
        address_id += addresses_generated


def print_addresses():
    string = ""
    values = f"(user_id, recipient_name, street, street2, city, state, zip, is_shipping, is_billing)"
    for i in range(len(addresses)):
        street2_val = f"'{addresses[i]['street2']}'"
        string = string + f"INSERT INTO addresses {values} VALUES({addresses[i]['user_id'] if 'user_id' in addresses[i] else i + 1}, '{addresses[i]['recipient_name']}', '{addresses[i]['street']}', {'NULL' if addresses[i]['street2'] == 'NULL' else f'{street2_val}'}, '{addresses[i]['city']}', '{addresses[i]['state']}', '{addresses[i]['zip']}', {addresses[i]['is_shipping']}, {addresses[i]['is_billing']});\n"
    f.write(string)
generate_addresses(num_users)


def create_product(code):
    row = df.loc[df['ProdCode'] == code]
    product = {
        "upc"               : row.iloc[0]['ProdCode'],
        "prod_name"         : row.iloc[0]['ProdName'],
        "brand"             : row.iloc[0]['Brand'],
        "prod_description"  : row.iloc[0]['ProdDescription'],
        "category"          : row.iloc[0]['Category'],
        "price_per_unit"    : float((row.iloc[0]['PricePerUnit']).split()[0]),
        "image_url"         : row.iloc[0]['ImageURL'],
        "available_stock"   : 0,
        "reserved_stock"    : 0,
        "shipped_stock"     : 0,
    }
    upc = product['upc']
    reserved_items[upc] = 0 
    shipped_items[upc] = 0
    return product


def generate_products():
    products.clear()
    codes = list(df['ProdCode'])
    # random_products = randint(1, 1760) ##################
    # codes = codes[random_products:random_products+40]####
    for code in codes:
        products.append(create_product(code))


def print_products():
    string = ""
    for i in range(len(products)):
        string = string + f"INSERT INTO products VALUES('{products[i]['upc']}', '{products[i]['prod_name']}', '{products[i]['brand']}', '{products[i]['category']}', '{products[i]['prod_description']}', {products[i]['price_per_unit']}, '{products[i]['image_url']}', {products[i]['available_stock']}, {products[i]['reserved_stock']}, {products[i]['shipped_stock']});\n"
    f.write(string)
generate_products()


def getOrderAddress(start_index, userId):
    possAddresses = []
    address_range = len(addresses)
    for i in range(start_index, address_range):
        address = addresses[i]
        if address['user_id'] == userId:
            possAddresses.append(address['address_id'])
        else:
            break
    return possAddresses


def getOrderCard(start_index, userId):
    possCards = []
    card_range = len(cards)
    for i in range(start_index, card_range):
        card = cards[i]
        if card['user_id'] == userId:
            possCards.append(card['card_id'])
        else:
            break
    return possCards


def generate_order_items(pre_id, numItems):
    totalPrice = 0
    usedProducts = set()
    for i in range(numItems):
        quantity = randint(1, randint(1,6))
        product = choice(products)
        while product['upc'] in usedProducts:
            product = choice(products)
        usedProducts.add(product['upc'])
        order_item = {
            "order_id"    : None,
            "pre_id"      : pre_id,
            "upc"         : product['upc'],
            "quantity"    : quantity,
            "total_price" : -1,
        }
        totalPrice += (quantity*product['price_per_unit'])
        order_item['total_price'] = round(totalPrice, 2)
        order_items.append(order_item)
    return order_item


def print_order_items():
    string = ""
    values = f"(order_id, quantity, upc)"
    for i in range(len(order_items)):
        string = string + f"INSERT INTO order_items {values} VALUES({order_items[i]['order_id']}, {order_items[i]['quantity']}, '{order_items[i]['upc']}');\n"
    f.write(string)


def generate_carts():
    i = 0
    for user in users:
        numCartItems = choices([randint(1,15), 0], [50, 50])[0]
        usedProducts = set()
        if numCartItems != 0:
            for i in range(numCartItems):
                product = choice(products)

                while product['upc'] in usedProducts:
                    product = choice(products)
                usedProducts.add(product['upc'])
                   
                cart_item = {
                    "user_id": (user['user_id']), 
                    "upc": product['upc'],
                    "quantity": randint(1, 10)
                    }
                carts.append(cart_item)
    shuffle(carts)


def print_carts():
    string = ""
    values = f"(user_id, quantity, upc)"
    for i in range(len(carts)):
        string = string + f"INSERT INTO cart_items {values} VALUES({carts[i]['user_id']}, {carts[i]['quantity']}, '{carts[i]['upc']}');\n"
    f.write(string)

generate_carts()


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


def generate_order_for_user(order_num, user, order_date, shipping_date, order_status, possible_addresses, possible_credit_cards):
    order = {
        "order_id"        : None,
        "user_id"         : user['user_id'],
        "address_id"      : choice(possible_addresses),
        "price"           : -1,
        "credit_card_id"  : choice(possible_credit_cards),
        'pre_id'          : order_num, 
        "date_ordered"    : order_date,
        "date_shipped"    : shipping_date,
        "order_status"    : order_status,
    }      

    num_order_items = randint(1,20)
    order_item = generate_order_items(order_num, num_order_items)
    price = order_item['total_price']
    order['price'] = price
    if order['order_status'] == 'PENDING':
        reserved_items[order_item['upc']] += order_item['quantity']
    elif order['order_status'] == 'SHIPPED':
        shipped_items[order_item['upc']] += order_item['quantity']

    orders.append(order)


def generate_orders(num_users):
    orders.clear()
    user_idx = 0
    order_num = 1
    start_index_addresses = 0
    start_index_cards = 0

    while user_idx < num_users:
        user = users[user_idx]
        possible_addresses = getOrderAddress(start_index_addresses, user['user_id'])
        start_index_addresses += len(possible_addresses)

        possible_credit_cards = getOrderCard(start_index_cards, user['user_id'])
        start_index_cards += len(possible_credit_cards)
        
        user_order_num = 1
        did_all_orders = False
        while did_all_orders == False:
            d100 = randint(1,100)
            
            order_date = date_ordered(user_order_num)
            date_shipped_and_status = date_shipped(order_date)
            
            shipping_date = date_shipped_and_status[0]
            order_status = date_shipped_and_status[1]
            generate_order_for_user(order_num, user, order_date, shipping_date, order_status, possible_addresses, possible_credit_cards)
            
            if d100 > 92 or user_order_num == 240:
                did_all_orders = True
                user_idx += 1
                user_order_num = 1

            user_order_num += 1
            order_num += 1


def print_orders():
    string = ""
    values = f"(user_id, address_id, price, credit_card_id, date_ordered, date_shipped, order_status)"
    for i in range(len(orders)):
        shipped_val = f"'{orders[i]['date_shipped']}'" 
        user_id = orders[i]['user_id']
        string = string + f"INSERT INTO orders {values} VALUES({user_id}, {orders[i]['address_id']}, {orders[i]['price']}, {orders[i]['credit_card_id']}, '{orders[i]['date_ordered']}', {'NULL' if orders[i]['date_shipped'] == 'NULL' else f'{shipped_val}'}, '{orders[i]['order_status']}');\n"
    f.write(string)
generate_orders(num_users)


def add_quantities_to_products():
    for product in products:
        upc = product['upc']
        if upc in reserved_items: product['reserved_stock'] += reserved_items[upc]
        if upc in shipped_items: product['shipped_stock'] += shipped_items[upc]
        if product['reserved_stock'] == 0:
            product['available_stock'] = randint(randint(1,10), randint(11,20))
        else:
            product['available_stock'] = int(product['reserved_stock'] * float(f"{randint(0, 2)}.{randint(0, 9)}{randint(0, 9)}{randint(0, 9)}")) + randint(0, 10)
add_quantities_to_products()


def sort_orders():
    orders.sort(key = lambda order: datetime.strptime(str(order['date_ordered']), "%Y-%m-%d"))
sort_orders()


def give_ids_to_orders():
    for i in range(len(orders)):
        orders[i]['order_id'] = i + 1
give_ids_to_orders()


def match_order_item_ids():
    id_dict = {}
    for order in orders:
        id_dict[order['pre_id']] = order['order_id']
    for item in order_items:
        item['order_id'] = id_dict[item['pre_id']] 
match_order_item_ids()


def sort_order_items():
    order_items.sort(key = lambda item: item['order_id'])
sort_order_items()


def create_text():
    print_products()
    f.write(f"\n\n\n")
    print_users()
    f.write(f"\n\n\n")
    print_credit_cards()
    f.write(f"\n\n\n")
    print_addresses()
    f.write(f"\n\n\n")
    print_carts()
    f.write(f"\n\n\n")
    print_orders()
    f.write(f"\n\n\n")
    print_order_items()
create_text()

f.close() 
# make_archive('super_db_seed_zipped', 'zip', '/Users/j/Desktop/work/final/nisumFinalProject/generators/', 'super_db_seed_lite.txt')
make_archive('db_seed_lite', 'zip', '/Users/j/Desktop/work/final/nisumFinalProject/generators/', 'super_db_seed_lite.txt')