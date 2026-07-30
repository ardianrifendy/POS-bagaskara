with open('www/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'id="prod-search-input"' in line:
        print(f'PROD SEARCH: {i}')
    if '<!-- Brand Filter Chips -->' in line:
        print(f'PROD FILTER CHIPS START: {i}')
    if 'id="inv-select-search"' in line:
        print(f'INV SEARCH: {i}')
    if 'id="inv-select-chips"' in line:
        print(f'INV FILTER CHIPS: {i}')
