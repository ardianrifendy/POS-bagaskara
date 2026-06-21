import csv
import json
import re

csv_file = 'UPDATE BESAR.csv'
js_file = 'www/phone-catalog.js'

catalog_dict = {}

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
            
        harga_normal = row.get('Harga_Normal', row.get('Harga', '')).strip()
        harga_promo = row.get('Harga_Promo', '').strip()
        
        # Determine price
        price = 0
        if harga_promo and harga_promo.isdigit():
            price = int(harga_promo)
        elif harga_normal and harga_normal.isdigit():
            price = int(harga_normal)
            
        if price == 0:
            continue
            
        warna = row.get('Warna', '').strip()
        kapasitas = row.get('Kapasitas', '').strip()
        stok_str = row.get('Stok_Qty', '0').strip()
        stok = int(stok_str) if stok_str.isdigit() else 0
        status_stok = row.get('Status_Stok', '').strip()
        varian_name = row.get('Varian', '').strip()
        image = row.get('Link_Gambar', '').strip()
        
        # Intelligent Extraction for un-split catalog items
        if warna in ('', '-') and kapasitas in ('', '-'):
            if ' - ' in nama:
                parts = nama.rsplit(' - ', 1)
                nama = parts[0].strip()
                warna = parts[1].strip()
            
            cap_match = re.search(r'\s(\d+/(?:\d+\.)?\d+[A-Za-z]+|\d+[A-Za-z]+)$', nama)
            if cap_match:
                kapasitas = cap_match.group(1)
                nama = nama[:cap_match.start()].strip()
            
            # Reconstruct variant_name for clarity
            if warna != '-' and kapasitas != '-':
                varian_name = f"{kapasitas},{warna}"
            elif warna != '-':
                varian_name = warna
            elif kapasitas != '-':
                varian_name = kapasitas
        
        # Initialize base model if not exists
        if nama not in catalog_dict:
            catalog_dict[nama] = {
                "brand": brand,
                "model": nama,
                "category": kategori,
                "image": image,
                "variants": []
            }
            
        # Append variant
        catalog_dict[nama]["variants"].append({
            "color": warna,
            "capacity": kapasitas,
            "variant_name": varian_name,
            "price": price,
            "stock": stok,
            "status": status_stok,
            "image": image
        })

# Process min/max prices and sort
unique_catalog = []
for model_name, data in catalog_dict.items():
    prices = [v["price"] for v in data["variants"]]
    data["price_min"] = min(prices) if prices else 0
    data["price_max"] = max(prices) if prices else 0
    
    # Sort variants by capacity then color
    data["variants"].sort(key=lambda x: (x["capacity"], x["color"]))
    
    unique_catalog.append(data)

# Sort by brand then model
unique_catalog.sort(key=lambda x: (x['brand'], x['model']))

js_content = 'window.ERAFONE_CATALOG = {"catalog": ' + json.dumps(unique_catalog) + '};'

with open(js_file, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Successfully generated {js_file} with {len(unique_catalog)} base models.")
