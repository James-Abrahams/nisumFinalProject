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
        lname = fake.last_name()
        email_bridge = choice(['', choice(['-','_',str(randint(0,9))])])
        email_affectation = choice(['', choice(['','',str(randint(0,9)),'fan',choice(['68', '419', '41968'])])])
        domain = choice(['com','net',choice(['edu','org','gov'])])
        person = {
            "user_id"       : i + 1,
            "email"         : fname.lower() + f"{email_bridge}{lname.lower()}{email_affectation}{randint(0,100)}@example.{domain}",
            "first_name"    : fname,
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
print(user_list)
# endregion















# region CREDIT
cards = []


def cardholder_name(first_name = fake.first_name(), last_name = fake.last_name()): 
    fname = first_name
    mname = choice(['' , ' ' + ''.join(choices([choice(list(string.ascii_letters.upper())), fake.first_name()], [4, 1])[0])])
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
            card['cardholder_name'] = cardholder_name(user['first_name'], user['last_name'])
        elif random_int < 97:
            card['cardholder_name'] = cardholder_name(last_name = user['last_name'])
        else:
            card['cardholder_name'] = cardholder_name()
        cards.append(card)
        i += 1

def generate_credit_cards(num_users):
    cards.clear()
    total_cards = num_users
    i = 0
    while i < total_cards:
        user = user_list[i]
        num_cards_for_user = choice([1,1,1,2,3])
        generate_cards_for_user(num_cards_for_user, user)
        i += num_cards_for_user

def print_credit_cards():
    string = ""
    values = f"(user_id, cardholder_name, last_four_card_number, expiration_year, expiration_month)"
    for i in range(len(cards)):
        user_id = cards[i]['user_id'] if 'user_id' in cards[i] else i + 1
        string = string + f"INSERT INTO credit_cards {values} VALUES ({user_id}, '{cards[i]['cardholder_name']}', '{cards[i]['last_four_card_number']}', '{cards[i]['expiration_year']}', '{cards[i]['expiration_month']}');\n"
    print(string)

generate_credit_cards(num_users)
print_credit_cards()
# endregion