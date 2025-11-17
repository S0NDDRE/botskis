import sys
p=sys.argv[1]
a=int(sys.argv[2])
b=int(sys.argv[3])
with open(p,'r',encoding='utf-8') as f:
    for i,l in enumerate(f, start=1):
        if a<=i<=b:
            print(f"{i:4}: {l.rstrip()}")
