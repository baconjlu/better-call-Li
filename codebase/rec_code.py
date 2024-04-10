import numpy as np 
import pandas as pd  
import os  
import random 
import json    
from utils.BERT import Bert 

class USER_RECOMMENDATION_SYSTEM:

	def __init__(self, 
		storage_path = 'datas/storage/user',
	): 
		
		# 用户存储
		self.STORAGE_PATH = storage_path 
		os.makedirs(self.STORAGE_PATH, exist_ok = True) 


		# NLP 存储 
		self.BERT_PATH = 'utils/weights/bert-base-uncased' 
		self.bert_model = Bert(self.BERT_PATH) 
		
	def query_word_similarity(self, word1, word2): 
		calc_sim = self.bert_model.getTextSim(word1, word2, 0) 
		return calc_sim[1] 

	
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
	
	def select_top_K(self, user_history, item_list, K): 
		score_list = [] 
		for _item in item_list: 
			MAXIMUM_SIM = -1
			for j in user_history: 
				MAXIMUM_SIM = max(MAXIMUM_SIM, self.query_word_similarity(_item, j)) 
			score_list.append((_item, MAXIMUM_SIM))
		score_list = sorted(score_list, key = lambda x : -x[1])
		return score_list[:K]  

	# recommend K items from item_list 
	def recommend_item(self, user_infos, item_list, K = 10): 
		K = min(K, len(item_list)) 
		user_history_file = self.get_user_history_path(user_infos['user_id'])
		if os.path.exists(user_history_file): 
			with open(user_history_file) as f: 
				history_data = json.load(f) 
			full_data = []
			for _ in history_data: 
				full_data += _['shop_list']
			top_k_items = self.select_top_K(full_data, item_list, K) 
			return [ _[0] for _ in top_k_items]
		
		else:  
			# NO history, direct recommend 
			random_selection = random.sample(item_list, K)  
			return random_selection  
			
		


if __name__ == '__main__':  

	rec_sys = USER_RECOMMENDATION_SYSTEM() 
	# rec_sys.update_user_info(
	# 	{"user_id": "00121"}, 
	# 	["apple", "juice", "sossage"]
	# ) 
	# rec_sys.update_user_info(
	# 	{"user_id": "00121"}, 
	# 	["lettace", "grape", "pear"] 
	# )  
 
	rec_sys.recommend_item({"user_id": "00121"}, ['bannana', 'pen', 'paper', 'soda'], K = 2) 

