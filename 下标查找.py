path =r'C:\Data\Project\self_sango\Sango8REEditor\存档武将分析.md'

with open(path,mode='r') as f:
    xxx = f.read().replace('\n','')

    idx = xxx.index('651b')
    print(idx)
    print(xxx[108:112])

    ss=0