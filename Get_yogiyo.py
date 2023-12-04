import base64
from fastapi import UploadFile
import requests
import json
from Ordersdatas import *
from Make_Datas import *
from DBMaker import *
from AccessToken import *
import cloudscraper
import httpx

def detour(url, headers):
    detour_url = url.replace("www.yogiyo.co.kr", "13.124.124.31")
    while True:
        cnt = 0
        response = httpx.get(detour_url, headers=headers,verify=False)

        if response.is_redirect:
            redirect_url = response.headers['location']
            if cnt > 1:
                redirect_url = redirect_url.replace("13.124.124.31", "52.78.63.81")
                cnt = cnt+1
            detour_url = redirect_url
        else:
            break
            
    return response.json()

def get_Yogiyo(category, lat, lng, own_delivery_only):
    header = {"x-apikey": 'iphoneap',
              "x-apisecret": 'fe5183cc3dea12bd0ce299cf110a75a2'}

    url = f"https://www.yogiyo.co.kr/api/v2/restaurants?category={category}&items=120&lat={lat}&lng={lng}&order=rank&own_delivery_only={own_delivery_only}&order=distance&page=0&search="
    
    return detour(url,header)
    
    
    
def Upload_IMG(image):

    key = 'b22dba8348a705c59d025bfe148ba482'

    url = "https://api.imgbb.com/1/upload"
    payload = {
        'expiration':72000,
        "key": key,
        "image": base64.b64encode(image),
    }
    res = requests.post(url, payload)
    Get_json = res.json()
    return Get_json['data']["url"]


def get_Menu(id):
    
    header = {
            'X-Apikey': 'iphoneap',
            'X-Apisecret': 'fe5183cc3dea12bd0ce299cf110a75a2',
        }

    url = f"https://www.yogiyo.co.kr/api/v1/restaurants/{id}/menu/?additional_discount_per_menu=1&add_liquor_menu=1&add_one_dish_menu=0&add_photo_menu=ios3x&additional_discount_per_menu=1&order_serving_type=delivery&restaurant_id=1182005&slidable_photo_menu=true"
    
    
    return detour(url,header)

def getItemReviews(id, page, count, menu_id):
    url = f"http://fastfood1144.iptime.org/getItemReviews?id={id}&count={count}&page={page}&menu_id={menu_id}"
    response = requests.get(url)
    Get_json = response.json()
    return Get_json


def get_Review(id, count, page):
    url = f"http://fastfood1144.iptime.org/getReviews?id={id}&count={count}&page={page}"
    response = requests.get(url)
    Get_json = response.json()
    return Get_json


def Search_Category(Search, page, lat, lng):
    header = {"x-apikey": 'iphoneap',
              "x-apisecret": 'fe5183cc3dea12bd0ce299cf110a75a2'}

    url = f"https://www.yogiyo.co.kr/api/v1/restaurants-geo/search/?items=120&lat={lat}&lng={lng}&order=rank&page={page}&search={Search}"
    
    return detour(url,header)


def Find_Top(lat, lng):
    url = f"http://fastfood1144.iptime.org/popularMenu?lat={lat}&lng={lng}"
    response = requests.get(url)
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

def update_point(UserId,Usepoint):
    Edit_Point(UserId,Usepoint)

def update_Repoint(UserId,Usepoint):
    Edit_RePoint(UserId,Usepoint)

def Push_Message(UserId, UserName, delivery_fee,origin_fee, OrderData, cart, lan, lng, Service_Money,new_cus,thumbnail_url,use_point,Coupon_Pay,Coupon_Code,use_Repoint):

    Order_Code = Insert_Data(
        UserName, UserId, delivery_fee,origin_fee, OrderData, cart, lan, lng, Service_Money,new_cus,thumbnail_url=thumbnail_url,use_point=use_point,
        Coupon_Pay=Coupon_Pay,Coupon_Code=Coupon_Code,use_Repoint=use_Repoint)

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
                          int(delivery_fee), Order_Code, Service_Money,use_point=use_point,Coupon_Pay=Coupon_Pay,Coupon_Code=Coupon_Code,use_Repoint = use_Repoint)

    return datas['messages'], Order_Code


def template_Test(userId, UserName, Total_pay, deliver_fee, Order_Code, Service_Money,use_point,Coupon_Pay,Coupon_Code,use_Repoint):

    Total_Count = Total_pay + deliver_fee + int(Service_Money)
    datas = Make_DD(userId, Total_pay, deliver_fee,
                    Total_Count, UserName, Order_Code, int(Service_Money),use_point=int(use_point),Coupon_Pay=int(Coupon_Pay),Coupon_Code=Coupon_Code,use_Repoint = use_Repoint)

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

def Upload_CF_IMG(image):
    
    headers = {
    'Authorization': 'Bearer d07tKnBiHPNKTJUtKolp-vA38J4R4E5cf1RWIUpv',
    }

    files = {
        'file': image,
    }

    response = requests.post(
        'https://api.cloudflare.com/client/v4/accounts/aaf9489dd4c9a1c749f15ab1bd7019de/images/v1',
        headers=headers,
        files=files,
    )
    Get_json = response.json()
    
    return Get_json['result']['variants'][0]

if __name__ == "__main__":
    
    # Upload_CF_IMG()
    # print(get_Menu(261363))
    print(get_Yogiyo('1인분주문', '37.5347556106622', '127.114906298514', 'false'))
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
