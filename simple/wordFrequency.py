import json

def frequency(file_name):
    with open(file_name,'r',encoding='utf8') as f:
        data=json.load(f)
    strs=''
    for k , v in data.items():  
        strs+=k+v
    freq={}
    for i in strs:  
        if i in freq:  
            freq[i]+=1  
        else:  
            freq[i]=1
    freqList=[]
    for k,v in freq.items():  
        freqList.append([k,v])
    return freqList
def frequency_as_string(string):
    freq={}
    for i in string:  
        if i in freq:  
            freq[i]+=1  
        else:  
            freq[i]=1
    freqList=[]
    for k,v in freq.items():  
        freqList.append([k,v])
    return freqList
