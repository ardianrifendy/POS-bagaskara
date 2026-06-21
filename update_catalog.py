import csv
import json
import re

csv_file = 'update database erafone.csv'
js_file = 'www/phone-catalog.js'

catalog = []

with open(csv_file, 'r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        nama = row.get('Nama', '').strip()
        if not nama:
            continue
            
        brand = row.get('Brand', '').strip()
        kategori = row.get('Tipe_Produk', '').strip()
        if not kategori:
            kategori = row.get('Kategori', '').strip()
            
        harga_normal = row.get('Harga', '').strip()
        harga_promo = row.get('Harga_Promo', '').strip()
        
        # Determine price
        price = 0
        if harga_promo and harga_promo.isdigit():
            price = int(harga_promo)
        elif harga_normal and harga_normal.isdigit():
            price = int(harga_normal)
            
        if price == 0:
            continue
            
        # Try to extract RAM and Storage
        ram = ""
        storage = ""
        kapasitas = row.get('Kapasitas', '').strip()
        
        # If empty, try to extract from Nama
        target_str = kapasitas if kapasitas else nama
        
        # Regex to find RAM/ROM like 8/256GB or 12GB/512GB
        match = re.search(r'(\d+)\s*(?:GB|TB)?\s*/\s*(\d+)\s*(GB|TB)', target_str, re.IGNORECASE)
        if match:
            ram = match.group(1) + "GB"
            storage = match.group(2) + match.group(3).upper()
        else:
            # Maybe just "256GB" without RAM
            match2 = re.search(r'(?<!/)\b(\d+)\s*(GB|TB)\b', target_str, re.IGNORECASE)
            if match2:
                storage = match2.group(1) + match2.group(2).upper()
                
        catalog.append({
            "brand": brand,
            "model": nama,
            "category": kategori,
            "ram": ram,
            "storage": storage,
            "price": price,
            "image": row.get('Link_Gambar', '')
        })

# Deduplicate by model name
seen = set()
unique_catalog = []
for item in catalog:
    if item['model'] not in seen:
        seen.add(item['model'])
        unique_catalog.append(item)

# Sort by brand then model
unique_catalog.sort(key=lambda x: (x['brand'], x['model']))

js_content = 'window.ERAFONE_CATALOG = {"catalog": ' + json.dumps(unique_catalog) + '};'

with open(js_file, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Successfully generated {js_file} with {len(unique_catalog)} products.")
