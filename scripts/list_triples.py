import sys
p=sys.argv[1]
with open(p,'r',encoding='utf-8') as f:
    for i,l in enumerate(f, start=1):
        if '"""' in l:
            print(i, l.rstrip())
