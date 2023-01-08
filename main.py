from Get_yogiyo import *
import json
from DBMaker import *
from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import time
from pydantic import BaseModel
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    date: str
    to: str
    message: str

class refundItem(BaseModel):
    UserName:str
    UserId:str
    Name:str
    BankName:str
    accountName:str

@app.get('/getStores')
async def getStores(category: str = "1인분주문", latitude='37.5347556106622', longitude='127.114906298514', own_delivery_only='false'):

    data = get_Yogiyo(category, latitude, longitude, own_delivery_only)
    return data

@app.post('/refund')
async def PostRefund(data:refundItem):
    Insert_Refund_Data(UserName=data.UserName, UserId=data.UserId,Name=data.Name, BankName=data.BankName, accountName=data.accountName)
    
    return "data"

@app.get('/getAccount')
async def Accoun():

    data = find_Account()

    return data


@app.get('/getMenus')
def getMenus(id="261363"):
    data = get_Menu(id)
    return data

@app.post('/wait-time')
def getMenus(item : Item):
    
    Insert_WaitTime(item.date,item.message)
    return item

@app.get('/getReviews')
def getReviews(id="1048427", count="100", page="1"):
    data = get_Review(id, count, page)
    return data


@app.get('/getItemReviews')
def getR(id="1048427", count="100", page="1", menu_id="314259651"):
    data = getItemReviews(id, page, count, menu_id)

    return data


@app.get('/search')
def Searchs(keyword="피자", page="0", latitude="37.5347556106622", longitude="127.114906298514"):

    data = Search_Category(keyword, page, latitude, longitude)

    return data


@app.get('/popularMenu')
def popularMenu(latitude="37.5347556106622", longitude="127.114906298514"):

    data = Find_Top(latitude, longitude)

    return data

@app.get('/find_Order_Datas')
def find_Order(userId="Ua405f456c424b90f2d3271fac5f723a6"):

    datas = find_Order_Datas(userId)
    return datas

@app.get('/Order_Data')
def find_Orders(Order_Code="d9tQxmYV9LQWe67xaivarm"):

    datas = DB_Order_Data(Order_Code)
    return datas

@app.post('/Add_Address')
def Add_Address(add1="",add2="",phone="",add_Name="",UserName="",UserId=""):

    Insert_Address(add1,add2,phone,add_Name,UserName,UserId)

    return "datas"

@app.post('/pushOrder')
def pushOrder(
        userId="66",
        userName="66",
        new_cus:bool=False,
        delivery_fee="66",
        Service_Money="66",
        ImageIn="66",
        lan=Form(...),
        lng=Form(...),
        use_point=Form(...),
        thumbnail_url=Form(...),
        OrderData=Form(...),
        cart=Form(...),
        image: UploadFile = File(None),
        background_tasks: BackgroundTasks = None
    ):

    datas, Order_Code = Push_Message(userId, userName, delivery_fee,
                                     json.loads(OrderData), json.loads(cart), lan, lng, Service_Money,new_cus = new_cus,thumbnail_url = thumbnail_url,use_point=use_point)
    update_point(userId,use_point)
    if ImageIn == "yes":
        background_tasks.add_task(UpLoad_IMG, image, Order_Code)

    return {'datas':datas,'Order_Code':Order_Code}


def UpLoad_IMG(img: UploadFile, Order_Code):
    IMG_URL = Upload_IMG(img.file.read())
    Edit_Data(Order_Code, IMG_URL)


@app.get('/service')
def Get_service():
    data = find_service()
    return {"Money":data['Money'],"opened":data['opened'],"ment":data['ment']}

@app.post('/LogErr')
def LogErr(Errors=Form(...)):

    Insert_Err(Errors)

    return "Yes"


@app.get('/find_User_Data')
def find_User_Data(User_ID="66"):
    User_Data = find_cust(User_ID)
    if User_Data != None:
        result = int(User_Data["Point"])
    else:
        result = -1
    return result

@app.get('/insert_User')
def In_cust(UserName, UserId, phone = "01000000000"):

    Insert_cust(UserName, UserId, phone)
    
    return "result"

@app.get('/UUName')
def Update_UserName(UserName, UserId):

    Edit_UserN(UserId, UserName,"66")
    
    return "result"

@app.get('/find_User_Data2')
def find_User_Data2(User_ID="66"):
    User_Data = find_cust(User_ID)
    if User_Data != None:
        result = User_Data
    else:

        result = None
    
    return result
