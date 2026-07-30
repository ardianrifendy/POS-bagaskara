with open('www/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[2385:2395]):
    print(f'{i+2386}: {line.encode("ascii", "ignore").decode("ascii").rstrip()}')
