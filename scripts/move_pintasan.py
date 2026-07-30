with open('www/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# The exact block to move
block_to_move = """
        <div class="card">
          <div class="card-title">Pintasan Cepat</div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
            <button class="btn-primary" onclick="switchTab('form'); resetInvoiceForm();" style="padding: 12px; font-size:12.5px;">
              ➕ Buat Invoice Baru
            </button>
            <button class="btn-secondary" onclick="switchTab('history')" style="padding: 12px; font-size:12.5px;">
              📄 Riwayat Transaksi
            </button>
          </div>
        </div>
"""

# Wait, let's just make sure we find the exact text in the file
start_idx = html.find('<div class="card">\n          <div class="card-title">Pintasan Cepat</div>')

if start_idx != -1:
    end_idx = html.find('</div>\n        </div>', start_idx) + len('</div>\n        </div>')
    
    # Extract the block
    actual_block = html[start_idx:end_idx]
    
    # Remove it from current location
    html = html[:start_idx] + html[end_idx:]
    
    # Insert it at the top of dash-view-ringkasan
    insert_target = '<div id="dash-view-ringkasan">'
    insert_idx = html.find(insert_target) + len(insert_target)
    
    html = html[:insert_idx] + '\n' + actual_block + '\n' + html[insert_idx:]
    
    with open('www/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully moved Pintasan Cepat to top")
else:
    print("Could not find Pintasan Cepat block")
