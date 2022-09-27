from random import randint, choice, choices
from faker import Faker
from faker_food import FoodProvider
from math import floor, sqrt
from datetime import *
import string
fake = Faker()

#region OLD CODE TO MAKE IT PRETTY
print(fake.date())
orders = []
today = date.today()
today = str(today).split("-")
print(today)
next_order_year  = int(today[0])
next_order_month = int(today[1])
next_order_day   = int(today[2])
#order_times = []
today = datetime.today()


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
def rand_days():
        return choice([0, randint(0,2)])

def getOrderDates():
    order_dates = []
    ordered = fake.date_between_dates(date_start=datetime(2018,1,1), date_end=datetime(2022,9,16))
    to_ship_time = (ordered + timedelta(days=rand_days()))
    shipped = choices(['NULL', to_ship_time], [100, 99])[0] 
    order_dates.append({'ordered': str(ordered), 'shipped': str(shipped)})
    # print('ordered: ', ordered, 'shipped: ', shipped, end = '\n')
    print(order_dates)
    return order_dates

def getOrderAddress(userId):
    possAddresses = []
    for address in addresses:
        if address['user_id'] == userId:
            possAddresses.append(address['address_id'])
    #return random address from user
    return choice(possAddresses)

def getOrderCard(userId):
    possCards = []
    for address in cards:
        if address['user_id'] == userId:
            possAddresses.append(address['credit_id'])
    #return random address from user
    return choice(possCards)

def order_status(order_time):
    for date in order_times:
        if order_time['delivered'] != 'NULL':
            return 'DELIVERED'
        elif order_time['shipped'] != 'NULL':
            return 'IN TRANSIT'
        else:
            return 'ORDERED'

def generate_orders():
    # total_orders = num_orders
    i = 0
    for user in user_list:
        numUserOrders = randint(0,2)

        while i < numUserOrders:
            orderDates = getOrderDates()
            order = {
                "user_id"         : user['user_id'],
                "address_id"      : getOrderAddress(user['user_id']),
                "price"           : round(randint(0, 300) + 0.99 * randint(1, 30), 2),
                "credit_card_id"  : getOrderCard(user['user_id']),
                "date_ordered"    : orderDates['ordered'],
                "date_shipped"    : orderDates['shipped'], 
                "order_status"    : order_status(orderDates),
            }       

            orders.append(order)
            i += 1
            price = generate_order_items_per_order(order[id])
        print(orders)

    generate_orders(10)




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




#justin


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
    # print('ordered: ', ordered, 'shipped: ', shipped, 'delivered: ', delivered, end = '\n')
print(order_times)