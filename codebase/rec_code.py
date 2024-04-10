import numpy as np 
import pandas as pd  
import os  
import random 
import json 
import gensim.downloader as api
from gensim.models import Word2Vec 

class USER_RECOMMENDATION_SYSTEM:

	def __init__(self, 
		storage_path = 'datas/storage/user',
	): 
		
		# 用户存储
		self.STORAGE_PATH = storage_path 
		os.makedirs(self.STORAGE_PATH, exist_ok = True) 

		# NLP 存储 
		self.NLP_SIM_PATH = 'datas/storage/NLP/similarity/word2vec_google_news_model.bin' 
		if os.path.exists(self.NLP_SIM_PATH): 
			self.w2v_model = Word2Vec(self.NLP_SIM_PATH) 
		else: 
			os.makedirs(os.path.dirname(self.NLP_SIM_PATH), exist_ok = True)  
			self.w2v_model = api.load('word2vec-google-news-300')   
			self.w2v_model
		

	
	def get_user_history_path(self, user_id): 
		user_storage_path = os.path.join(self.STORAGE_PATH, user_id) 
		user_shoplist_info = os.path.join(user_storage_path, 'shoplist_info.json')    
		return user_shoplist_info 

	def update_user_info(self, user_infos, shop_list): 
		user_storage_path  = os.path.join(self.STORAGE_PATH, user_infos['user_id'])  
		user_shoplist_info = os.path.join(user_storage_path, 'shoplist_info.json')   
		os.makedirs(user_storage_path, exist_ok = True) 
		if os.path.exists(user_shoplist_info): 
			with open(user_shoplist_info, 'r') as f: 
				data = json.load(f)  
			data.append({"shop_list": shop_list}) 
			with open(user_shoplist_info, 'w') as f: 
				json.dump(data, f) 
		else:
			with open(user_shoplist_info, 'w') as f:  
				json.dump([{"shop_list": shop_list}], f) 
		
	# recommend K items from item_list 
	def recommend_item(self, user_infos, item_list, K = 10): 
		K = min(K, len(item_list)) 
		user_history_file = self.get_user_history_path(user_infos['user_id'])
		if os.path.exists(user_history_file): 
			with open(user_history_file) as f: 
				history_data = json.load(f) 
			full_data = []
			for _ in history_data: 
				full_data.append(_)      
			
			
		else:  
			# NO history, direct recommend 
			random_selection = random.sample(item_list, K)  
			return random_selection  
			
		


if __name__ == '__main__':  
	w2v_model = api.load('word2vec-google  -news-300')

	rec_sys = USER_RECOMMENDATION_SYSTEM() 
	rec_sys.update_user_info(
		{"user_id": "00121"}, 
		["apple", "juice", "sossage"]
	) 
