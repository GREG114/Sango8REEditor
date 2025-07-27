path = r'D:\data\Code\dbg\sanedit\warriors\ea0b.txt'
with open(path,'r',encoding='utf-8') as f:
    content = f.read().replace('\n','')
    t = content[122:130]
    print(t)
    ss=0