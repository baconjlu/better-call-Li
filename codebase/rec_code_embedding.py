import numpy as np 
import pandas as pd  
import os  
import random 
import json    
from tqdm import tqdm 
from utils.BERT import Bert 
from collections import defaultdict  

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
			return [ _[0] for _ in top_k_items], [ _[1] for _ in top_k_items] 
		
		else:  
			# NO history, direct recommend 
			random_selection = random.sample(item_list, K) 
			return random_selection, [1 for _ in range(K)] 
			
class STORE_RECOMMENDATION_SYSTEM(USER_RECOMMENDATION_SYSTEM): 
	def __init__( self, storage_path = 'datas/storage/user'): 
		
		# 父类调用构造函数
		super().__init__(storage_path = storage_path)  
		
	# 推荐商户

	# 0.5 是一个门槛（ >= 0.5, 号； <= 0.5，差） 
	def recommend_store(self, user_info, store_list, K = 10): 
		# store_list 是一个 list，然后 list 中的每个元素是一个 dict 

		# 此时应该考虑 user-feedback   
		user_storage_path  = os.path.join(self.STORAGE_PATH, user_info['user_id'])  
		user_comment_path = os.path.join(user_storage_path, 'comment.json') 
		history_score = defaultdict(list) 
		if os.path.exists(user_comment_path): 
			with open(user_comment_path, 'r') as f: 
				user_comment = json.load(f)    
			for com in user_comment: 
				for stor in com['store_info']: 
					print(stor['store_name'] )
					history_score[stor['store_name']].append(com['score']) 
			for _ in history_score: 
				history_score[_] = np.mean(history_score[_]) 
		lis_store = [] 
		for store in tqdm(store_list):   
			store_item = store['store_item'] 
			store_name = store['store_name'] 
			sim_values = []     
			rec_items, rec_scores = self.recommend_item(user_info, store_item, K = len(store_item))    
			store_score = np.mean(rec_scores)
			if store_name in history_score: 
				# print(history_score) 
				store_score *= (history_score[store_name] + 0.5)   
			lis_store.append([store, store_score])
		lis_store = sorted(lis_store, key = lambda x : -x[1])      
		return lis_store 

	# 传入用户数据，商铺数据，以及一个打分
	def update_store_feedback(self, user_infos, store_infos, rec_score): 
		user_storage_path  = os.path.join(self.STORAGE_PATH, user_infos['user_id'])  
		if not os.path.exists(user_storage_path):
			os.makedirs(user_storage_path)  
		user_comment_path = os.path.join(user_storage_path, 'comment.json')     
		if os.path.exists(user_comment_path): 
			with open(user_comment_path, 'r') as f: 
				origin_data = json.load(f) 
			# print(f'1-0: {origin_data}')
			new_data = origin_data + [{"user_info": user_infos, "store_info": store_infos, "score": rec_score}]
			# print(f'1-1: {new_data}')	
			with open(user_comment_path, 'w') as f: 
				json.dump(new_data, f) 
			# print(f'1-1: {new_data}')
		else: 
			with open(user_comment_path, 'w') as f: 
				json.dump([{"user_info": user_infos, "store_info": store_infos, "score": rec_score}], f)
			# with open(user_comment_path, 'r') as f: 
				# origin_data = json.load(f) 
			# print(f'2: {origin_data}')
		
			 
# 可以这么做, 如果一个用户对之前推荐的结果不满意，就将这些商店的权重降低 

# 用户反馈   
if __name__ == '__main__':  

	# rec_sys = USER_RECOMMENDATION_SYSTEM() 
	rec_store = STORE_RECOMMENDATION_SYSTEM()  
	store_list = [
		{
			"store_name": "store-1", 
			"store_item": ['apple', 'grape', 'juice', 'milk'] 
		}, 
		{
			"store_name": "store-2", 
			"store_item": ['bannana', 'grape', 'bottle', 'water'] 
		},
		{
			"store_name": "store-3", 
			"store_item": ['cherry', 'peach', 'pencil', 'bear'] 
		},
		{
			"store_name": "store-4", 
			"store_item": ['lipstick', 'blueberry', 'computer', 'car'] 
		}
	]
	rec_store.update_user_info(
		{"user_id": "00121"}, 
		["apple", "juice", "sossage"]
	) 
	rec_store.update_user_info(
		{"user_id": "00121"}, 
		["lettace", "grape", "pear"] 
	)  
	rec_store.update_store_feedback(
		{"user_id": "00121"}, 
		[
			{
				"store_name": "store-1", 
				"store_item": ['apple', 'grape', 'juice', 'milk'] 
			}, 
			{
				"store_name": "store-2", 
				"store_item": ['bannana', 'grape', 'bottle', 'water'] 
			},
		], 
		0.8
	)
	rec_store.update_store_feedback(
		{"user_id": "00121"}, 
		[
			{
				"store_name": "store-1", 
				"store_item": ['apple', 'grape', 'juice', 'milk'] 
			}, 
			{
				"store_name": "store-2", 
				"store_item": ['bannana', 'grape', 'bottle', 'water'] 
			},
		], 
		0.8
	)
	rec_items = rec_store.recommend_item(
		{"user_id": "00121"}, 
		["apple", "grape", "orange", "peach"], 
		K = 3 
	)
	print(rec_items )
	recommended_stores = rec_store.recommend_store({"user_id": "00121"}, store_list)
	for _ in recommended_stores: 
		print(_) 
	# print(rec_store.recommend_store({"user_id": "00121"}, store_list))
	




# python rec_code_embedding.py 