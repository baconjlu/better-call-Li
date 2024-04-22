import numpy as np 
import pandas as pd  
import os  
import random 
import json    
from tqdm import tqdm 
from utils.BERT import Bert 
from collections import defaultdict  
from sklearn.tree import DecisionTreeClassifier
import pickle 
class USER_RECOMMENDATION_SYSTEM:

	def __init__(self, 
		storage_path = 'datas/storage/user',
		device = 'cuda:0', 
		embedding_storage_path = 'data/storage/embedding'
	): 
		
		# 用户存储
		self.STORE_STORAGE_PATH = 'datas/storage/store' 
		self.STORAGE_PATH = storage_path 
		self.embedding_storage_path = embedding_storage_path 
		os.makedirs(self.STORAGE_PATH, exist_ok = True) 


		# NLP 存储 
		self.BERT_PATH = 'utils/weights/bert-base-uncased' 
		self.bert_model = Bert(self.BERT_PATH, device) 
	
	def get_word_embedding(self, q_word): 
		return self.bert_model.getEmb(q_word).detach().cpu().numpy()
	
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
	def __init__(self, 
		storage_path = 'datas/storage/user', 
		device = 'cuda:0', 
		embdding_storage_path = 'data/storage/embeddings', 
		classifier_name = 'decision_tree' 
	): 
		
		# 父类调用构造函数
		super().__init__(
			storage_path = storage_path, 
			device = device, 
			embedding_storage_path = embdding_storage_path
		)  
		
	# 推荐商户

	# 0.5 是一个门槛（ >= 0.5, 号； <= 0.5，差） 
	# def recommend_store(self, user_info, store_list, K = 10): 
	# 	# store_list 是一个 list，然后 list 中的每个元素是一个 dict 

	# 	# 此时应该考虑 user-feedback   
	# 	user_storage_path  = os.path.join(self.STORAGE_PATH, user_info['user_id'])  
	# 	user_comment_path = os.path.join(user_storage_path, 'comment.json') 
	# 	history_score = defaultdict(list) 
	# 	if os.path.exists(user_comment_path): 
	# 		with open(user_comment_path, 'r') as f: 
	# 			user_comment = json.load(f)    
	# 		for com in user_comment: 
	# 			for stor in com['store_info']: 
	# 				# print(stor['store_name'] )
	# 				history_score[stor['store_name']].append(com['score']) 
	# 		for _ in history_score: 
	# 			history_score[_] = np.mean(history_score[_]) 
	# 	lis_store = [] 
	# 	for store in tqdm(store_list):   
	# 		store_item = store['store_item'] 
	# 		store_name = store['store_name'] 
	# 		sim_values = []     
	# 		rec_items, rec_scores = self.recommend_item(user_info, store_item, K = len(store_item))    
	# 		store_score = np.mean(rec_scores)
	# 		if store_name in history_score: 
	# 			# print(history_score) 
	# 			store_score *= (history_score[store_name] + 0.5)   
	# 		lis_store.append([store, store_score])
	# 	lis_store = sorted(lis_store, key = lambda x : -x[1])      
	# 	return lis_store 


	def recommend_store(self, user_infos, store_list): 
		user_storage_path  = os.path.join(self.STORAGE_PATH, user_infos['user_id'])    
		if not os.path.exists(user_storage_path):
			# 没有，那就随机推荐就行 
			return store_list 
		else: 
			rec_list = [] 
			for _store in store_list: 
				store_storage_path = os.path.join(self.STORE_STORAGE_PATH, _store) 
				store_storage_file = os.path.join(store_storage_path, 'store_info.json') 
				with open(store_storage_file, 'r') as f: 
					store_items = json.load(f)['store_item'] 
				
				# classify_user_preference
				ave_score = []
				for _item in store_items:   
					ave_score.append(self.classify_user_preference(user_infos, _item))
				rec_list.append([_store, np.mean(ave_score)]) 
			return rec_list

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

	# 可一个更新商店的信息
	def update_store_info(self, store_info): 
		store_storage_path = os.path.join(self.STORE_STORAGE_PATH, store_info['store_name']) 
		if not os.path.exists(store_storage_path): 
			os.makedirs(store_storage_path) 
			store_storage_file = os.path.join(store_storage_path, 'store_info.json') 
			with open(store_storage_file, 'w') as f: 
				json.dump(store_info, f)
		else:      
			return 

	def update_user_store_preference(self, user_infos, store_name, score): 
		store_storage_path = os.path.join(self.STORE_STORAGE_PATH, store_name) 
		if os.path.exists(store_storage_path): 
			# 此时会更新对于这个商铺的偏好 
			store_storage_file = os.path.join(store_storage_path, 'store_info.json')   
			with open(store_storage_file, 'r') as f: 
				store_data = json.load(f) 

			if 'score' in store_data: 
				store_data['score'].append(score) 
			else: 
				store_data['score'] = [score]
			
			with open(store_storage_file, 'w') as f: 
				json.dump(store_data, f) 

			with open(store_storage_file, 'r') as f: 
				store_items = json.load(f)['store_item'] 
			user_preference = [] 
			for _item in store_items: 
				user_preference.append((_item, score)) 
			self.update_user_item_preference(user_infos, user_preference) 

	def update_user_item_preference(self, user_infos, user_preference):  
		user_storage_path  = os.path.join(self.STORAGE_PATH, user_infos['user_id'])    
		if not os.path.exists(user_storage_path):
			os.makedirs(user_storage_path)  
		user_comment_path = os.path.join(user_storage_path, 'item_preference.json')     
		if os.path.exists(user_comment_path): 
			with open(user_comment_path, 'r') as f: 
				origin_data = json.load(f)    
			for _ in user_preference: 
				if _[0] in origin_data: 
					origin_data[_[0]].append(_[1])
				else: 
					origin_data[_[0]] = [_[1]] 
			with open(user_comment_path, 'w') as f: 
				json.dump(origin_data, f)  
			# print(f'1-1: {new_data}')
		else: 
			item_score_dict = defaultdict(list)  
			for _ in user_preference: 
				item_score_dict[_[0]].append(_[1]) 
			with open(user_comment_path, 'w') as f:    
				json.dump(item_score_dict, f)   
		self.flush_user_preference(user_infos)
	
	def classify_user_preference(self, user_infos, _item): 
		user_storage_path  = os.path.join(self.STORAGE_PATH, user_infos['user_id'])   
		user_classifier_path = os.path.join(user_storage_path, 'classifier.pkl')    
		if os.path.exists(user_classifier_path): 
			with open(user_classifier_path, 'rb') as f: 
				dec = pickle.load(f) 
			return dec.predict(self.get_word_embedding(_item))
		else: 
			return None 

	def flush_user_preference(self, user_infos): 
		user_storage_path  = os.path.join(self.STORAGE_PATH, user_infos['user_id'])   
		user_classifier_path = os.path.join(user_storage_path, 'classifier.pkl')    
		user_comment_path = os.path.join(user_storage_path, 'item_preference.json')        
		with open(user_comment_path, 'r') as f: 
			data = json.load(f) 
		# 用决策树进行拟合的时候，一行一个样本
		X_matrix = [] 
		Y_matrix = [] 
		for _ in data: 
			X_matrix.append(np.squeeze(self.get_word_embedding(_), axis = 0))   
			Y_matrix.append(int(np.mean(data[_])))
		X_matrix = np.array(X_matrix) 
		Y_matrix = np.array(Y_matrix)
		dec = DecisionTreeClassifier()
		dec.fit(X_matrix, Y_matrix)  
		with open(user_classifier_path, 'wb') as f: 
			pickle.dump(dec, f) 

# 可以这么做, 如果一个用户对之前推荐的结果不满意，就将这些商店的权重降低 

# 用户反馈   

# python rec_code_embedding.py 
if __name__ == '__main__':  
	rec_store = STORE_RECOMMENDATION_SYSTEM(
		storage_path = 'datas/storage/user', 
		device = 'cuda:0', 
		embdding_storage_path = 'data/storage/embeddings', 
		classifier_name = 'decision_tree'
	)  

	# 对于用户 preference，可以个性化存储 
	rec_store.update_user_item_preference(
		{"user_id": "00121"}, 
		[("apple", 8), ("orange", 8), ("juice", 3), ("car", 2), ("grape", 9)] 
	)
	rec_store.update_user_item_preference(
		{"user_id": "00121"}, 
		[("computer", 2), ("apple", 8), ("bycicle", 3), ("car", 2), ("grape", 9)] 
	)  

	# 存储商店信息
	rec_store.update_store_info(
		{
			"store_name": "store-1", 
			"store_item": ['apple', 'grape', 'juice', 'milk'] 
		}
	)
	rec_store.update_store_info(
		{
			"store_name": "store-2", 
			"store_item": ['car', 'bycicle', 'pants', 'soccer'] 
		}
	)
	rec_store.update_store_info(
		{
			"store_name": "store-3", 
			"store_item": ['dvd', 'mp3', 'ipad', 'computer'] 
		}
	)
	
	# 存储每个用户对于商店中商品的偏好 
	rec_store.update_user_store_preference({"user_id": "00121"}, "store-1", 7)
	rec_store.update_user_store_preference({"user_id": "00121"}, "store-2", 3)
	rec_store.update_user_store_preference({"user_id": "00121"}, "store-3", 4)   


	# 新来了两个店铺 
	rec_store.update_store_info(
		{
			"store_name": "store-4", 
			"store_item": ['fruit', 'cherry', 'peach', 'lime', 'papaya'] 
		}
	)
	rec_store.update_store_info(
		{
			"store_name": "store-5", 
			"store_item": ['uniform', 'wardrobe', 'clothing', 'overalls', 'tailcoat'] 
		}
	)
	for _ in tqdm(range(100)): 
		rec_result = rec_store.recommend_store(
			{"user_id": "00121"}, ["store-4", "store-5"] 
		)
		print(_, rec_result) # [['store-4', 6.0], ['store-5', 4.0]] 	
	# python rec_code_embedding.py 