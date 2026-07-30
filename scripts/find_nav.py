with open('www/index.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'class="bottom-nav"' in line:
            print(f'{i+1}: {line.strip()}')
