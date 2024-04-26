import time 
import sys 
import numpy as np 
import pandas as pd  
import os  
import random 
import json    
from tqdm import tqdm 
from utils.BERT import Bert 
from collections import defaultdict  
import shutil 
from sklearn.tree import DecisionTreeClassifier
import pickle 
from utils.preprocess_input import get_feedback_to_store, get_store_information, get_user_information
from utils.preprocess_input import get_feedback_to_item

# 设计一个新策略：如果 feedback 的 > 7，则算法 preference 

# 
MLTHRESHOLD = 30
LIKE_LIMIT = 7 
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
	
	# 一个用户的偏好清单
	def update_user_preference_tag(self, user_infos, preference_tag): 
		if len(preference_tag) == 0: 
			return 
		user_storage_path  = os.path.join(self.STORAGE_PATH, user_infos['user_id'])    
		user_preference_tag_path = os.path.join(user_storage_path, 'preference_tag.json')  
		print(user_preference_tag_path) 
		if not os.path.exists(user_storage_path):
			os.makedirs(user_storage_path)  
			with open(user_preference_tag_path, 'w') as f: 
				json.dump({'tag': preference_tag}, f) 
		else: 
			if os.path.exists(user_preference_tag_path):
				with open(user_preference_tag_path, 'r') as f: 
					current_data = json.load(f)  
				current_data['tag'] += preference_tag  
			else: 
				current_data = {} 
				current_data['tag'] = preference_tag
			# 去重 
			current_data['tag'] = list(set(current_data['tag']))
			with open(user_preference_tag_path, 'w') as f: 
				json.dump(current_data, f) 


	# 返回一个 list, list 中每个元素是二元组 (store, store_score) 
	def recommend_store_by_user_preference_tag(self, user_infos, store_list): 
		user_storage_path  = os.path.join(self.STORAGE_PATH, user_infos['user_id'])    
		user_preference_tag_path = os.path.join(user_storage_path, 'preference_tag.json')

		# 不存在 preference tag，直接返回 0 分 
		if not os.path.exists(user_preference_tag_path):
			# 不存在, 直接返回 
			return_lis = [] 
			for _ in store_list: 
				return_lis.append((_, 0)) 
			return return_lis 
		else: 
			# 存在, 可以根据这个粗略进行推荐 
			with open(user_preference_tag_path, 'r') as f: 
				preference_tags = json.load(f) 
			# tag 
			store_scores = defaultdict(list) 
			
			# 应该是一个 store 对每个单词维护一个 max 

			for _store in store_list: 
				store_storage_path = os.path.join(self.STORE_STORAGE_PATH, _store) 
				store_storage_file = os.path.join(store_storage_path, 'store_info.json') 
				with open(store_storage_file, 'r') as f: 
					store_items = json.load(f)['store_item']     
				# 现在获得该商店的所有商品了 
				max_values = [] 
				for _word in preference_tags['tag']: 
					max_value = 0 
					for _item in store_items: 
						cur_score = self.bert_model.getTextSim(_word, _item) 
						max_value = max(max_value, cur_score) 
					max_values.append(max_value) 
				store_scores[_store] = np.mean(max_values) 


			# for _word in preference_tags['tag']: 
			# 	# _word 是偏好单词 
			# 	for _store in store_list: 
			# 		store_storage_path = os.path.join(self.STORE_STORAGE_PATH, _store) 
			# 		store_storage_file = os.path.join(store_storage_path, 'store_info.json') 
			# 		with open(store_storage_file, 'r') as f: 
			# 			store_items = json.load(f)['store_item']     
			# 		# 计算 store_items 和这个 _word 的 embedding 相似度 (平均)
			# 		ave_score = []
			# 		for _item in store_items:
			# 			cur_score = self.bert_model.getTextSim(_word, _item)
			# 			ave_score.append(cur_score) 
			# 		store_scores[_store].append(np.mean(ave_score)) 
			# for _ in store_scores: 
			# 	store_scores[_] = np.mean(store_scores[_]) 
			return_lis = [] 
			for _ in store_scores: 
				return_lis.append((_, store_scores[_])) 
			return return_lis		

	# 推荐物品 
	def recommend_item_by_user_preference_tag(self, user_infos, item_list): 
		user_storage_path  = os.path.join(self.STORAGE_PATH, user_infos['user_id'])    
		user_preference_tag_path = os.path.join(user_storage_path, 'preference_tag.json')
		if not os.path.exists(user_preference_tag_path):
			# 不存在, 直接返回 
			return_lis = [] 
			for _ in item_list: 
				return_lis.append((_, 0)) 
			return return_lis   
		else: 
			# 存在, 可以根据这个粗略进行推荐 
			with open(user_preference_tag_path, 'r') as f: 
				preference_tags = json.load(f) 
			# tag 
			item_scores = defaultdict(list) 
			
			# _word 是偏好单词 
			for _item in item_list:
				ave_score = []
				for _word in preference_tags['tag']: 
					cur_score = self.bert_model.getTextSim(_word, _item)
					ave_score.append(cur_score) 
				item_scores[_item].append(np.mean(ave_score)) 
			for _ in item_scores: 
				item_scores[_] = np.mean(item_scores[_]) 
			return_lis = [] 
			for _ in item_scores: 
				return_lis.append((_, item_scores[_])) 
			return return_lis	   
	
	# 返回的是 [store_name, 分数] (综合推荐商店)
	# 这个要综合上 preference 那个 
	def recommend_store(self, user_infos, store_list): 
		user_storage_path  = os.path.join(self.STORAGE_PATH, user_infos['user_id']) 

		print(self.get_user_item_preference_number(user_infos), MLTHRESHOLD)


		# print(self.get_user_item_preference_number(user_infos)) 
		# print(self.get_user_item_preference_number(user_infos))
		if not os.path.exists(user_storage_path):
			# 没有用户信息，那就随机推荐就行 
			return_lis = [] 
			for _ in store_list: 
				return_lis.append((_, 0)) 
			return return_lis     
		elif self.get_user_item_preference_number(user_infos) >= MLTHRESHOLD: 
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
		else: 
			return self.recommend_store_by_user_preference_tag(user_infos, store_list) 

	# 传入用户数据，商铺数据，以及一个打分   
	# def update_store_feedback(self, user_infos, store_infos, rec_score): 
	# 	user_storage_path  = os.path.join(self.STORAGE_PATH, user_infos['user_id'])  
	# 	if not os.path.exists(user_storage_path):
	# 		os.makedirs(user_storage_path)  
	# 	user_comment_path = os.path.join(user_storage_path, 'comment.json')       

	# 	# user_comment_path: 
	# 	if os.path.exists(user_comment_path): 
	# 		with open(user_comment_path, 'r') as f: 
	# 			origin_data = json.load(f) 
	# 		# print(f'1-0: {origin_data}')
	# 		new_data = origin_data + [{"user_info": user_infos, "store_info": store_infos, "score": rec_score}]
	# 		# print(f'1-1: {new_data}')	
	# 		with open(user_comment_path, 'w') as f: 
	# 			json.dump(new_data, f) 
	# 		# print(f'1-1: {new_data}')
	# 	else: 
	# 		with open(user_comment_path, 'w') as f: 
	# 			json.dump([{"user_info": user_infos, "store_info": store_infos, "score": rec_score}], f)


	# 可一个更新商店的信息 
	# 可覆盖 
	def update_store_info(self, store_info): 
		store_storage_path = os.path.join(self.STORE_STORAGE_PATH, store_info['store_name']) 
		if not os.path.exists(store_storage_path): 
			os.makedirs(store_storage_path) 
		store_storage_file = os.path.join(store_storage_path, 'store_info.json') 
		with open(store_storage_file, 'w') as f: 
			json.dump(store_info, f)

	def update_user_store_preference(self, user_infos, store_name, score): 
		store_storage_path = os.path.join(self.STORE_STORAGE_PATH, store_name) 
		if os.path.exists(store_storage_path): 
			# 此时会更新对于这个商铺的偏好 
			store_storage_file = os.path.join(store_storage_path, 'store_info.json')   
			with open(store_storage_file, 'r') as f: 
				store_items = json.load(f)['store_item'] 
			user_preference = [] 
			for _item in store_items: 
				user_preference.append((_item, score)) 
			self.update_user_item_preference(user_infos, user_preference) 

				
	def get_user_item_preference_number(self, user_infos): 
		user_storage_path  = os.path.join(self.STORAGE_PATH, user_infos['user_id'])    
		user_comment_path = os.path.join(user_storage_path, 'item_preference.json')        
		if not os.path.exists(user_comment_path):
			return 0 
		else: 
			with open(user_comment_path, 'r') as f: 
				return len(json.load(f)) 
	
	def get_user_item_preference(self, user_infos): 
		user_storage_path  = os.path.join(self.STORAGE_PATH, user_infos['user_id'])   
		user_comment_path = os.path.join(user_storage_path, 'item_preference.json')   
		if os.path.exists(user_comment_path):      
			with open(user_comment_path, 'r') as f: 
				data = json.load(f)  
			for _ in data: 
				data[_] = np.mean(data[_])   
			return data 
		else: 
			return None 


	def update_user_item_preference(self, user_infos, user_preference):  
		# update_user_preference_tag 

		user_storage_path  = os.path.join(self.STORAGE_PATH, user_infos['user_id'])    
		if not os.path.exists(user_storage_path):
			os.makedirs(user_storage_path)  
		user_comment_path = os.path.join(user_storage_path, 'item_preference.json')     

		# user_all_preferences = None 
		if os.path.exists(user_comment_path): 
			with open(user_comment_path, 'r') as f: 
				origin_data = json.load(f)    
			for _ in user_preference: 
				if _[0] in origin_data: 
					origin_data[_[0]].append(_[1])
				else: 
					origin_data[_[0]] = [_[1]] 
			# user_all_preferences = origin_data
			with open(user_comment_path, 'w') as f: 
				json.dump(origin_data, f)  
			# print(f'1-1: {new_data}')
		else: 
			item_score_dict = defaultdict(list)  
			for _ in user_preference: 
				item_score_dict[_[0]].append(_[1]) 
			# user_all_preferences = item_score_dict
			with open(user_comment_path, 'w') as f:    
				json.dump(item_score_dict, f)    
		pref_list = []
		for _ in user_preference: 
			if _[1] >= LIKE_LIMIT: 
				pref_list.append(_[0]) 
		self.update_user_preference_tag(user_infos, pref_list) 
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
# [['12584', 4.0], ['25455', 9.0], ['34506', 5.666666666666667]]    
def test_example_3(): 
	rec_store = STORE_RECOMMENDATION_SYSTEM(
		storage_path = 'datas/storage/user', 
		device = 'cuda:0', 
		embdding_storage_path = 'data/storage/embeddings', 
		classifier_name = 'decision_tree'
	)

	# 测试样例 3 通过 
	path_f2s = [
        'utils/test_files/Functional-Test/3/F2S-0.json' , 
        'utils/test_files/Functional-Test/3/F2S-1.json' , 
        'utils/test_files/Functional-Test/3/F2S-2.json' , 
        'utils/test_files/Functional-Test/3/F2S-3.json' , 
    ]
	path_stores = [
		'utils/test_files/Functional-Test/3/S.json'
	]
	path_user = [
		'utils/test_files/Functional-Test/3/UwoIn.json'
	]
	for i in range(len(path_f2s)): 
		data = get_feedback_to_store(path_f2s[i]) 
		store_info  = data[0] 
		user_info   = data[1] 
		rating_info = data[2] 
		rec_store.update_store_info(
			store_info
		)
		rec_store.update_user_store_preference(
			user_info, store_info['store_name'], rating_info
		)
	
	store_query_list = get_store_information(path_stores[0]) 
	for _ in store_query_list: 
		rec_store.update_store_info(_)
	user_info_query  = get_user_information(path_user[0]) 
	print(rec_store.recommend_store(user_info_query, [_["store_name"] for _ in store_query_list]))
	print(rec_store.get_user_item_preference(user_info_query) )
	sys.exit(0) 



def test_example_2(): 
	rec_store = STORE_RECOMMENDATION_SYSTEM(
		storage_path = 'datas/storage/user', 
		device = 'cuda:0', 
		embdding_storage_path = 'data/storage/embeddings', 
		classifier_name = 'decision_tree'
	)
	path_stores = [
		'utils/test_files/Functional-Test/2/S.json'
	]
	path_user = [
		'utils/test_files/Functional-Test/2/UwIn.json'
	]
	
	
	# 收到 user 并保存
	user_info_query  = get_user_information(path_user[0])    
	if 'user_preference' in user_info_query: 
		rec_store.update_user_preference_tag(user_info_query, user_info_query['user_preference']) 

	# 给每个商店打分 
 	# 收到 store 并接受 
	store_query_list = get_store_information(path_stores[0])      
	for _ in store_query_list: 
		rec_store.update_store_info(_)
	print(rec_store.recommend_store(user_info_query, [_["store_name"] for _ in store_query_list]))
	sys.exit(0) 


def test_example_1(): 
	rec_store = STORE_RECOMMENDATION_SYSTEM(
		storage_path = 'datas/storage/user', 
		device = 'cuda:0', 
		embdding_storage_path = 'data/storage/embeddings', 
		classifier_name = 'decision_tree'
	)

	path_stores = [
		'utils/test_files/Functional-Test/1/S.json'
	]
	path_user = [
		'utils/test_files/Functional-Test/1/UwoIn.json'
	]
	
	

	user_info_query  = get_user_information(path_user[0])    
	if 'user_preference' in user_info_query: 
		rec_store.update_user_preference_tag(user_info_query, user_info_query['user_preference']) 

	store_query_list = get_store_information(path_stores[0])      
	for _ in store_query_list: 
		rec_store.update_store_info(_)
	print(rec_store.recommend_store(user_info_query, [_["store_name"] for _ in store_query_list]))
	sys.exit(0) 

def test_example_4(): 
	rec_store = STORE_RECOMMENDATION_SYSTEM(
		storage_path = 'datas/storage/user', 
		device = 'cuda:0', 
		embdding_storage_path = 'data/storage/embeddings', 
		classifier_name = 'decision_tree'
	) 
	path_f2i = [
		'utils/test_files/Functional-Test/4/F2I.json' 
	]
	for _ in path_f2i: 
		data = get_feedback_to_item(_) 
		for _user in data: 
			rec_store.update_user_item_preference(
				{"user_id": _user}, data[_user] 
			)
	path_stores = [
		'utils/test_files/Functional-Test/1/S.json'
	]
	path_user = [
		'utils/test_files/Functional-Test/1/UwoIn.json'
	]

	
	user_info_query  = get_user_information(path_user[0])        
	if 'user_preference' in user_info_query: 
		rec_store.update_user_preference_tag(user_info_query, user_info_query['user_preference']) 
	

	print(user_info_query) 

	store_query_list = get_store_information(path_stores[0])      
	for _ in store_query_list: 
		rec_store.update_store_info(_)
	print(rec_store.recommend_store(user_info_query, [_["store_name"] for _ in store_query_list]))
	sys.exit(0) 

def test_example_5(): 
	rec_store = STORE_RECOMMENDATION_SYSTEM(
		storage_path = 'datas/storage/user', 
		device = 'cuda:0', 
		embdding_storage_path = 'data/storage/embeddings', 
		classifier_name = 'decision_tree'
	) 
	path_f2i = [
		'utils/test_files/Functional-Test/5/F2I.json' 
	]
	for _ in path_f2i: 
		data = get_feedback_to_item(_) 
		for _user in data: 
			rec_store.update_user_item_preference(
				{"user_id": _user}, data[_user] 
			)
	path_f2s = [
        'utils/test_files/Functional-Test/5/F2S-0.json' , 
        'utils/test_files/Functional-Test/5/F2S-1.json' , 
        'utils/test_files/Functional-Test/5/F2S-2.json' , 
        'utils/test_files/Functional-Test/5/F2S-3.json' , 
    ]
	for i in range(len(path_f2s)): 
		data = get_feedback_to_store(path_f2s[i]) 
		store_info  = data[0] 
		user_info   = data[1] 
		rating_info = data[2] 
		rec_store.update_store_info(
			store_info
		)
		rec_store.update_user_store_preference(
			user_info, store_info['store_name'], rating_info
		)
	
	
	path_stores = [
		'utils/test_files/Functional-Test/5/S.json'
	]
	path_user = [
		'utils/test_files/Functional-Test/5/UwIn.json'
	]
	store_query_list = get_store_information(path_stores[0])      
	for _ in store_query_list: 
		rec_store.update_store_info(_)
	user_info_query  = get_user_information(path_user[0])        
	if 'user_preference' in user_info_query: 
		rec_store.update_user_preference_tag(user_info_query, user_info_query['user_preference']) 

	print(user_info_query) 

	t1 = time.time() 
	print(rec_store.recommend_store(user_info_query, [_["store_name"] for _ in store_query_list]))  


def test_pressure(): 
	rec_store = STORE_RECOMMENDATION_SYSTEM(
		storage_path = 'datas/storage/user', 
		device = 'cuda:0', 
		embdding_storage_path = 'data/storage/embeddings', 
		classifier_name = 'decision_tree'
	) 
	path_f2i = [
		'utils/test_files/Performance-Test/1/F2I.json' 
	]
	for _ in path_f2i: 
		data = get_feedback_to_item(_) 
		for _user in data: 
			rec_store.update_user_item_preference(
				{"user_id": _user}, data[_user] 
			)
	path_f2s = [
        'utils/test_files/Performance-Test/1/F2S-0.json' , 
        'utils/test_files/Performance-Test/1/F2S-1.json' , 
        'utils/test_files/Performance-Test/1/F2S-2.json' , 
        'utils/test_files/Performance-Test/1/F2S-3.json' , 
    ]
	for i in range(len(path_f2s)): 
		data = get_feedback_to_store(path_f2s[i]) 
		store_info  = data[0] 
		user_info   = data[1] 
		rating_info = data[2] 
		rec_store.update_store_info(
			store_info
		)
		rec_store.update_user_store_preference(
			user_info, store_info['store_name'], rating_info
		)
	
	
	path_stores = [
		'utils/test_files/Performance-Test/1/S.json'
	]
	path_user = [
		'utils/test_files/Performance-Test/1/UwIn.json'
	]
	store_query_list = get_store_information(path_stores[0])      
	for _ in store_query_list: 
		rec_store.update_store_info(_)
	user_info_query  = get_user_information(path_user[0])        
	if 'user_preference' in user_info_query: 
		rec_store.update_user_preference_tag(user_info_query, user_info_query['user_preference']) 

	print(user_info_query) 
	t1 = time.time() 
	print(rec_store.recommend_store(user_info_query, [_["store_name"] for _ in store_query_list]))  
	t2 = time.time() 
	print(t2 - t1) 

if __name__ == '__main__':  
	if os.path.exists("datas"): 
		try:
			shutil.rmtree("datas") 
			print('Deleted!')
		except: 
			print('No need to delete')
	# test_example_5() 
	test_pressure() 
	# rec_store = STORE_RECOMMENDATION_SYSTEM(
	# 	storage_path = 'datas/storage/user', 
	# 	device = 'cuda:0', 
	# 	embdding_storage_path = 'datas/storage/embeddings', 
	# 	classifier_name = 'decision_tree'
	# )
	# app.run(host='0.0.0.0',port=5000)
	# test_example_1() 
	# test_example_2() 
	# test_example_3() 
	# test_example_4() 
	# test_example_5()
	# test_performance() 
 
	# # 初期：会只根据几个关键词来对用户进行建模 
	# rec_store.update_user_preference_tag(
	# 	{"user_id": "00121"}, 
	# 	['apple', 'fruit', 'bannana', 'oranage', 'food'] 
	# )  
	# # rec_store.update_user_item_preference(
	# # 	{"user_id": "00121"}, 
	# # 	[("apple", 8), ("orange", 8), ("juice", 3), ("car", 2), ("grape", 9)] 
	# # )
	# # rec_store.update_user_item_preference(
	# # 	{"user_id": "00121"}, 
	# # 	[("computer", 2), ("apple", 8), ("bycicle", 3), ("car", 2), ("grape", 9)] 
	# # )  


	# # 存储商店信息
	# rec_store.update_store_info(
	# 	{
	# 		"store_name": "store-1", 
	# 		"store_item": ['apple', 'grape', 'juice', 'milk'] 
	# 	}
	# )
	# rec_store.update_store_info(
	# 	{
	# 		"store_name": "store-2", 
	# 		"store_item": ['car', 'bycicle', 'pants', 'soccer'] 
	# 	}
	# )
	# rec_store.update_store_info(
	# 	{
	# 		"store_name": "store-3", 
	# 		"store_item": ['dvd', 'mp3', 'ipad', 'computer'] 
	# 	}
	# )
	
	# # 存储每个用户对于商店中商品的偏好 
	# # rec_store.update_user_store_preference({"user_id": "00121"}, "store-1", 7)
	# # rec_store.update_user_store_preference({"user_id": "00121"}, "store-2", 3)
	# # rec_store.update_user_store_preference({"user_id": "00121"}, "store-3", 4)   


	# # 新来了两个店铺 
 
 	# # ['apple', 'fruit', 'bannana', 'oranage', 'food'] 
	# rec_store.update_store_info(
	# 	{
	# 		"store_name": "store-4", 
	# 		"store_item": ['pen', 'paper', 'boat', 'ink', 'dress'] 
	# 	}
	# )
	# rec_store.update_store_info(
	# 	{
	# 		"store_name": "store-5", 
	# 		"store_item": ['uniform', 'wardrobe', 'clothing', 'overalls', 'tailcoat'] 
	# 	}
	# )
	# rec_store.update_store_info(
	# 	{
	# 		"store_name": "store-6", 
	# 		"store_item": ['fruit', 'cherry', 'peach', 'lime', 'papaya'] 
	# 	}
	# )
	# rec_result = rec_store.recommend_store(
	# 	{"user_id": "00121"}, ["store-4", "store-5", "store-6"] 
	# )
	# print(rec_result) 
	
	# [['store-4', 6.0], ['store-5', 4.0]] 	
	# python rec_code_embedding.py 
	# python rec_code_embedding.py 