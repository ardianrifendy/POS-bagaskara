with open('www/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add currentProductStatusFilter declaration
old_decl = """    let currentProductBrandFilter = 'All';"""
new_decl = """    let currentProductBrandFilter = 'All';
    let currentProductStatusFilter = 'all';"""
html = html.replace(old_decl, new_decl)

# 2. Add status filtering logic
old_filter = """      const filtered = products.filter(p => {
        // Brand filter
        if (currentProductBrandFilter !== 'All' && p.brand !== currentProductBrandFilter) return false;
        
        // Search query"""
new_filter = """      const filtered = products.filter(p => {
        // Brand filter
        if (currentProductBrandFilter !== 'All' && p.brand !== currentProductBrandFilter) return false;
        
        // Status filter
        if (currentProductStatusFilter === 'terjual' && p.status !== 'Terjual') return false;
        if (currentProductStatusFilter === 'belum_terjual' && p.status === 'Terjual') return false;
        
        // Search query"""
html = html.replace(old_filter, new_filter)

# 3. Modify openGlobalFilter for product type
old_modal = """      } else if (type === 'product') {
        title.textContent = 'Filter Merek Produk';
        currentVal = currentProductBrandFilter;
        const uniqueBrands = new Set(products.map(p => p.brand).filter(b => b));
        const sortedBrands = Array.from(uniqueBrands).sort();
        options = [{ val: 'All', label: 'Semua Brand' }];
        sortedBrands.forEach(b => options.push({ val: b, label: b }));
      } else if (type === 'inv') {"""

new_modal = """      } else if (type === 'product') {
        title.textContent = 'Filter Produk & Stok';
        chipsContainer.innerHTML = '';
        
        // STATUS SECTION
        const statusLbl = document.createElement('div');
        statusLbl.style = 'font-size:12px; color:var(--gy); margin-bottom:8px; font-weight:700;';
        statusLbl.textContent = 'STATUS STOK';
        chipsContainer.appendChild(statusLbl);
        
        const statusDiv = document.createElement('div');
        statusDiv.style = 'display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px;';
        const statuses = [
          { val: 'all', label: 'Semua Status' },
          { val: 'belum_terjual', label: 'Tersedia' },
          { val: 'terjual', label: 'Terjual' }
        ];
        statuses.forEach(opt => {
          const btn = document.createElement('button');
          btn.className = `chip ${currentProductStatusFilter === opt.val ? 'active' : ''}`;
          btn.textContent = opt.label;
          btn.onclick = () => {
             currentProductStatusFilter = opt.val;
             renderProductList();
             Array.from(statusDiv.children).forEach(c => c.classList.remove('active'));
             btn.classList.add('active');
          };
          statusDiv.appendChild(btn);
        });
        chipsContainer.appendChild(statusDiv);

        // BRAND SECTION
        const brandLbl = document.createElement('div');
        brandLbl.style = 'font-size:12px; color:var(--gy); margin-bottom:8px; font-weight:700;';
        brandLbl.textContent = 'MEREK PRODUK';
        chipsContainer.appendChild(brandLbl);

        const brandDiv = document.createElement('div');
        brandDiv.style = 'display:flex; flex-wrap:wrap; gap:8px; margin-bottom:20px;';
        
        const uniqueBrands = new Set(products.map(p => p.brand).filter(b => b));
        const sortedBrands = Array.from(uniqueBrands).sort();
        const brandOpts = [{ val: 'All', label: 'Semua Brand' }];
        sortedBrands.forEach(b => brandOpts.push({ val: b, label: b }));

        brandOpts.forEach(opt => {
          const btn = document.createElement('button');
          btn.className = `chip ${currentProductBrandFilter === opt.val ? 'active' : ''}`;
          btn.textContent = opt.label;
          btn.onclick = () => {
             currentProductBrandFilter = opt.val;
             renderProductList();
             Array.from(brandDiv.children).forEach(c => c.classList.remove('active'));
             btn.classList.add('active');
          };
          brandDiv.appendChild(btn);
        });
        chipsContainer.appendChild(brandDiv);

        modal.classList.add('show');
        return;
      } else if (type === 'inv') {"""
html = html.replace(old_modal, new_modal)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done!')
