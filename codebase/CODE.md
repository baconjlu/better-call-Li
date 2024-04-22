## CodeBase of Recommendation System 



### 

- for each user, save its average score for each item, and each store 

- When a new store-feedback comes, update average score for items & stores

- When a new item-feedback comes, update average score for items  

- When recommending stores, Rank by [average score of item in score] * F(store_score)  


### TODO 

- BERT Inference is relatively slow, we can pre-process 30k popular english words in advance. 

- Use GPU to infer 

- Choose Random Forest to classify preference 





###
Usage:
```python
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
```