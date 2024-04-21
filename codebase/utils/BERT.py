from transformers import AutoTokenizer, AutoModel
import torch


class Bert():
    def __init__(self, pretrained_model_name_or_path = "weights/bert-base-uncased", device = 'cuda:0') -> None:
        self.model = AutoModel.from_pretrained(pretrained_model_name_or_path).to(torch.device(device)) 
        self.tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path)
        self.device = device 
    
    def getEmb(self, text):
        encoding = self.tokenizer(text, return_tensors='pt', max_length=512, truncation=True)
        encoding.to(self.device) 
        with torch.no_grad():
            output = self.model(**encoding)
        embedding = output.last_hidden_state.mean(dim=1)
        return embedding
    
    def getTextSim(self, text1, text2, threshold = 0.5):
        encoding1 = self.tokenizer(text1, return_tensors='pt', max_length=512, truncation=True)
        encoding2 = self.tokenizer(text2, return_tensors='pt', max_length=512, truncation=True)
        encoding1.to(self.device) 
        encoding2.to(self.device)
        with torch.no_grad():
            output1 = self.model(**encoding1)
            output2 = self.model(**encoding2)
        # print(output1.last_hidden_state.mean(dim=1))
        cosine_sim = torch.nn.functional.cosine_similarity(output1.last_hidden_state.mean(dim=1),
                                                           output2.last_hidden_state.mean(dim=1))
        return cosine_sim.item() > threshold, cosine_sim.item()
    
    def getEmbSim(self, emb1, emb2, threshold = 0.5):
        emb1 = torch.tensor(emb1)
        emb2 = torch.tensor(emb2)
        cosine_sim = torch.nn.functional.cosine_similarity(emb1, emb2)
        return cosine_sim.item() > threshold, cosine_sim.item()


if __name__ == '__main__': 
    bert = Bert(pretrained_model_name_or_path = 'weights/bert-base-uncased')  

    print(bert.getTextSim('apple', 'orange', 0.3)) 
    print(bert.getTextSim('apple', 'fruit', 0.3)) 
    print(bert.getTextSim('apple', 'car', 0.3)) 
    print(bert.getTextSim('apple', 'bus', 0.3)) 
    print(bert.getTextSim('apple', 'bannana', 0.3)) 
    print(bert.getTextSim('apple', 'vegatable', 0.3)) 