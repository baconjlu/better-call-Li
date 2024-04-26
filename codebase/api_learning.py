from flask import Flask,request,jsonify
# from rec_code_embedding import STORE_RECOMMENDATION_SYSTEM
# from rec_code_embedding import USER_RECOMMENDATION_SYSTEM
import sys
import requests
# from utils.preprocess_input import get_feedback_to_store, get_store_information, get_user_information

import json

with open('utils/test_files/Functional-Test/2/S.json','rb') as file:
    sdata=json.load(file)

with open('utils/test_files/Functional-Test/2/UwIn.json','rb') as file:
    udata=json.load(file)

data = {'store':sdata,'user':udata}
json_data=json.dumps(data)
# url = 'http://192.168.215.11:5000/require_recommendation'
# url = 'http://connect.neimeng.seetacloud.com:6006/require_recommendation'
url = 'https://u10536-9aae-47f62ca6.neimeng.seetacloud.com:6443/require_recommendation'
headers={'Content-Type':'application/json'}

response = requests.post(url,json=json_data,headers=headers)
print(response.text)