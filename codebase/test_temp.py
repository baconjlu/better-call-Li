import numpy as np 

if __name__ == '__main__': 
    path = 'utils/word_cache/0.npz' 
    data = np.load(path) 
    cnt = 0
    for _ in data: 
        print(_)
        print(data[_].shape) 
        cnt += 1 
        if cnt > 10: 
            break 