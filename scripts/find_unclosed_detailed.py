import sys
p=sys.argv[1]
with open(p,'r',encoding='utf-8') as f:
    data=f.read()

in_single=False
in_double=False
in_triple_double=False
in_triple_single=False
line_no=1
idx=0
while idx < len(data):
    if data[idx]=='\n':
        line_no+=1
    if data[idx:idx+3]=="\"\"\"":
        in_triple_double=not in_triple_double
        print(f"line {line_no}: toggle triple double -> {in_triple_double}")
        idx+=3
        continue
    if data[idx:idx+3]=="'''":
        in_triple_single=not in_triple_single
        print(f"line {line_no}: toggle triple single -> {in_triple_single}")
        idx+=3
        continue
    if not (in_triple_double or in_triple_single):
        if data[idx]=='"':
            in_double = not in_double
            print(f"line {line_no}: toggle double -> {in_double}")
        elif data[idx]=="'":
            in_single = not in_single
            print(f"line {line_no}: toggle single -> {in_single}")
    idx+=1
print('final states:', in_triple_double, in_triple_single, in_double, in_single)
