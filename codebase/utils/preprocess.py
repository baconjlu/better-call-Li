import os 
import numpy as np 

import pandas as pd 
import json 
from BERT import Bert 
from tqdm import tqdm 
if __name__ == '__main__': 

	BERT_PATH = 'weights/bert-base-uncased' 
	device = 'cuda:0'
	bert_model = Bert(BERT_PATH, device)    


	word_cache_path = 'word_cache/words_dictionary.json' 

	 
	with open(word_cache_path, 'r') as f: 
		words = json.load(f) 

	# self.bert_model.getEmb(q_word).detach().cpu().numpy()
	cnt = 0 
	NUM = 3
	total_cnt = 0 
	save_freq = 1000 

	pretrained_embed = {}     
	print(len(words)) 

	for _ in tqdm(words):    
		total_cnt += 1 
		current_word = _

		word_vec = bert_model.getEmb(current_word).detach().cpu().numpy()
		pretrained_embed[current_word] = word_vec
		if (total_cnt % save_freq == 0) or (total_cnt == len(words)): 
			cnt += 1 
			cnt %= NUM 
			save_path = os.path.join('word_cache', str(cnt) + '.npz') 
			np.savez(save_path, **pretrained_embed) 