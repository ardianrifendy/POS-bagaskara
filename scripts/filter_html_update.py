with open('www/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. History Filter
history_old = """      <div class="search-row">
        <input type="text" id="history-search-input" placeholder="Cari nama pembeli, no invoice, IMEI..." oninput="renderHistoryList()">
      </div>
      <div class="filter-chips" id="history-filter-chips" style="display:flex; gap:8px; overflow-x:auto; padding-bottom:10px; margin-bottom:4px; -webkit-overflow-scrolling:touch; scrollbar-width:none;">
        <div class="chip active" data-hstatus="all" onclick="filterHistoryStatus('all')">Semua</div>
        <div class="chip" data-hstatus="lunas" onclick="filterHistoryStatus('lunas')">Lunas</div>
        <div class="chip" data-hstatus="dp" onclick="filterHistoryStatus('dp')">DP</div>
        <div class="chip" data-hstatus="belum_bayar" onclick="filterHistoryStatus('belum_bayar')">Belum Bayar</div>
        <div class="chip" data-hstatus="belum_lunas" onclick="filterHistoryStatus('belum_lunas')">Semua Piutang</div>
      </div>"""

history_new = """      <div style="display:flex; gap:10px; margin-bottom:16px;">
        <div style="flex:1; position:relative;">
          <input type="text" id="history-search-input" placeholder="Cari nama pembeli, no invoice, IMEI..." oninput="renderHistoryList()" style="width:100%; padding: 14px 16px; border-radius:12px; background:var(--bk3); border:1px solid rgba(255,255,255,0.08); color:#fff; outline:none; font-size:14px;">
        </div>
        <div style="position:relative; background:var(--bk3); border:1px solid rgba(255,255,255,0.08); border-radius:12px; display:flex; align-items:center; justify-content:center; width:52px; cursor:pointer;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
          <select id="history-filter-select" onchange="filterHistoryStatus(this.value)" style="position:absolute; top:0; left:0; width:100%; height:100%; opacity:0; cursor:pointer; font-size:16px;">
            <option value="all">Semua Status</option>
            <option value="lunas">Lunas</option>
            <option value="dp">DP</option>
            <option value="belum_bayar">Belum Bayar</option>
            <option value="belum_lunas">Semua Piutang</option>
          </select>
        </div>
      </div>"""

if history_old in html:
    html = html.replace(history_old, history_new)
else:
    print('History old block not found')

# 2. Product Filter HTML
product_old = """        <div class="search-row">
          <input type="text" id="product-search-input" placeholder="Cari merek, nama produk..." oninput="renderProductList()">
          <button class="btn-primary" onclick="openProductModal()" style="padding: 10px 14px; white-space:nowrap; width:auto;">
            <span style="font-size:16px;">+</span><span class="desktop-only" style="margin-left:4px;">Stok</span>
          </button>
          <input type="file" id="product-import-file" accept=".csv" style="display: none;" onchange="importProductsFromCSV(event)">
        </div>
  
        <!-- Brand Filter Chips -->
        <div class="filter-chips" id="product-filter-chips" style="display: flex; gap: 8px; overflow-x: auto; padding-bottom: 10px; margin-bottom: 16px; -webkit-overflow-scrolling: touch;">
          <div class="chip active" onclick="filterProductBrand('All')" data-brand="All">Semua</div>
        </div>"""

product_new = """        <div style="display:flex; gap:10px; margin-bottom:16px;">
          <div style="flex:1; position:relative;">
            <input type="text" id="product-search-input" placeholder="Cari merek, nama produk..." oninput="renderProductList()" style="width:100%; padding: 14px 16px; border-radius:12px; background:var(--bk3); border:1px solid rgba(255,255,255,0.08); color:#fff; outline:none; font-size:14px;">
          </div>
          <div style="position:relative; background:var(--bk3); border:1px solid rgba(255,255,255,0.08); border-radius:12px; display:flex; align-items:center; justify-content:center; width:52px; cursor:pointer;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
            <select id="product-filter-select" onchange="filterProductBrand(this.value)" style="position:absolute; top:0; left:0; width:100%; height:100%; opacity:0; cursor:pointer; font-size:16px;">
              <option value="All">Semua Brand</option>
            </select>
          </div>
          <button class="btn-primary" onclick="openProductModal()" style="padding: 10px 14px; white-space:nowrap; width:auto; border-radius:12px;">
            <span style="font-size:16px;">+</span><span class="desktop-only" style="margin-left:4px;">Stok</span>
          </button>
          <input type="file" id="product-import-file" accept=".csv" style="display: none;" onchange="importProductsFromCSV(event)">
        </div>"""

if product_old in html:
    html = html.replace(product_old, product_new)
else:
    print('Product old block not found')

# 3. Inv Select Filter HTML
inv_old = """        <div class="search-row" style="margin-top:16px; margin-bottom:10px;">
          <input type="text" id="inv-search-input" placeholder="Cari nama HP atau brand..." oninput="renderInventorySelectList()">
        </div>
        <div class="filter-chips" id="inv-select-chips" style="margin-top:0; padding-bottom:6px; overflow-x:auto;">
          <button class="chip active" data-brand="All" onclick="filterInventorySelectBrand('All')">Semua</button>
          <button class="chip" data-brand="Samsung" onclick="filterInventorySelectBrand('Samsung')">Samsung</button>
          <button class="chip" data-brand="Apple" onclick="filterInventorySelectBrand('Apple')">iPhone</button>
          <button class="chip" data-brand="Xiaomi" onclick="filterInventorySelectBrand('Xiaomi')">Xiaomi</button>
          <button class="chip" data-brand="OPPO" onclick="filterInventorySelectBrand('OPPO')">OPPO</button>
          <button class="chip" data-brand="Vivo" onclick="filterInventorySelectBrand('Vivo')">Vivo</button>
          <button class="chip" data-brand="Realme" onclick="filterInventorySelectBrand('Realme')">Realme</button>
          <button class="chip" data-brand="Poco" onclick="filterInventorySelectBrand('Poco')">Poco</button>
          <button class="chip" data-brand="iQOO" onclick="filterInventorySelectBrand('iQOO')">iQOO</button>
        </div>"""

inv_new = """        <div style="display:flex; gap:10px; margin-top:16px; margin-bottom:16px;">
          <div style="flex:1; position:relative;">
            <input type="text" id="inv-search-input" placeholder="Cari nama HP atau brand..." oninput="renderInventorySelectList()" style="width:100%; padding: 14px 16px; border-radius:12px; background:var(--bk3); border:1px solid rgba(255,255,255,0.08); color:#fff; outline:none; font-size:14px;">
          </div>
          <div style="position:relative; background:var(--bk3); border:1px solid rgba(255,255,255,0.08); border-radius:12px; display:flex; align-items:center; justify-content:center; width:52px; cursor:pointer;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
            <select id="inv-filter-select" onchange="filterInventorySelectBrand(this.value)" style="position:absolute; top:0; left:0; width:100%; height:100%; opacity:0; cursor:pointer; font-size:16px;">
              <option value="All">Semua Brand</option>
              <option value="Samsung">Samsung</option>
              <option value="Apple">iPhone</option>
              <option value="Xiaomi">Xiaomi</option>
              <option value="OPPO">OPPO</option>
              <option value="Vivo">Vivo</option>
              <option value="Realme">Realme</option>
              <option value="Poco">Poco</option>
              <option value="iQOO">iQOO</option>
            </select>
          </div>
        </div>"""

if inv_old in html:
    html = html.replace(inv_old, inv_new)
else:
    print('Inv old block not found')

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done!')
