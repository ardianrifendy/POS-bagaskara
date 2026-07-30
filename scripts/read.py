with open('www/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines[2183:2196]):
    print(f'{i+2184}: {line.encode("ascii", "ignore").decode("ascii").strip()}')
