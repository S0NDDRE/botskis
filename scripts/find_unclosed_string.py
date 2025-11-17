import sys
p=sys.argv[1]
with open(p,'r',encoding='utf-8') as f:
    data=f.read()

in_single=False
in_double=False
in_triple_single=False
in_triple_double=False
line_no=1
idx=0
while idx < len(data):
    ch=data[idx]
    if data[idx:idx+3]=="\"\"\"":
        in_triple_double=not in_triple_double
        idx+=3
        continue
    if data[idx:idx+3]=="'''":
        in_triple_single=not in_triple_single
        idx+=3
        continue
    if not (in_triple_double or in_triple_single):
        if ch=='"' and not in_single:
            in_double = not in_double
        elif ch=="'" and not in_double:
            in_single = not in_single
    if ch=='\n':
        line_no+=1
    idx+=1

print('Triple double', in_triple_double)
print('Triple single', in_triple_single)
print('Double quote', in_double)
print('Single quote', in_single)
if in_double or in_single or in_triple_double or in_triple_single:
    print('Unclosed string detected')
else:
    print('All strings closed')
