path =r'D:\data\Code\dbg\eg\edit_personSC.bin.txt'

with open(path,mode='r') as f:
    xxx = f.read().replace('\n','')
    idx = xxx.index('00aa')
    print(idx)
    print(xxx[108:112])

    ss=0