with open('www/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# renderProductBrandChips
old_render_chips = """      const container = document.getElementById('product-filter-chips');
      if (!container) return;

      container.innerHTML = '';

      // Add "Semua" chip
      const allChip = document.createElement('div');
      allChip.className = `chip ${currentProductBrandFilter === 'All' ? 'active' : ''}`;
      allChip.textContent = 'Semua';
      allChip.dataset.brand = 'All';
      allChip.onclick = () => filterProductBrand('All');
      container.appendChild(allChip);

      // Add dynamic brand chips
      sortedBrands.forEach(brand => {
        const chip = document.createElement('div');
        chip.className = `chip ${currentProductBrandFilter === brand ? 'active' : ''}`;
        chip.textContent = brand;
        chip.dataset.brand = brand;
        chip.onclick = () => filterProductBrand(brand);
        container.appendChild(chip);
      });"""

new_render_chips = """      const container = document.getElementById('product-filter-select');
      if (!container) return;

      container.innerHTML = '';

      const allOption = document.createElement('option');
      allOption.value = 'All';
      allOption.textContent = 'Semua Brand';
      container.appendChild(allOption);

      sortedBrands.forEach(brand => {
        const option = document.createElement('option');
        option.value = brand;
        option.textContent = brand;
        container.appendChild(option);
      });
      container.value = currentProductBrandFilter;"""

if old_render_chips in html:
    html = html.replace(old_render_chips, new_render_chips)
else:
    print('old_render_chips not found')

# filterProductBrand
old_filter_prod = """      function filterProductBrand(brand) {
        currentProductBrandFilter = brand;
        document.querySelectorAll('.filter-chips .chip').forEach(c => {
          if (c.dataset.brand === brand) c.classList.add('active');
          else c.classList.remove('active');
        });
        renderProductList();
      }"""

new_filter_prod = """      function filterProductBrand(brand) {
        currentProductBrandFilter = brand;
        const select = document.getElementById('product-filter-select');
        if (select) select.value = brand;
        renderProductList();
      }"""

if old_filter_prod in html:
    html = html.replace(old_filter_prod, new_filter_prod)
else:
    print('old_filter_prod not found')

# resetInventorySelectModal
old_reset_inv = """      function resetInventorySelectModal() {
        document.getElementById('inv-select-search').value = '';
        currentInvSelectBrand = 'All';
        document.querySelectorAll('#inv-select-chips .chip').forEach(c => {
          if (c.dataset.brand === 'All') c.classList.add('active');
          else c.classList.remove('active');
        });
        renderInventorySelectList();
      }"""

new_reset_inv = """      function resetInventorySelectModal() {
        document.getElementById('inv-select-search').value = '';
        currentInvSelectBrand = 'All';
        const select = document.getElementById('inv-filter-select');
        if (select) select.value = 'All';
        renderInventorySelectList();
      }"""

if old_reset_inv in html:
    html = html.replace(old_reset_inv, new_reset_inv)
else:
    print('old_reset_inv not found')

# filterInventorySelectBrand
old_filter_inv = """      function filterInventorySelectBrand(brand) {
        currentInvSelectBrand = brand;
        document.querySelectorAll('#inv-select-chips .chip').forEach(c => {
          if (c.dataset.brand === brand) c.classList.add('active');
          else c.classList.remove('active');
        });
        renderInventorySelectList();
      }"""

new_filter_inv = """      function filterInventorySelectBrand(brand) {
        currentInvSelectBrand = brand;
        const select = document.getElementById('inv-filter-select');
        if (select) select.value = brand;
        renderInventorySelectList();
      }"""

if old_filter_inv in html:
    html = html.replace(old_filter_inv, new_filter_inv)
else:
    print('old_filter_inv not found')

# filterHistoryStatus
old_filter_hist = """    function filterHistoryStatus(status) {
      currentHistoryStatusFilter = status;
      document.querySelectorAll('#history-filter-chips .chip').forEach(c => {
        if (c.dataset.hstatus === status) c.classList.add('active');
        else c.classList.remove('active');
      });
      renderHistoryList();
    }"""

new_filter_hist = """    function filterHistoryStatus(status) {
      currentHistoryStatusFilter = status;
      const select = document.getElementById('history-filter-select');
      if (select) select.value = status;
      renderHistoryList();
    }"""

if old_filter_hist in html:
    html = html.replace(old_filter_hist, new_filter_hist)
else:
    print('old_filter_hist not found')

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('JS update done!')
