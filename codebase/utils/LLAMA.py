import torch
import os
from vllm import LLM, SamplingParams


class LLAMA():
    def __init__(self, pretrained_model_name_or_path = "weights/Llama-2-7b-chat-hf", gpu_id = '0') -> None:
        os.environ['CUDA_VISIBLE_DEVICES'] = str(gpu_id)
        self.sampling_params = SamplingParams(temperature=0.8, top_p=0.9, top_k=50, max_tokens=512, stop="</s>")
        self.model = LLM(model=pretrained_model_name_or_path, dtype=torch.float16, seed = 0, tensor_parallel_size=1, trust_remote_code=True, gpu_memory_utilization=0.7)
        print('LLAMA initialized')
         
    def getPrompts(self, texts):
        prompts = []
        for t in texts:
            prompt = t
            prompts.append(prompt)
        return prompts
    
    def ask(self, texts):
        '''
        input a list of text, output a list of reply
        '''
        prompts = self.getPrompts(texts)
        results = self.model.generate(prompts, self.sampling_params, use_tqdm = True)
        
        replys = []
        for index in range(len(results)):
            replys.append(results[index].outputs[0].text)
        return replys

if __name__ == '__main__': 
    llama = LLAMA("/home/mazhouyuan/LLAMA/Llama-2-7b-chat-hf", gpu_id = '1')
    texts = ["hi! Are you dong good?"]
    
    print(llama.ask(texts)) 