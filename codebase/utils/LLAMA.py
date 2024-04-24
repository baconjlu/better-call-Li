import torch
import time
import os
from vllm import LLM, SamplingParams


class LLAMA():
    def __init__(self, pretrained_model_name_or_path = "weights/Llama-2-7b-chat-hf", prompt_path = "./utils/prompts", gpu_id = '0') -> None:
        os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu_id)
        self.sampling_params = SamplingParams(temperature=0.8, top_p=0.9, top_k=50, max_tokens=512, stop="</s>")
        self.model = LLM(model=pretrained_model_name_or_path, dtype=torch.float16, seed = 0, tensor_parallel_size=1, trust_remote_code=True, gpu_memory_utilization=0.7)
        
        with open(os.path.join(prompt_path, 'rec_with_interest.txt'), 'r') as file:
            self.rec_with_interest_prompt = file.read()
        with open(os.path.join(prompt_path, 'rec_with_item.txt'), 'r') as file:
            self.rec_with_item_prompt = file.read()
        with open(os.path.join(prompt_path, 'report.txt'), 'r') as file:
            self.report_prompt = file.read()
            
        print('LLAMA initialized')
         
    def rec_with_interest(self, interest_list, item_list):
        prompts = []
        small_lists = [item_list[i:i+10] for i in range(0, len(item_list), 10)]
        for l in small_lists:
            prompt = self.rec_with_interest_prompt.replace("{{Interest List}}", str(interest_list)).replace("{{Product List}}", str(l))
            prompts.append(prompt)
            
        replys = self.ask(prompts)
        result_string = ''.join(replys).lower()
        interest_prodects = []
        for item in item_list:
            if item.lower() in result_string:
                interest_prodects.append(item)
                
        prompt = self.rec_with_interest_prompt.replace("{{Interest List}}", str(interest_list)).replace("{{Product List}}", str(interest_prodects))
        replys = self.ask([prompt])
        result_string = ''.join(replys).lower()
        interest_prodects = []
        for item in item_list:
            if item.lower() in result_string:
                interest_prodects.append(item)
        return interest_prodects
    
    def rec_with_item(self, pos_item_list, item_list):
        prompts = []
        small_lists = [item_list[i:i+10] for i in range(0, len(item_list), 10)]
        for l in small_lists:
            prompt = self.rec_with_item_prompt.replace("{{Pos}}", str(pos_item_list)).replace("{{Product List}}", str(l))
            prompts.append(prompt)
            
        replys = self.ask(prompts)
        result_string = ''.join(replys).lower()
        interest_prodects = []
        for item in item_list:
            if item.lower() in result_string:
                interest_prodects.append(item)
                
        prompt = self.rec_with_item_prompt.replace("{{Pos}}", str(pos_item_list)).replace("{{Product List}}", str(interest_prodects))
        replys = self.ask([prompt])
        result_string = ''.join(replys).lower()
        interest_prodects = []
        for item in item_list:
            if item.lower() in result_string:
                interest_prodects.append(item)
        return interest_prodects
    
    def get_report(self, pos_item_list, neg_item_list):
        prompt = self.report_prompt.replace("{{Pos}}", str(pos_item_list)).replace("{{Neg}}", str(neg_item_list))
        replys = self.ask([prompt])
        return replys[0]

    def ask(self, prompts):
        '''
        input a list of prompts, output a list of reply
        '''
        results = self.model.generate(prompts, self.sampling_params, use_tqdm = True)
        
        replys = []
        for index in range(len(results)):
            replys.append(results[index].outputs[0].text)
        return replys

if __name__ == '__main__': 
    llama = LLAMA("/home/mazhouyuan/LLAMA/Llama-2-7b-chat-hf", gpu_id = '1')
    # texts = ["hi! Are you dong good?"]
    # print(llama.ask(texts)) 
    
    
    item_list = ["Apples", "Milk", "Laptop", "Meat", "Bananas", "Bread", "Eggs", "Cheese", "Coffee", "Tea", 
             "Orange Juice", "Cereal", "Pasta", "Rice", "Chicken", "Beef", "Pork", "Potatoes", 
             "Tomatoes", "Spinach", "Broccoli", "Carrots", "Onions", "Garlic", "Bell Peppers", "Avocado", 
             "Strawberries", "Blueberries", "Grapes", "Watermelon", "Pineapple", "Cucumbers", "Lettuce", 
             "Kale", "Almonds", "Peanuts", "Walnuts", "Cashews", "Hazelnuts", "Pistachios", "Olive Oil", 
             "Coconut Oil", "Soy Sauce", "Vinegar", "Honey", "Maple Syrup", "Salt", "Pepper", "Cinnamon", 
             "Vanilla Extract", "Sugar", "Flour", "Baking Powder", "Baking Soda", "Jeans", "Chocolate Chips", 
             "Yogurt", "Ice Cream", "Butter", "Cream Cheese", "Sour Cream", "Mayonnaise", "Ketchup", 
             "Mustard", "Barbecue Sauce", "Guacamole", "Chips", "Crackers", "Popcorn", "Peanut Butter", 
             "Jam", "Biscuits", "Cookies", "Brownies", "Headphones", "Pie Crust", "Marshmallows", "Graham Crackers", 
             "Soup", "Canned Beans", "Canned Tomatoes", "Canned Tuna", "Canned Salmon", "Canned Chicken", 
             "Canned Corn", "Canned Fruit", "Canned Vegetables", "Instant Noodles", "Instant Rice", 
             "Instant Soup", "Instant Coffee", "Instant Tea", "Instant Oatmeal", "Instant Mashed Potatoes", 
             "Instant Pancake Mix", "Instant Gravy", "Instant Pudding", "Instant Gelatin"]
   
    # Interest-Rec Demo
    interest_list = ["Technology", "Fashion"]
    start_time = time.time()
    rec_list = llama.rec_with_interest(interest_list, item_list)
    print("Interest-Rec time:", round(time.time() - start_time, 2), "seconds")
    print(rec_list)
    # ['Laptop', 'Jeans', 'Headphones']
    
    # Item-Rec Demo
    
    pos_list = ["Baking Soda", "Ice Cream", "Coffee", "Tea", "Peanut Butter", "Jelly"]
    start_time = time.time()
    rec_list = llama.rec_with_item(pos_list, item_list)
    print("Item-Rec time:", round(time.time() - start_time, 2), "seconds")
    print(rec_list)
    # ['Baking Soda', 'Ice Cream', 'Butter', 'Peanut Butter']

    # User-Report Demo
    
    pos_list = ["Laptop", "Ice Cream", "Coffee", "Tea", "Peanut Butter", "Jelly"]
    neg_list = ["Orange Juice", "Cereal", "Pasta", "Rice"]
    start_time = time.time()
    report = llama.get_report(pos_list, neg_list)
    print("Item-Rec time:", round(time.time() - start_time, 2), "seconds")
    print(report)
    # Based on your shopping history, it appears you have a strong interest in technology, particularly laptops, which suggests a need or desire for a reliable and efficient device for work or personal use. Your interest in ice cream, coffee, and tea also indicates a taste for indulgent treats and a preference for caffeinated beverages. Additionally, your purchases of peanut butter and jelly suggest a love for spreads and a desire for quick and easy snacks.
    # On the other hand, your dislikes reveal a lack of interest in certain food items, such as orange juice and cereal, which may suggest a preference for more natural or less processed foods. Additionally, your dislike of pasta and rice may indicate a desire for more diverse and varied meals, rather than relying on a limited range of carbohydrate-based options.
    # In summary, your shopping habits suggest a focus on technology, indulgent treats, and a desire for quick and easy meals, while also indicating a preference for more natural and less processed foods. You tend to steer clear of certain carbohydrate-based options, such as pasta and rice, in favor of more diverse and varied meals.