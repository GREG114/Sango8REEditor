path =r'D:\data\Code\dbg\eg\83.bin.txt'

# with open(path,mode='r') as f:
#     xxx = f.read().replace('\n','')
#     idx_s = 40
#     c = xxx[idx_s:]
#     idx = c.index('ffff')    
#     print(idx)
    


ap = r'D:\data\Code\dbg\eg\edit_personSC.bin.txt'
with open(ap,mode='r') as f:
    xxx = f.read().replace('\n','')
    idx_s = xxx.index('00b8')
    print(idx_s)