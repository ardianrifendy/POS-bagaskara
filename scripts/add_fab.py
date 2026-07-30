with open('www/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Delete Pintasan Cepat (lines 2184 - 2194 approx)
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if '<div class="card-title">Pintasan Cepat</div>' in line:
        # the card wrapper is at i-1
        start_idx = i - 1
        break
if start_idx != -1:
    for i in range(start_idx, len(lines)):
        if '</div>' in lines[i]:
            # we need to find the matching closing div for the card
            # Pintasan Cepat has:
            # <div class="card">
            #   <div class="card-title">Pintasan Cepat</div>
            #   <div style="...">
            #     <button> ... </button>
            #     <button> ... </button>
            #   </div>
            # </div>
            pass
    # We know the exact lines from previous check: 2184 to 2194
    # But let's be dynamic, it spans 11 lines
    end_idx = start_idx + 11
    del lines[start_idx:end_idx]

# 2. Add CSS
css_to_add = """
    .fab-invoice {
      position: fixed;
      bottom: 90px;
      right: 20px;
      width: 56px;
      height: 56px;
      background: var(--gn);
      color: #111;
      border-radius: 16px;
      display: flex;
      justify-content: center;
      align-items: center;
      box-shadow: 0 6px 20px rgba(34, 197, 94, 0.4);
      z-index: 400;
      cursor: pointer;
      transition: transform 0.2s, background 0.2s;
    }
    .fab-invoice:active {
      transform: scale(0.92);
      background: #1da44d;
    }
    body[data-theme*="light"] .fab-invoice {
      box-shadow: 0 6px 20px rgba(34, 197, 94, 0.5);
      color: #fff;
    }
    .fab-invoice svg {
      width: 26px;
      height: 26px;
    }
"""
for i, line in enumerate(lines):
    if '.nav-item {' in line:
        lines.insert(i, css_to_add)
        break

# 3. Add JS in switchTab
for i, line in enumerate(lines):
    if 'function switchTab(tabId) {' in line:
        js_to_add = """      const fab = document.getElementById('fab-invoice');
      if (fab) {
        if (tabId === 'form') fab.style.display = 'none';
        else fab.style.display = 'flex';
      }
"""
        lines.insert(i+1, js_to_add)
        break

# 4. Add HTML for FAB right before <div class="bottom-nav">
html_to_add = """  <!-- FAB INVOICE -->
  <div class="fab-invoice" id="fab-invoice" onclick="switchTab('form'); resetInvoiceForm();">
    <svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="1.5">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
      <line x1="9" y1="10" x2="15" y2="10" stroke="#22c55e" stroke-width="2.5" stroke-linecap="round"></line>
      <line x1="12" y1="7" x2="12" y2="13" stroke="#22c55e" stroke-width="2.5" stroke-linecap="round"></line>
    </svg>
  </div>
"""
for i, line in enumerate(lines):
    if '<div class="bottom-nav">' in line:
        lines.insert(i, html_to_add)
        break

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Done!')
