import numpy as np 
import pandas as pd  
import os  
import random 
import json    

class GPT_RECOMMENDER:

	def __init__(self, 
		storage_path = 'datas/storage/user',
		openai_key = None 
	): 
		
		# 用户存储
		self.STORAGE_PATH = storage_path 
		os.makedirs(self.STORAGE_PATH, exist_ok = True) 

		self.prompt_path = 'utils/prompts/query.txt' 
		with open(self.prompt_path, 'r') as f: 
			self.prompt = f.read() 
		
		self.openai_key = openai_key 
		
		print(f'###current prompt###\n\n{self.prompt}\n\n') 
		

	
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
	
	def create_gpt_prompt(self, history_data, item_list): 
		cur_prompt = self.prompt 
		cur_prompt += '\n' + 'Question: User shopping history: [' + ", ".join(history_data) + "], item list: [" + ", ".join(item_list) + ']'
		return cur_prompt 

	def ask_gpt(self, prompt):
		return prompt 
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

			current_prompt = self.create_gpt_prompt(full_data, item_list)
			gpt_recommendation = self.ask_gpt(current_prompt) 


		else:  
			# NO history, direct recommend 
			random_selection = random.sample(item_list, K)  
			return random_selection  
			
		


if __name__ == '__main__':  

	rec_sys = GPT_RECOMMENDER() 
	# rec_sys.update_user_info(
	# 	{"user_id": "00121"}, 
	# 	["apple", "juice", "sossage"]
	# ) 
	# rec_sys.update_user_info(
	# 	{"user_id": "00121"}, 
	# 	["lettace", "grape", "pear"] 
	# )  
 
	rec_sys.recommend_item({"user_id": "00121"}, ['bannana', 'pen', 'paper', 'soda'], K = 2) 

