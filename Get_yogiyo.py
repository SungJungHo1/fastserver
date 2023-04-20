import base64
from importlib.metadata import files
from fastapi import UploadFile
import requests
import json
from Ordersdatas import *
from Make_Datas import *
from DBMaker import *
from AccessToken import *
import cloudscraper
import httpx


def get_Yogiyo(category, lat, lng, own_delivery_only):
    header = {"x-apikey": 'iphoneap',
              "x-apisecret": 'fe5183cc3dea12bd0ce299cf110a75a2'}

    url = f"https://www.yogiyo.co.kr/api/v1/restaurants-geo/?category={category}&items=120&lat={lat}&lng={lng}&order=rank&own_delivery_only={own_delivery_only}&order=distance&page=0&search="
    response = requests.get(url, headers=header)
    Get_json = response.json()
    Get_json['restaurants']
    return Get_json
    
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


# def get_Menu(id):
    
#     header = {
#             'Hackle-Session-Id': '1678847517095.08b248b4',
#             'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2Nzg4NDc1MjEsImV4cCI6MTY3ODg1NDcyMSwicGxhdGZvcm0iOiJZR1kiLCJyb2xlIjoidXNlciIsInN1Yl9pZCI6IjY5NzkzMTI5NCIsImJhc2VfdXJsIjoiaHR0cHM6Ly93d3cueW9naXlvLmNvLmtyIiwidXNlcl9pZCI6IjM1MjE2NzQyIn0.CBRVBE5vj9cAzVPO4KChu9qq2fdII5I7LCn75WsLzgoNNTUMWOwk7fANn6arLCT0eII7a--O6lvfiNkAQfNuiCW9SuKBO-pzFwfdNw14XJftGILtq5o_zvp8Gee4qmGCg5V-V83b1Tw6ZirQ929v5nAsQoyaZX2gpmP8j_cxkIcEw8Lkr9K5HQDLLvnux-MO9Ikxvmwyi7g6L-LUImKL-40S5m7QEBRAVFizt2yvRHfMfPYHPZ2r0vkhJfc1JBn_hAzGb8cRW8posxO-TE0XJ9-3JMyKyCeDFU1zyvBp1EeENJWkBdhanpj2WxYdLbEtTOALml1SGJIqFRDjeUnAoA',
#             'Accept': '*/*',
#             'X-Datadog-Sampling-Priority': '0',
#             'Hackle-Id': '4A6D6F65-E1F7-4432-812C-8B7190DFFB34',
#             'Accept-Encoding': 'gzip, deflate',
#             'Accept-Language': 'ko-KR;q=1.0, en-KR;q=0.9',
#             'X-Apikey': 'iphoneap',
#             'User-Agent':  'iOS/iPhone13,2/16.3.1/yogiyo-ios-7.8.0',
#             'X-Apisecret': 'fe5183cc3dea12bd0ce299cf110a75a2',
#             'X-Datadog-Origin': 'rum'
#         }
#     cookie = {
#             "__cf_bm": "PqhT6j5QvR.MPnPP0CQ1PaUlqXJhHWhjmtEcVJL9dZQ-1678854281-0-AVWPZHm1LH2NSPwTfKmekWH1mABhV7e0ei+aB5D5vsNmoCM+H4SDR0C5QhdMAYJQKsHnly9vFT/g3PzzFXGQwgA=",
#             "optimizelyEndUserId": "oeu1678854281263r0.7429886281832376",
#             "sessionid": "15cd6a6637cbb0dce55f23b95d748c9a",
#             "RestaurantListCookieTrigger": "true",
#             "RestaurantMenuCookieTrigger": "true",
#         }


#     url = f"https://www.yogiyo.co.kr/api/v1/restaurants/{id}/menu/?additional_discount_per_menu=1&add_liquor_menu=1&add_one_dish_menu=0&add_photo_menu=ios3x&additional_discount_per_menu=1&order_serving_type=delivery&restaurant_id=1182005&slidable_photo_menu=true"
#     # while True:
#     #     try:
#     #         scraper = cloudscraper.create_scraper()
#     #         response = scraper.get(url, headers=header, cookies=cookie)
#     #         Get_json = response.json()
#     #         break
#     #     except:
#     #         pass
#     response = httpx.get(url, headers=header,verify=False)
#     Get_json = response.json()
    
#     return Get_json

def get_Menu(id):
    header = {   
        
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Safari Line/13.2.1 LIFF',
        'Accept-Language': 'ko-KR,ko;q=0.9',
        'Referer': f'https://thailovefood.com/menu/{id}',
        }

    url = f"https://www.thailovefood.com/menu_info/{id}"
    url2 = f"http://yogiyofind.ddns.net/getMenus?id={id}"
    url3 = f'http://fastfood1144.iptime.org/getMenus?id={id}'
    # BackUp_Datas = find_BackUp_Datas(id)
    
    # if BackUp_Datas != None:
    #     Get_json = BackUp_Datas
        
    # else:

    try:
        response = requests.get(url3,headers=header,verify=False,timeout=2)
        Get_json = response.json()["data"]
        # data_BackUp(Get_json,id)
    except:

        response = requests.get(url2)
        Get_json = response.json()
        # data_BackUp(Get_json,id)

    return Get_json

# def get_Menu(id):

#     url = f"http://3.39.0.137/getMenus?id={id}"
    
#     response = requests.get(url)
#     Get_json = response.json()

#     return Get_json



# def get_Menu(id):
#     header = {   
        
#         'Cookie': 'PHPSESSID=rh3a3euioieoau71nd72s2q76u',
#         'Accept': '*/*',
#         'Accept-Encoding': 'gzip, deflate',
#         'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Safari Line/13.2.1 LIFF',
#         'Accept-Language': 'ko-KR,ko;q=0.9',
        
#         }

#     url = f"https://youduay.com/datacenter/getajaxfood.php?type=6&sid={id}"
#     try:
#         scraper = cloudscraper.create_scraper()
#         response = scraper.get(url, headers=header)
#         Get_json = response.json()
#         print("정상")
#     except:
        
#         Get_json = find_BackUp_Datas(id)
#         print('에러')

#     return Get_json

# def get_Menu(id):
#     param = {
#         "add_photo_menu": "android",
#         "add_one_dish_menu": "true",
#         "order_serving_type": "delivery",
#     }
#     header = {
#             'Hackle-Session-Id': '1678847517095.08b248b4',
#             'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2Nzg4NDc1MjEsImV4cCI6MTY3ODg1NDcyMSwicGxhdGZvcm0iOiJZR1kiLCJyb2xlIjoidXNlciIsInN1Yl9pZCI6IjY5NzkzMTI5NCIsImJhc2VfdXJsIjoiaHR0cHM6Ly93d3cueW9naXlvLmNvLmtyIiwidXNlcl9pZCI6IjM1MjE2NzQyIn0.CBRVBE5vj9cAzVPO4KChu9qq2fdII5I7LCn75WsLzgoNNTUMWOwk7fANn6arLCT0eII7a--O6lvfiNkAQfNuiCW9SuKBO-pzFwfdNw14XJftGILtq5o_zvp8Gee4qmGCg5V-V83b1Tw6ZirQ929v5nAsQoyaZX2gpmP8j_cxkIcEw8Lkr9K5HQDLLvnux-MO9Ikxvmwyi7g6L-LUImKL-40S5m7QEBRAVFizt2yvRHfMfPYHPZ2r0vkhJfc1JBn_hAzGb8cRW8posxO-TE0XJ9-3JMyKyCeDFU1zyvBp1EeENJWkBdhanpj2WxYdLbEtTOALml1SGJIqFRDjeUnAoA',
#             'Accept': '*/*',
#             'X-Datadog-Sampling-Priority': '0',
#             'Hackle-Id': '4A6D6F65-E1F7-4432-812C-8B7190DFFB34',
#             'Accept-Encoding': 'gzip, deflate',
#             'Accept-Language': 'ko-KR;q=1.0, en-KR;q=0.9',
#             'X-Apikey': 'iphoneap',
#             'User-Agent':  'iOS/iPhone13,2/16.3.1/yogiyo-ios-7.8.0',
#             'X-Apisecret': 'fe5183cc3dea12bd0ce299cf110a75a2',
#             'X-Datadog-Origin': 'rum'
#         }
#     cookie = {
#             "__cf_bm": "PqhT6j5QvR.MPnPP0CQ1PaUlqXJhHWhjmtEcVJL9dZQ-1678854281-0-AVWPZHm1LH2NSPwTfKmekWH1mABhV7e0ei+aB5D5vsNmoCM+H4SDR0C5QhdMAYJQKsHnly9vFT/g3PzzFXGQwgA=",
#             "optimizelyEndUserId": "oeu1678854281263r0.7429886281832376",
#             "sessionid": "15cd6a6637cbb0dce55f23b95d748c9a",
#             "RestaurantListCookieTrigger": "true",
#             "RestaurantMenuCookieTrigger": "true",
#         }
#     response = httpx.get(f"https://www.yogiyo.co.kr/api/v1/restaurants/{id}/menu/", params=param, headers=header, cookies=cookie, verify=False)
#     Get_json = response.json()


#     return Get_json

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

    url = f"https://www.yogiyo.co.kr/api/v1/restaurants-geo/search/?items=120&lat={lat}&lng={lng}&order=rank&page={page}&search={Search}"
    response = requests.get(url, headers=header)
    Get_json = response.json()
    return Get_json


def Find_Top(lat, lng):
    header = {"x-apikey": 'iphoneap',
              "x-apisecret": 'fe5183cc3dea12bd0ce299cf110a75a2'}

    url = f"https://www.yogiyo.co.kr/api/v1/restaurants-geo/?category=전체&items=60&lat={lat}&lng={lng}&sort_order=desc"
    # url = f"https://www.yogiyo.co.kr/api/v1/restaurants-geo/?items=60&lat={lat}&lng={lng}&order=review_avg&page=0&search="
    response = requests.get(url, headers=header)
    Get_json = response.json()
    if 'restaurants' in Get_json:
        Return_Data = {'restaurants':Get_json['restaurants'][0:15]}
    else :
        Return_Data = {'restaurants': []}
    return Return_Data


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

def Push_Message(UserId, UserName, delivery_fee, OrderData, cart, lan, lng, Service_Money,new_cus,thumbnail_url,use_point,Coupon_Pay,Coupon_Code,use_Repoint):

    Order_Code = Insert_Data(
        UserName, UserId, delivery_fee, OrderData, cart, lan, lng, Service_Money,new_cus,thumbnail_url=thumbnail_url,use_point=use_point,
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
    print(get_Menu(261363))
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
