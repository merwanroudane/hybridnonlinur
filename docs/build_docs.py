"""Combine all parts into docs/index.html"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8')

DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)

# The part scripts wrote to docs/ subdir from here, so files are in docs/ subfolder
# Let's just read them from where they actually are
parts_paths = []
for pf in ['build_part1.py', 'build_part2.py', 'build_part3.py', 'build_part4.py']:
    code = open(pf, 'r', encoding='utf-8').read()
    code = code.replace("'docs/", "'")
    exec(code)

parts = ['_part1.html', '_part2.html', '_part3.html', '_part4.html']

# Check which location has the files
for p in parts:
    if not os.path.exists(p) and os.path.exists(f'docs/{p}'):
        os.rename(f'docs/{p}', p)

with open('index.html', 'w', encoding='utf-8') as out:
    for p in parts:
        with open(p, 'r', encoding='utf-8') as f:
            out.write(f.read())
        os.remove(p)

total = os.path.getsize('index.html')
print(f"docs/index.html generated ({total:,} bytes)")
