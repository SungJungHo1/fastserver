from pymongo import MongoClient
from Ordersdatas import *
from datetime import *
from random import *
from datetime import datetime, timedelta, timezone
import shortuuid
import re

pattern = re.compile("- 매장명 : \S+")

client = MongoClient('mongodb://fastfood:fastfood@43.200.202.12', 27017)

mydb = client['FastFoodDB']
mycol = mydb['OrderDatas']
mycustomer = mydb['Customer']
myAccount = mydb['Account']
MyAddress = mydb['Address']
errcol = mydb['Errors']
service = mydb['service']
WaitTime = mydb['WaitTime']
Refund_Data = mydb['Refund_Data']

def Insert_WaitTime(Time,message):
    WaitTime.insert_one({"Time":Time,"message":message})

def Insert_Address(add1,add2,phone,add_Name,UserName,UserId,friend):
    add_Code = shortuuid.uuid()

    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d %H:%M:%S'
    str_datetime = datetime.strftime(datetime_utc2, format)

    MyAddress.insert_one({'add_Code':add_Code,'str_datetime':str_datetime,'UserName':UserName,'UserId':UserId,"add1":add1,"add2":add2,'phone':phone,'add_Name':add_Name,'Addres_Url':"",'friend':friend})
    return add_Code


def Edit_UserN(UserId, UserName,phone):
    if phone != '66':
        mycustomer.update_one({"UserId": str(UserId)}, {
            '$set': {'UserName': str(UserName),'phone':str(phone)}})
    else:
        mycustomer.update_one({"UserId": str(UserId)}, {
            '$set': {'UserName': str(UserName)}})
def Add_Order_Log(UserId):
    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d'
    str_datetime = datetime.strftime(datetime_utc2, format)
    mycustomer.update_one({"UserId": str(UserId)}, {
            '$set': {'Last_Order_Time': str_datetime,"First_Coupon":False}})
    mycustomer.update_one({ 'UserId' : str(UserId)}, {"$inc" : {"Order_Total_Count" : 1}})


def Insert_Data(UserName, UserId, Delivery_Fee, Order_Data, Cart, lan, lng, Service_Money,new_cus,thumbnail_url,use_point):
    # z = randrange(0, 900)
    Order_Code = shortuuid.uuid()

    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d %H:%M:%S'
    str_datetime = datetime.strftime(datetime_utc2, format)
    cus = find_cust(UserId)
    if cus != None:
        Add_Order_Log(UserId)
    if cus == None:
        Insert_cust(UserName, UserId, Order_Data['phone'])
    elif cus["phone"] == "01000000000" or cus["phone"] == "66":
        Edit_UserN(UserId,UserName,Order_Data['phone'])
    mycol.insert_one({"Order_Code": Order_Code, "UserName": UserName, "UserId": UserId,
                    'use_point':use_point,
                     "delivery_fee": Delivery_Fee, "Order_Data": Order_Data, "Cart": Cart,
                      'Service_Money': Service_Money, "Order_End": True, 'Del_End': False, "Memo": "음식 문앞에두고 벨 눌러주세요~!",
                       "Rider": "", "Order_Time": str(str_datetime), 'lan':  lan, 'lng': lng,'new_cus':new_cus,'thumbnail_url':thumbnail_url})
    
    return Order_Code
    

def Insert_Refund_Data(UserName, UserId,Name, BankName, accountName):
    # z = randrange(0, 900)
    Order_Code = shortuuid.uuid()

    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d %H:%M:%S'
    str_datetime = datetime.strftime(datetime_utc2, format)

    Refund_Data.insert_one({"Refund_Code": Order_Code, "UserName": UserName, "UserId": UserId,
                       "Refund_Time": str(str_datetime),'Name':Name,'BankName':BankName,'accountName':accountName})

    return Order_Code

def Insert_cust(UserName, UserId, phone):
    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d %H:%M:%S'
    str_datetime = datetime.strftime(datetime_utc2, format)

    mycustomer.insert_one(
        {"UserName": UserName, 'UserId': UserId, "address1": "", "address2": "", "phone": phone, "memo": "", 'Point': 0, 'Start_Time': str_datetime,
        'coupon_List':[],"First_Coupon":True,"1W_Coupon":True,"1M_Coupon":True,'Last_Order_Time':"",'Order_Total_Count':0})

def find_Account():

    DBs = myAccount.find_one({"number": 1, },{'_id': 0})

    return DBs

def find_cust(UserId):

    DBs = mycustomer.find_one({"UserId": str(UserId), },{'_id': 0})

    return DBs

def find_Order_Datas(UserId):
    lis = []
    DBs = mycol.find({"UserId": str(UserId)},{'_id': 0}).sort("_id", -1)
    for i in DBs:
        lis.append(i)
        
    return {'Order_List':lis}

def DB_Order_Data(Order_Code):
    DBs = mycol.find_one({"Order_Code": str(Order_Code)},{'_id': 0})
    
    return DBs

def find_Allcust():

    DBs = mycustomer.find()
    return DBs


def Insert_service():

    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d %H:%M:%S'
    str_datetime = datetime.strftime(datetime_utc2, format)

    # service.insert_one({"Money": 3000,"ment":"วันนี้หยุดบริการ 1 วัน 🙏\nเปิดบริการอีกทีในวันพรุ่งนี้ค่ะ🙏\nขอบคุณที่ใช้บริการFASTFOODนะคะ","opened":False, "Time": str(str_datetime)})
    service.insert_one({"Money": 3000,"ment":"Test Ment","opened":False, "Time": str(str_datetime)})


def find_service():

    DBs = service.find().sort("_id", -1)

    return DBs[0]


def Insert_Err(Errors):
    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d %H:%M:%S'
    str_datetime = datetime.strftime(datetime_utc2, format)

    errcol.insert_one({"Errors": Errors, "Time": str(str_datetime)})


def Edit_Data(Order_Code, Ur):
    mycol.update_one({"Order_Code": str(Order_Code)}, {
        '$set': {'Addres_Url': str(Ur)}})



def Edit_Add_Data(add_Code, Ur):
    MyAddress.update_one({"add_Code": str(add_Code)}, {
        '$set': {'Addres_Url': str(Ur)}})





def Edit_Point(Order_Code, point):
    mycustomer.update_one({"UserId": str(Order_Code)}, {
        '$inc': {'Point': -int(point)}})

def Add_cus_AddrData(UserId, Ur):
    mycustomer.update_one({"UserId": str(UserId)}, { '$addToSet': { 'AddLists':  Ur} })


def Drop_Users():
    mycustomer.drop()


if __name__ == "__main__":
    # Add_cus_AddrData(5485851021533487,{'주소이름':'광주집','주소1':'월곡동','주소2':'빌라','좌표1':35.1673079492069,'좌표2':126.80982365415,})
    www = MyAddress.find({})
    # www = Refund_Data.find().sort("_id", -1)
    # sdsdsd= mycol.find({'UserId':'U812329a68632f4237dea561c6ba1d413'})
    for i in www:
        print(i)
    # for i in www:
    #     # if "Refund_Code" in i:
    #     # Refund_Data.delete_one({'Order_Code':i['Order_Code']})

    #     print(i)
    # Edit_Point('U812329a68632f4237dea561c6ba1d413',100)
    # print(find_Account())
    # print(find_cust('194958326369375'))
    # mycustomer.delete_one({'UserId': '194958326369375'})
    # print(find_cust('U812329a68632f4237dea561c6ba1d413'))
    # print(find_Order_Datas('U812329a68632f4237dea561c6ba1d413'))
    # print(www["message"])
    # tet = pattern.search(www["message"]).group()
    # print(tet.replace("- 매장명 : ",""))
    # Insert_Data("Uad859360a7e2589c8c213b3b47fc27a2",'크턱',orderdata,cart)
    # Drop_Users()
    # z = randrange(0,900)
    # Order_Code = str(datetime.now().hour) + str(datetime.now().month) + str(datetime.now().year) + str(datetime.now().day) + str(int(datetime.now().microsecond / 1000)) + str(z)[-1]
    # print('Order_Code')
    # x = errcol.find()
    # for i in x:
    #     print(i)
    # find_Order_Datas('Uad859360a7e2589c8c213b3b47fc27a2')
    # print(find_service())
    # Order_Code = shortuuid.uuid()
    # print(Order_Code)
    # print(type(Order_Code))
    # print(find_service())
    # Insert_cust("크턱", "010-6675-5961")
    # find_Allcust()
    # DB_Order_Data('LqVxBH5pAxpWvnJhYEfVR8')
    # print(find_Account())
    # Drop_Users()
    # Insert_Err("sdsdsdsdsds")
    # Edit_Data("1382022238380", "https://ibb.co/r22bKFs")