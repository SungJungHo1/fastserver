from pymongo import MongoClient
from Ordersdatas import *
from datetime import *
from random import *
from datetime import datetime, timedelta, timezone

client = MongoClient('mongodb://fastfood:fastfood@43.200.202.12', 27017)

mydb = client['FastFoodDB']
mycol = mydb['OrderDatas']
mycustomer = mydb['Customer']
errcol = mydb['Errors']
service = mydb['service']


def Insert_Data(UserName, UserId, Delivery_Fee, Order_Data, Cart, lan, lng, Service_Money):
    z = randrange(0, 900)
    Order_Code = str(datetime.now().hour) + str(datetime.now().month) + str(datetime.now().year) + \
        str(datetime.now().day) + \
        str(int(datetime.now().microsecond / 1000)) + str(z)[-1]

    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d %H:%M:%S'
    str_datetime = datetime.strftime(datetime_utc2, format)
    if find_cust(UserId) == None:
        Insert_cust(UserName, UserId, Order_Data['phone'])
    mycol.insert_one({"Order_Code": Order_Code, "UserName": UserName, "UserId": UserId,
                     "delivery_fee": Delivery_Fee, "Order_Data": Order_Data, "Cart": Cart, 'Service_Money': Service_Money, "Order_End": True, 'Del_End': False, "Memo": "음식 문앞에두고 꼭 전화한번 주세요!", "Rider": "", "Order_Time": str(str_datetime), 'lan':  lan, 'lng': lng})

    return Order_Code


def Insert_cust(UserName, UserId, phone):
    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d %H:%M:%S'
    str_datetime = datetime.strftime(datetime_utc2, format)

    mycustomer.insert_one(
        {"UserName": UserName, 'UserId': UserId, "address1": "", "address2": "", "phone": phone, "memo": "", 'Point': "1000", 'Start_Time': str_datetime})


def find_cust(UserId):

    DBs = mycustomer.find_one({"UserId": str(UserId), })
    return DBs


def find_Allcust():

    DBs = mycustomer.find()
    for i in DBs:
        print(i)
    return DBs


def Insert_service():

    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d %H:%M:%S'
    str_datetime = datetime.strftime(datetime_utc2, format)

    service.insert_one({"Money": 1000, "Time": str(str_datetime)})


def find_service():

    DBs = service.find().sort("_id", -1)

    return DBs[0]["Money"]


def Insert_Err(Errors):
    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d %H:%M:%S'
    str_datetime = datetime.strftime(datetime_utc2, format)

    errcol.insert_one({"Errors": Errors, "Time": str(str_datetime)})


def Edit_Data(Order_Code, Ur):
    ttt = mycol.update_one({"Order_Code": str(Order_Code)}, {
        '$set': {'Addres_Url': str(Ur)}})


def Drop_Users():
    mycustomer.drop()


if __name__ == "__main__":
    # Insert_Data("Uad859360a7e2589c8c213b3b47fc27a2",'크턱',orderdata,cart)
    # Drop_Users()
    # z = randrange(0,900)
    # Order_Code = str(datetime.now().hour) + str(datetime.now().month) + str(datetime.now().year) + str(datetime.now().day) + str(int(datetime.now().microsecond / 1000)) + str(z)[-1]
    # print('Order_Code')
    # x = errcol.find()
    # for i in x:
    #     print(i)
    Insert_service()
    # print(find_service())
    # Insert_cust("크턱", "010-6675-5961")
    # find_Allcust()
    # Drop_Users()
    # Insert_Err("sdsdsdsdsds")
    # Edit_Data("1382022238380", "https://ibb.co/r22bKFs")
