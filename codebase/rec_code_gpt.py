import re 
import numpy as np 
import pandas as pd  
import os  
import random 
import openai
import json    

class GPT_RECOMMENDER:

	def __init__(self, 
		storage_path = 'datas/storage/user',
		openai_key = None,
		key_path = None,
		api_base = "https://api.openai.com/v1",
		max_retries = 10,
	): 
		
		# 用户存储
		self.STORAGE_PATH = storage_path 
		os.makedirs(self.STORAGE_PATH, exist_ok = True) 

		self.prompt_path = 'utils/prompts/query.txt' 
		with open(self.prompt_path, 'r') as f: 
			self.prompt = f.read() 
		
		self.openai_key = openai_key 
		
		print(f'###current prompt###\n\n{self.prompt}\n\n') 

		self.keys = []
		with open(key_path, 'r', encoding='utf-8') as file:
			for line in file:
				key = line.strip()
				self.keys.append(key)
		self.api_base = api_base
		self.using_key = 0
		self.max_retries  = max_retries
	
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
	
	def getKey(self):
		self.using_key = (self.using_key + 1) % len(self.keys)
		return self.keys[self.using_key]

	def ask_gpt(self, prompt):
		openai.api_key = self.getKey()
		openai.api_base = self.api_base
		MODEL = "gpt-3.5-turbo"
		retries = 0
		error_keys = []
		while retries < self.max_retries:
			try:
				response = openai.ChatCompletion.create(
					model=MODEL,
					messages=prompt,
					temperature = 0.8)
				print(f"Key {self.using_key} Successful")
				break
			except Exception as e:
				error_keys.append(self.using_key)
				print(f"Key {self.using_key} Failed")
				openai.api_key = self.getKey()
			retries += 1
		if retries == self.max_retries:
			answer = ""		# Key连接失败
		else:
			answer = response['choices'][0]['message']['content']

		# parse gpt answer 
		print(answer)
		pattern = r'\[(.*?)\]'
		data_list = re.findall(r'\[([^\[\]]*)\]', answer)
		extracted_data = [item.strip() for item in data_list[0].split(',')]
		return extracted_data 

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
			return gpt_recommendation

		else:  
			# NO history, direct recommend 
			random_selection = random.sample(item_list, K)  
			return random_selection  
			
		



if __name__ == '__main__':  
	rec_sys = GPT_RECOMMENDER(key_path = './utils/keys/MyKeys.txt', api_base = "https://api.nbfaka.com/v1") 

	rec_sys.update_user_info(
		{"user_id": "00121"}, 
		["apple", "juice", "soda", "pepper", "hamburger"] 
	) 

	print(rec_sys.recommend_item({"user_id": "00121"}, ['bannana', 'pen', 'paper', 'water'], K = 2))
	reply = rec_sys.ask_gpt(prompt = "hi are you ok?")
	print(reply)
	# with open('test_pars.txt', 'r') as f:
	# 	prompt = f.read() 
	# pattern = r'\[(.*?)\]'
	# data_list = re.findall(r'\[([^\[\]]*)\]', prompt)
	# extracted_data = [item.strip() for item in data_list[0].split(',')]
	# print(extracted_data)
	# for _ in extracted_data:
	# 	print(_) 
	# print([data for data in extracted_data])
	# extracted_data = [data.replace("'", "") for data in extracted_data]
	# print(extracted_data)
	# rec_sys = GPT_RECOMMENDER() 
	# rec_sys.update_user_info(
	# 	{"user_id": "00121"}, 
	# 	["apple", "juice", "sossage"]
	# ) 
	# rec_sys.update_user_info(
	# 	{"user_id": "00121"}, 
	# 	["lettace", "grape", "pear"] 
	# )  
 
	# rec_sys.recommend_item({"user_id": "00121"}, ['bannana', 'pen', 'paper', 'soda'], K = 2) 

