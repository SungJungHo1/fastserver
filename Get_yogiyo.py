import base64
from importlib.metadata import files
import requests
import json
from Ordersdatas import *
from Make_Datas import *
from DBMaker import *
from AccessToken import *


def get_Yogiyo(category, lat, lng, own_delivery_only):
    header = {"x-apikey": 'iphoneap',
              "x-apisecret": 'fe5183cc3dea12bd0ce299cf110a75a2'}

    url = f"https://www.yogiyo.co.kr/api/v1/restaurants-geo/?category={category}&items=60&lat={lat}&lng={lng}&order=rank&own_delivery_only={own_delivery_only}&page=0&search="
    response = requests.get(url, headers=header)
    Get_json = response.json()
    Get_json['restaurants'].sort(key=lambda x: (-x['additional_discount'],-x['discount_percent']))
    return Get_json


def Upload_IMG(image):

    key = 'b22dba8348a705c59d025bfe148ba482'

    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": key,
        "image": base64.b64encode(image),
    }
    res = requests.post(url, payload)
    Get_json = res.json()

    return Get_json['data']["url"]


def get_Menu(id):
    header = {"x-apikey": 'iphoneap',
              "x-apisecret": 'fe5183cc3dea12bd0ce299cf110a75a2'}

    url = f"https://www.yogiyo.co.kr/api/v1/restaurants/{id}/menu/?add_photo_menu=android&add_one_dish_menu=true&order_serving_type=delivery"
    response = requests.get(url, headers=header)
    Get_json = response.json()
    return Get_json


def getItemReviews(id, page, count, menu_id):
    header = {"x-apikey": 'iphoneap',
              "x-apisecret": 'fe5183cc3dea12bd0ce299cf110a75a2'}
    url = f"https://www.yogiyo.co.kr/api/v1/reviews/{id}/?page={page}&count={count}&sort=time&type=&sort_order=desc&menu_id={menu_id}"
    response = requests.get(url, headers=header)
    Get_json = response.json()
    return Get_json


def get_Review(id, count, page):
    header = {"x-apikey": 'iphoneap',
              "x-apisecret": 'fe5183cc3dea12bd0ce299cf110a75a2'}
    url = f"https://www.yogiyo.co.kr/api/v1/reviews/{id}/?count={count}&only_photo_review=false&page={page}&sort=time"
    response = requests.get(url, headers=header)
    Get_json = response.json()
    return Get_json


def Search_Category(Search, page, lat, lng):
    header = {"x-apikey": 'iphoneap',
              "x-apisecret": 'fe5183cc3dea12bd0ce299cf110a75a2'}

    url = f"https://www.yogiyo.co.kr/api/v1/restaurants-geo/search/?items=60&lat={lat}&lng={lng}&order=rank&page={page}&search={Search}"
    response = requests.get(url, headers=header)
    Get_json = response.json()
    return Get_json


def Find_Top(lat, lng):
    header = {"x-apikey": 'iphoneap',
              "x-apisecret": 'fe5183cc3dea12bd0ce299cf110a75a2'}

    url = f"https://www.yogiyo.co.kr/api/v1/restaurants-geo/?items=60&lat={lat}&lng={lng}&order=review_avg&page=0&search="
    response = requests.get(url, headers=header)
    Get_json = response.json()
    return Get_json


def Find_User_Profile(UserId):
    Line_tokens = f"Bearer {Access_Token}"
    header = {
        "Authorization": Line_tokens
    }
    url = f"https://api.line.me/v2/bot/profile/{UserId}"
    response = requests.get(url, headers=header)
    Get_json = response.json()
    return Get_json


def Push_Message(UserId, UserName, delivery_fee, OrderData, cart, lan, lng, Service_Money):

    Order_Code = Insert_Data(
        UserName, UserId, delivery_fee, OrderData, cart, lan, lng, Service_Money)

    options_fee = 0
    totals = 0
    Menu_Data = []
    for i in cart:
        menu = i['menu']

        if (len(i['options']) == 0):
            MDs = Set_Dics(menu, i)
            Make_dics(Menu_Data, MDs)
            totals = totals + i['totalPrice']
        else:
            MDs = Set_Dics(menu, i)
            Make_dics(Menu_Data, MDs)
            totals = totals + i['totalPrice']
            for x in i['options']:
                Option_Data = Set_Options(x)
                Make_dics(Menu_Data, Option_Data)
                options_fee = options_fee + x['subOptionPrice']

    datas = template_Test(UserId, UserName, int(totals),
                          int(delivery_fee), Order_Code, Service_Money)

    return datas['messages'], Order_Code


def template_Test(userId, UserName, Total_pay, deliver_fee, Order_Code, Service_Money):

    Total_Count = Total_pay + deliver_fee + int(Service_Money)
    datas = Make_DD(userId, Total_pay, deliver_fee,
                    Total_Count, UserName, Order_Code, int(Service_Money))

    return datas


def IMG_Test(UserId, file_Name):
    Line_tokens = f"Bearer {Access_Token}"

    header = {
        "Authorization": Line_tokens,
        "Content-Type": "application/json"

    }
    datas = {
        "to": UserId,
        "messages": [
            {
                "type": "image",
                "originalContentUrl": file_Name,
                "previewImageUrl": file_Name,
            }
        ]
    }

    url = f"https://api.line.me/v2/bot/message/push"
    response = requests.post(url, headers=header, data=json.dumps(datas))
    Get_json = response.json()
    return Get_json


if __name__ == "__main__":
    rt = get_Yogiyo("전체",37.5347556106622,127.114906298514,False)
    
    print(rt)
    # delivery_fee = 3000
    # datas = Push_Message("U812329a68632f4237dea561c6ba1d413",
    #                      '크턱', 3000, orderdata, cart2, 1010100, 10101010, 3000)
    # print(datas)
    # print(data)
    # print(get_Menu(351360))
    # print(data)
    # IMG_Test("Uad859360a7e2589c8c213b3b47fc27a2")
    # get_Menu()
    # get_Menu(1109037)
