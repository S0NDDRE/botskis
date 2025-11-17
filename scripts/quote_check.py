import sys
from collections import Counter

path = sys.argv[1]
with open(path, 'r', encoding='utf-8') as f:
    s = f.read()

quotes = Counter()
quotes['single'] = s.count("'")
quotes['double'] = s.count('"')
quotes['triple_single'] = s.count("\"\"\"")
quotes['triple_double'] = s.count("\'\'\'")
print(quotes)
