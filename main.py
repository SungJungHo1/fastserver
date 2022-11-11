from Get_yogiyo import *
import json
from DBMaker import *
from fastapi import FastAPI, File, Form, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import time
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/getStores')
async def getStores(category: str = "1인분주문", latitude='37.5347556106622', longitude='127.114906298514', own_delivery_only='false'):

    data = get_Yogiyo(category, latitude, longitude, own_delivery_only)

    return data


@app.get('/getMenus')
def getMenus(id="261363"):
    data = get_Menu(id)
    return data


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


@app.post('/pushOrder')
def pushOrder(userId="66", userName="66", delivery_fee="66", Service_Money="66", ImageIn="66", lan=Form(...), lng=Form(...), OrderData=Form(...), cart=Form(...), image: UploadFile = File(None), background_tasks: BackgroundTasks = None):

    datas, Order_Code = Push_Message(userId, userName, delivery_fee,
                                     json.loads(OrderData), json.loads(cart), lan, lng, Service_Money)
    if ImageIn == "yes":
        background_tasks.add_task(UpLoad_IMG, image, Order_Code)

    return datas


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
