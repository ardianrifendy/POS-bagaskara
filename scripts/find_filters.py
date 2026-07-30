with open('www/index.html', 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if 'filter' in line.lower() and ('class=' in line or 'id=' in line):
            print(f"{i+1}: {line.strip()[:100]}")
