import ast
import sys

def check(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
        ast.parse(s)
        print('OK')
    except Exception as e:
        print(type(e).__name__, e)

if __name__ == '__main__':
    for p in sys.argv[1:]:
        print('Checking', p)
        check(p)
