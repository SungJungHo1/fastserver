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
Coupon_Data = mydb['Coupon_Data']

def Use_Coupon(쿠폰번호):
    Coupon_Data.update_one({'쿠폰번호':str(쿠폰번호)},{"$set":{"쿠폰사용여부":True}})

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
            '$set': {'Last_Order_Time': str_datetime}})
    mycustomer.update_one({ 'UserId' : str(UserId)}, {"$inc" : {"Order_Total_Count" : 1}})

def Del_Coupon(userId,Coupon_Code):
    mycustomer.update_one({"UserId":userId},{ "$pull": { "coupon_List": {"쿠폰번호":Coupon_Code} }})

def Insert_Data(UserName, UserId, Delivery_Fee, Order_Data, Cart, lan, lng, Service_Money,new_cus,thumbnail_url,use_point,Coupon_Pay,Coupon_Code):
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
                       "Rider": "", "Order_Time": str(str_datetime), 'lan':  lan, 'lng': lng,'new_cus':new_cus,'thumbnail_url':thumbnail_url,
                       'Coupon_Pay':Coupon_Pay,'Coupon_Code':Coupon_Code})
    
    return Order_Code
    

def Insert_Refund_Data(UserName, UserId,Name, BankName, accountName, Refund_Point):
    # z = randrange(0, 900)
    Order_Code = shortuuid.uuid()

    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)

    format = '%Y-%m-%d %H:%M:%S'
    str_datetime = datetime.strftime(datetime_utc2, format)

    Refund_Data.insert_one({"Refund_Code": Order_Code, "UserName": UserName, "UserId": UserId,
                       "Refund_Time": str(str_datetime),'Name':Name,'BankName':BankName,'accountName':accountName,'Refund_Point':Refund_Point})

    return Order_Code

def Insert_CouponTime(지급일자,쿠폰내용,쿠폰번호,유저아이디):
    Coupon_Data.insert_one({"지급일자":지급일자,"쿠폰내용":쿠폰내용,'쿠폰번호':str(쿠폰번호),'소유자':유저아이디})

def Insert_cust(UserName, UserId, phone):

    timezone_kst = timezone(timedelta(hours=9))
    datetime_utc2 = datetime.now(timezone_kst)
    Coupon_Code = shortuuid.uuid()
    format = '%Y-%m-%d %H:%M:%S'
    format_Days = '%Y-%m-%d'
    str_datetime = datetime.strftime(datetime_utc2, format)
    str_Days = datetime.strftime(datetime_utc2, format_Days)

    Insert_CouponTime(str_Days,"First Coupon",Coupon_Code,UserName)

    mycustomer.insert_one(
        {"UserName": UserName, 'UserId': UserId, "address1": "", "address2": "", "phone": phone, "memo": "", 'Point': 0,'Re_Point': 0, 'Start_Time': str_datetime,
        'coupon_List':[{"지급일자":str_Days,"쿠폰내용":"First Coupon","쿠폰번호":Coupon_Code,"쿠폰보유":True}],"First_Coupon":True,"1W_Coupon":True,"1M_Coupon":True,'Last_Order_Time':"",'Order_Total_Count':0})

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





def Edit_Point(UserId, point):
    mycustomer.update_one({"UserId": str(UserId)}, {
        '$inc': {'Point': -int(point)}})

def Add_cus_AddrData(UserId, Ur):
    mycustomer.update_one({"UserId": str(UserId)}, { '$addToSet': { 'AddLists':  Ur} })


def Drop_Users():
    mycustomer.drop()


if __name__ == "__main__":
    # Del_Coupon('ZJwhWPpZp8xhGkyBHv2bxp')
    # xx = Coupon_Data.find({})
    # for i in xx:
    #     print(i)
    # mycustomer.update_many({}, {
    #     '$set': {'Re_Point': 0}})
    v = mycustomer.find({})
    for i in v:
        print(i)