with open('www/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[2285:2310]):
    print(f'{i+2286}: {line.encode("ascii", "ignore").decode("ascii").strip()}')
