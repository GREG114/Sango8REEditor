path =r'D:\data\Code\dbg\eg\edit_personSC.bin.txt'

with open(path,mode='r') as f:
    xxx = f.read().replace('\n','')



    idx = xxx.index('d20b0903')
    xxx = xxx[57050:]

    idx = xxx.index('0004164')
    print(idx)

    ss=0