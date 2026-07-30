with open('www/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_code = """      if (type === 'history') {
        title.textContent = 'Filter Status Pembayaran';"""

new_code = """      if (type === 'history') {
        chipsContainer.style.display = 'flex';
        title.textContent = 'Filter Status Pembayaran';"""
html = html.replace(old_code, new_code)

old_code2 = """      } else if (type === 'product') {
        title.textContent = 'Filter Produk & Stok';
        chipsContainer.innerHTML = '';"""

new_code2 = """      } else if (type === 'product') {
        chipsContainer.style.display = 'block';
        title.textContent = 'Filter Produk & Stok';
        chipsContainer.innerHTML = '';"""
html = html.replace(old_code2, new_code2)

old_code3 = """      } else if (type === 'inv') {
        title.textContent = 'Filter Merek Inventori';"""

new_code3 = """      } else if (type === 'inv') {
        chipsContainer.style.display = 'flex';
        title.textContent = 'Filter Merek Inventori';"""
html = html.replace(old_code3, new_code3)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done!')
