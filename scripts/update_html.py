with open('www/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Replace the History, Product, and Inv icon divs to trigger openGlobalFilter
history_old = """        <div style="position:relative; background:var(--bk3); border:1px solid rgba(255,255,255,0.08); border-radius:12px; display:flex; align-items:center; justify-content:center; width:52px; cursor:pointer;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
          <select id="history-filter-select" onchange="filterHistoryStatus(this.value)" style="position:absolute; top:0; left:0; width:100%; height:100%; opacity:0; cursor:pointer; font-size:16px;">
            <option value="all">Semua Status</option>
            <option value="lunas">Lunas</option>
            <option value="dp">DP</option>
            <option value="belum_bayar">Belum Bayar</option>
            <option value="belum_lunas">Semua Piutang</option>
          </select>
        </div>"""

history_new = """        <div onclick="openGlobalFilter('history')" style="position:relative; background:var(--bk3); border:1px solid rgba(255,255,255,0.08); border-radius:12px; display:flex; align-items:center; justify-content:center; width:52px; cursor:pointer;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
        </div>"""

html = html.replace(history_old, history_new)

product_old = """        <div style="position:relative; background:var(--bk3); border:1px solid rgba(255,255,255,0.08); border-radius:12px; display:flex; align-items:center; justify-content:center; width:52px; cursor:pointer;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
          <select id="product-filter-select" onchange="filterProductBrand(this.value)" style="position:absolute; top:0; left:0; width:100%; height:100%; opacity:0; cursor:pointer; font-size:16px;">
            <option value="All">Semua Brand</option>
          </select>
        </div>"""

product_new = """        <div onclick="openGlobalFilter('product')" style="position:relative; background:var(--bk3); border:1px solid rgba(255,255,255,0.08); border-radius:12px; display:flex; align-items:center; justify-content:center; width:52px; cursor:pointer;">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
        </div>"""
html = html.replace(product_old, product_new)

inv_old = """          <div style="position:relative; background:var(--bk3); border:1px solid rgba(255,255,255,0.08); border-radius:12px; display:flex; align-items:center; justify-content:center; width:52px; cursor:pointer;">
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
          </div>"""

inv_new = """          <div onclick="openGlobalFilter('inv')" style="position:relative; background:var(--bk3); border:1px solid rgba(255,255,255,0.08); border-radius:12px; display:flex; align-items:center; justify-content:center; width:52px; cursor:pointer;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"></polygon></svg>
          </div>"""
html = html.replace(inv_old, inv_new)

# Insert global-filter-modal HTML right before </body>
modal_html = """  <!-- GLOBAL FILTER MODAL -->
  <div class="cicilan-overlay" id="global-filter-modal" onclick="if(event.target===this)closeGlobalFilter()">
    <div class="cicilan-sheet" style="max-height: 85vh; display:flex; flex-direction:column;">
      <h3 id="gf-title" style="margin-top:0; font-size:16px; color:#fff; margin-bottom:16px;">Filter</h3>
      <div style="flex:1; overflow-y:auto; padding-right:4px;">
        <div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px;" id="gf-chips">
          <!-- Chips injected here -->
        </div>
      </div>
      <button class="btn-secondary" onclick="closeGlobalFilter()" style="margin-top:0;">Tutup</button>
    </div>
  </div>
</body>"""
html = html.replace('</body>', modal_html)

# Add Global Filter JS right before </script></body>
js_logic = """
    // GLOBAL FILTER MODAL LOGIC
    function openGlobalFilter(type) {
      const modal = document.getElementById('global-filter-modal');
      const title = document.getElementById('gf-title');
      const chipsContainer = document.getElementById('gf-chips');
      chipsContainer.innerHTML = '';
      
      let options = [];
      let currentVal = '';

      if (type === 'history') {
        title.textContent = 'Filter Status Pembayaran';
        currentVal = currentHistoryStatusFilter;
        options = [
          { val: 'all', label: 'Semua Status' },
          { val: 'lunas', label: 'Lunas' },
          { val: 'dp', label: 'DP' },
          { val: 'belum_bayar', label: 'Belum Bayar' },
          { val: 'belum_lunas', label: 'Semua Piutang' }
        ];
      } else if (type === 'product') {
        title.textContent = 'Filter Merek Produk';
        currentVal = currentProductBrandFilter;
        const uniqueBrands = new Set(products.map(p => p.brand).filter(b => b));
        const sortedBrands = Array.from(uniqueBrands).sort();
        options = [{ val: 'All', label: 'Semua Brand' }];
        sortedBrands.forEach(b => options.push({ val: b, label: b }));
      } else if (type === 'inv') {
        title.textContent = 'Filter Merek Inventori';
        currentVal = currentInventorySelectBrandFilter;
        options = [
          { val: 'All', label: 'Semua Brand' },
          { val: 'Samsung', label: 'Samsung' },
          { val: 'Apple', label: 'iPhone' },
          { val: 'Xiaomi', label: 'Xiaomi' },
          { val: 'OPPO', label: 'OPPO' },
          { val: 'Vivo', label: 'Vivo' },
          { val: 'Realme', label: 'Realme' },
          { val: 'Poco', label: 'Poco' },
          { val: 'iQOO', label: 'iQOO' }
        ];
      }

      options.forEach(opt => {
        const btn = document.createElement('button');
        btn.className = `chip ${currentVal === opt.val ? 'active' : ''}`;
        btn.textContent = opt.label;
        btn.onclick = () => selectGlobalFilter(type, opt.val);
        chipsContainer.appendChild(btn);
      });

      modal.classList.add('show');
    }

    function closeGlobalFilter() {
      document.getElementById('global-filter-modal').classList.remove('show');
    }

    function selectGlobalFilter(type, val) {
      if (type === 'history') {
        currentHistoryStatusFilter = val;
        renderHistoryList();
      } else if (type === 'product') {
        currentProductBrandFilter = val;
        renderProductList();
      } else if (type === 'inv') {
        currentInventorySelectBrandFilter = val;
        renderInventorySelectList();
      }
      closeGlobalFilter();
    }
  </script>"""
html = html.replace('  </script>', js_logic)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done!')
