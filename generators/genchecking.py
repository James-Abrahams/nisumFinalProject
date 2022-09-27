from random import randint, choice, choices
from faker import Faker
from faker_food import FoodProvider
from math import floor, sqrt
from datetime import datetime, timedelta, date
import string
fake = Faker()

num_users = 20
num_products_more_or_less = 15
today = date.today()
print("today: ", today)

orders = []


def date_ordered(order_num):
    day_variation = randint(-15, 15)
    if order_num == 1 and day_variation > 0: return today
    
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
    if (d100 > 70): return [today + timedelta(1), "SHIPPED"]
    if (d100 > 85): return [choice([today, today + timedelta(1)]), "CANCELLED"]
    return [today, "SHIPPED"]


def generate_order_for_user(user, order_date, shipping_date, order_status): #, date_ordered, date_shipped):
    i = 0
    order = {
        # "order_id"        : i + 1,
        # "user_id"         : i + 1,
        # "address_id"      : i + 1,
        # "price"           : 0,
        # "credit_card_id"  : i + 1,
        'preliminary_id'  : user, 
        "date_ordered"    : order_date,
        "date_shipped"    : shipping_date,
        "order_status"    : order_status,
    }      
    # id = order['preliminary_id']
    # price = generate_order_items_per_order(order[id])
    
    orders.append(order)
    i += 1


def generate_orders():
    orders.clear()
    total = 0
    user_id = 1
    order_num = 1
    while user_id < 5:
        did_all_orders = False
        while not did_all_orders:
            d100 = randint(1,100)
            order_date = date_ordered(order_num)
            date_shipped_and_status = date_shipped(order_date)
            # print(date_shipped_and_status)
            shipping_date = date_shipped_and_status[0]
            order_status = date_shipped_and_status[1]
            generate_order_for_user(user_id, order_date, shipping_date, order_status) #change to user
            
            
            if d100 > 91:
                did_all_orders = True
                user_id += 1
                # print(f"total for person {user_id}: {order_num} \n")
                order_num = 1
            else:
                order_num += 1
            total += 1

generate_orders()

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

print_orders()