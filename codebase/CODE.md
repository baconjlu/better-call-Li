## CodeBase of Recommendation System 



### 

- for each user, save its average score for each item, and each store 

- When a new store-feedback comes, update average score for items & stores

- When a new item-feedback comes, update average score for items  

- When recommending stores, Rank by [average score of item in score] * F(store_score)  



### TODO 

- BERT Inference is relatively slow, we can pre-process 30k popular english words in advance.(Doing Now)  

- Use GPU to infer (Done)

- Choose Random Forest to classify preference (Done) 





###
Usage:
```python
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

	rec_result = rec_store.recommend_store(
		{"user_id": "00121"}, ["store-4", "store-5"] 
	)
	print(rec_result) # [['store-4', 6.0], ['store-5', 4.0]]
```