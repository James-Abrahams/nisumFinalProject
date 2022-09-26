from random import randint, choice, choices
from faker import Faker
from faker_food import FoodProvider
from math import floor, sqrt
from datetime import *
import string
fake = Faker()

num_users = 10000


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
# print_users()
# print(user_list)
print(len(user_list))
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
# print_credit_cards()

print(len(cards))

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
# print_addresses()
print(len(addresses))
# endregion
