with open('www/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update history-card CSS
old_card_css = """    .history-card {
      background: var(--bk2);
      border: 1px solid rgba(255,255,255,0.05);
      border-radius: 18px;
      padding: 14px;
      position: relative;
      transition: transform 0.2s ease;
    }"""

new_card_css = """    .history-card {
      background: var(--bk2);
      border: 1px solid rgba(255,255,255,0.05);
      border-radius: 18px;
      padding: 14px;
      margin-bottom: 8px;
      position: relative;
      transition: transform 0.2s ease;
    }
    .history-card:last-child {
      margin-bottom: 0;
    }"""
html = html.replace(old_card_css, new_card_css)

# 2. Add history-month-group CSS
old_header_css = """    /* HISTORY ACCORDION */
    .history-month-header {"""

new_header_css = """    /* HISTORY ACCORDION */
    .history-month-group {
      background: rgba(255,255,255,0.03);
      border: 1px solid rgba(255,255,255,0.05);
      border-radius: 18px;
      margin-bottom: 16px;
      padding: 6px;
    }
    body[data-theme*="light"] .history-month-group {
      background: rgba(0,0,0,0.03);
      border-color: rgba(0,0,0,0.05);
    }
    .history-month-header {"""
html = html.replace(old_header_css, new_header_css)

# 3. Update the HTML output in the renderHistoryList loop
old_html_output = """        const safeId = monthYear.replace(/\s+/g, '-');
        html += `
          <div class="history-month-header ${isFirst ? 'open' : ''}" onclick="toggleHistoryAccordion('${safeId}')" id="hist-hdr-${safeId}">
            <div>
              <div style="font-size:14px;">${monthYear}</div>
              <div style="font-size:11px; color:var(--gy); font-weight:400; margin-top:2px;">${data.invoices.length} Transaksi &bull; Rp ${data.total.toLocaleString('id-ID')}</div>
            </div>
            <svg class="chevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
          </div>
          <div id="hist-acc-${safeId}" class="history-acc-content ${isFirst ? 'open' : ''}">
            ${cardsHtml}
          </div>
        `;"""

new_html_output = """        const safeId = monthYear.replace(/\s+/g, '-');
        html += `
          <div class="history-month-group">
            <div class="history-month-header ${isFirst ? 'open' : ''}" onclick="toggleHistoryAccordion('${safeId}')" id="hist-hdr-${safeId}">
              <div>
                <div style="font-size:14px;">${monthYear}</div>
                <div style="font-size:11px; color:var(--gy); font-weight:400; margin-top:2px;">${data.invoices.length} Transaksi &bull; Rp ${data.total.toLocaleString('id-ID')}</div>
              </div>
              <svg class="chevron" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"></polyline></svg>
            </div>
            <div id="hist-acc-${safeId}" class="history-acc-content ${isFirst ? 'open' : ''}">
              ${cardsHtml}
            </div>
          </div>
        `;"""
html = html.replace(old_html_output, new_html_output)

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done!')
