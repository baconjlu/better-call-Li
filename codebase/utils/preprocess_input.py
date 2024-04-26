import numpy as np 
import json 
import pickle 
from collections import defaultdict 

def get_feedback_to_item(path): 
    with open(path, 'r') as f: 
        data = json.load(f)
    return_list = defaultdict(list) 
    for _info in data: 
        # print(_info) 
        item_name = str(_info['Feedback']['Item']['ItemName']).lower() 
        if 'itemCategory' in _info: 
            item_name = str(_info['itemCategory']).lower() 
        return_list[str(_info['Feedback']['UserId'])].append((item_name, _info['Feedback']['rating'])) 
    return return_list 

def get_feedback_to_store(path): 
    with open(path, 'r') as f: 
        data = json.load(f) 
    data = data["Feedback"]
    rating = data["rating"] 
    user_id = data["UserId"] 
    store_info = data["Item"]
    item_infos = store_info["items"] 
    item_list = [] 
    for _ in item_infos: 
        item_list.append(str(_["itemCategory"]).lower())
    store_dict = {
        "store_name" : str(store_info["storeId"]), 
        "store_item" : list(set(item_list))
    }
    user_info  = {
        "user_id" : str(user_id)
    } 
    return store_dict, user_info, rating 


def get_store_information(path): 
    with open(path, 'r') as f: 
        original_data = json.load(f) 
    store_list = [] 
    store_data = original_data['Stores'] 
    for _store in store_data: 
        store_name = str(_store['storeId']) 
        store_item = _store['items'] 
        item_list = [] 
        for _item in store_item: 
            if 'category' in _item:
                item_list.append(str(_item['category']).lower()) 
            else: 
                item_list.append(str(_item['itemName']).lower()) 
        store_list.append({"store_name": store_name, "store_item": list(set(item_list))})   
    return store_list

def get_user_information(path): 
    with open(path, 'r') as f: 
        origin_data = json.load(f) 
    user_interest = origin_data["UserData"]["Interests"] 
    user_interest = [str(_).lower() for _ in user_interest] 
    return {"user_id": str(origin_data["UserData"]["UserId"]), "user_preference": user_interest} 

if __name__ == '__main__': 
    # path = 'test_files/Functional-Test/3/.json' 
    path_f2s = [
        'test_files/Functional-Test/3/F2S-0.json' , 
        'test_files/Functional-Test/3/F2S-1.json' , 
        'test_files/Functional-Test/3/F2S-2.json' , 
        'test_files/Functional-Test/3/F2S-3.json' , 
    ]
    for i in range(len(path_f2s)): 
        data = get_feedback_to_store(path_f2s[i]) 
        print(data) 
    pass 