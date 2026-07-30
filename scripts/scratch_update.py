with open('d:/AntiGravity/BagaskaraCell/www/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

replacement = """    function renderHistoryList() {
      const query = document.getElementById('history-search-input').value.toLowerCase().trim();
      const container = document.getElementById('full-history-feed');
      container.innerHTML = '';

      // Filter based on search query + payment status filter
      let filtered = database.filter(inv => {
        const inInvNo = inv.invNo.toLowerCase().includes(query);
        const inCustName = inv.custName.toLowerCase().includes(query);
        const inImei = inv.items.some(item => item.imei && item.imei.toLowerCase().includes(query));
        const inItemName = inv.items.some(item => item.name.toLowerCase().includes(query));
        return inInvNo || inCustName || inImei || inItemName;
      });

      // Apply payment status filter
      if (currentHistoryStatusFilter !== 'all') {
        if (currentHistoryStatusFilter === 'belum_lunas') {
          filtered = filtered.filter(inv => (inv.paymentStatus || 'lunas') !== 'lunas');
        } else {
          filtered = filtered.filter(inv => (inv.paymentStatus || 'lunas') === currentHistoryStatusFilter);
        }
      }

      if (filtered.length === 0) {
        container.innerHTML = `<div style="text-align:center; padding:40px; color:var(--gy); font-size:13px;">Tidak menemukan transaksi cocok.</div>`;
        return;
      }

      // Sort newest to oldest
      filtered.sort((a, b) => {
        const tA = new Date(a.dateVal).getTime();
        const tB = new Date(b.dateVal).getTime();
        return tB - tA;
      });

      // Group by Month-Year
      const groups = {};
      const monthsIndo = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"];
      
      const groupKeys = [];

      filtered.forEach(inv => {
        const d = new Date(inv.dateVal);
        const monthYear = `${monthsIndo[d.getMonth()]} ${d.getFullYear()}`;
        if (!groups[monthYear]) {
          groups[monthYear] = { invoices: [], total: 0 };
          groupKeys.push(monthYear);
        }
        groups[monthYear].invoices.push(inv);
        groups[monthYear].total += inv.grandTotal;
      });

      let html = '';
      let isFirst = true;

      groupKeys.forEach(monthYear => {
        const data = groups[monthYear];
        let cardsHtml = '';
        
        data.invoices.forEach(inv => {
          const ps = inv.paymentStatus || 'lunas';
          const isDebt = ps === 'dp' || ps === 'belum_bayar';
          const debtSection = isDebt ? `
            <div class="debt-info">
              <div class="debt-info-col">
                <div class="debt-info-lbl">Sudah Dibayar</div>
                <div class="debt-info-val" style="color:#4ade80;">Rp ${(inv.amountPaid || 0).toLocaleString('id-ID')}</div>
              </div>
              <div class="debt-info-col">
                <div class="debt-info-lbl">Sisa Tagihan</div>
                <div class="debt-info-val" style="color:#f87171;">Rp ${(inv.amountRemaining || 0).toLocaleString('id-ID')}</div>
              </div>
            </div>
          ` : '';
          const cicilanBtn = isDebt ? `<button class="hc-btn" style="background:rgba(247,147,26,0.15); color:var(--or); border:1px solid rgba(247,147,26,0.3);" onclick="openCicilanModal('${inv.invNo}')">💳</button>` : '';

          cardsHtml += `
            <div class="history-card">
              <div class="hc-top">
                <div class="hc-inv">${inv.invNo}</div>
                <div class="hc-date">${inv.dateFormatted}</div>
              </div>
              <div class="hc-name" style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
                ${inv.custName}
                <span class="pay-badge ${getPayBadgeClass(ps)}">${getPayStatusLabel(ps)}</span>
              </div>
              <div class="hc-items">${inv.items.map(x => `📦 ${x.name} (x${x.qty})`).join('<br>')}</div>
              ${debtSection}
              <div class="hc-bot">
                <div class="hc-total">Rp ${inv.grandTotal.toLocaleString('id-ID')}</div>
                <div class="hc-actions">
                  ${cicilanBtn}
                  <button class="hc-btn hc-btn-wa" onclick="shareToWhatsApp('${inv.invNo}')">
                    <svg viewBox="0 0 24 24" fill="currentColor" style="width:16px;height:16px;">
                      <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L0 24l6.335-1.662c1.746.953 3.71 1.455 5.703 1.456h.004c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                    </svg>
                  </button>
                  <button class="hc-btn" onclick="openPreviewFromFeed('${inv.invNo}')">📄</button>
                  <button class="hc-btn hc-btn-del" onclick="deleteInvoiceFromHistory('${inv.invNo}')">🗑️</button>
                </div>
              </div>
            </div>
          `;
        });

        const safeId = monthYear.replace(/\s+/g, '-');
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
        `;
        isFirst = false;
      });

      container.innerHTML = html;
    }

    function toggleHistoryAccordion(safeId) {
      const content = document.getElementById('hist-acc-' + safeId);
      const header = document.getElementById('hist-hdr-' + safeId);
      
      if (content.classList.contains('open')) {
        content.classList.remove('open');
        header.classList.remove('open');
      } else {
        content.classList.add('open');
        header.classList.add('open');
      }
    }
"""

new_lines = lines[:5400] + [replacement + "\n"] + lines[5476:]

with open('d:/AntiGravity/BagaskaraCell/www/index.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Done replacing lines 5401-5476")
