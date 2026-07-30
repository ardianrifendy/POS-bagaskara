with open('www/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[2250:2290]):
    print(f'{i+2251}: {line.encode("ascii", "ignore").decode("ascii").strip()}')
