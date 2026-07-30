import re

with open('www/index.html', 'r', encoding='utf-8') as f:
    data = f.read()

# Replace body.light-theme with body[data-theme*="light"]
data = re.sub(r'body\.light-theme', r'body[data-theme*="light"]', data)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(data)
