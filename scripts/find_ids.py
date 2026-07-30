import re
with open('www/index.html', 'r', encoding='utf-8') as f:
    text = f.read()
ids = re.findall(r'id="([^"]+)"', text)
for i in ids:
    if 'tab' in i.lower() or 'nav' in i.lower():
        print(i)
