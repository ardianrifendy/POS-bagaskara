import sys

def main():
    with open('www/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Remove "Total Piutang" and "Pelanggan Berhutang" cards
    piutang_start = html.find('<div class="stat-card" style="border-color: rgba(239,68,68,0.25);">')
    if piutang_start != -1:
        # Find the end of these two cards.
        # It's right before <div class="card">\n          <div class="card-title" data-i18n="Penjualan 7 Hari Terakhir">
        chart_start = html.find('<div class="card">\n          <div class="card-title" data-i18n="Penjualan 7 Hari Terakhir">')
        if chart_start != -1:
            html = html[:piutang_start] + html[chart_start:]
            print("Removed Piutang cards")

    # 2. Update CSS for Chart Tooltip
    old_tooltip_css = """    .chart-val-tooltip {
      position: absolute;
      top: -22px;
      font-size: 9px;
      font-weight: 700;
      color: #fff;
      background: var(--bk);
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid rgba(255,255,255,0.1);
      opacity: 0;
      transition: opacity 0.2s;
      pointer-events: none;
      white-space: nowrap;
      z-index: 5;
    }
    .chart-col:hover .chart-val-tooltip, .chart-col:active .chart-val-tooltip {
      opacity: 1;
    }"""
    
    new_tooltip_css = """    .chart-y-axis {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 100%;
      padding-right: 8px;
      border-right: 1px solid rgba(255,255,255,0.1);
      font-size: 9px;
      color: var(--gy);
      text-align: right;
      min-width: 45px;
    }
    .chart-val-tooltip {
      position: absolute;
      bottom: 100%;
      margin-bottom: 4px;
      font-size: 8px;
      font-weight: 700;
      color: var(--gy);
      white-space: nowrap;
      z-index: 5;
      /* Rotate if needed, but horizontal might fit if it's small */
    }"""
    
    if old_tooltip_css in html:
        html = html.replace(old_tooltip_css, new_tooltip_css)
        print("Replaced tooltip CSS")
    
    # 3. Update Chart JS to generate Y-axis
    # Find the renderDashboardChart function
    js_start = html.find('function renderDashboardChart() {')
    if js_start != -1:
        js_end = html.find('function updateDashboardStats() {', js_start)
        old_js = html[js_start:js_end]
        
        new_js = """function renderDashboardChart() {
      const chartContainer = document.getElementById('dashboard-chart');
      if (!chartContainer) return;
      
      chartContainer.innerHTML = ''; // clear

      // Get last 7 days
      const days = [];
      const totals = [];
      let maxTotal = 0;
      
      // Initialize last 7 days
      for (let i = 6; i >= 0; i--) {
        const d = new Date();
        d.setDate(d.getDate() - i);
        const dateStr = d.toLocaleDateString('id-ID', { day: '2-digit', month: 'short' });
        
        // adjust for local timezone offset
        const offset = d.getTimezoneOffset() * 60000;
        const localISOTime = (new Date(d.getTime() - offset)).toISOString().split('T')[0];
        const matchDate = localISOTime;
        
        // Calculate total for this day
        let dayTotal = 0;
        database.forEach(t => {
           if (t.dateVal === matchDate && (t.paymentStatus === 'lunas' || t.paymentStatus === 'dp')) {
              dayTotal += t.grandTotal;
           }
        });
        
        days.push(dateStr);
        totals.push(dayTotal);
        if (dayTotal > maxTotal) maxTotal = dayTotal;
      }
      
      // If maxTotal is 0, make it 1 so we don't divide by 0
      if (maxTotal === 0) maxTotal = 1;

      // Render Y-Axis
      const formatAxis = (val) => {
        if(val >= 1000000) return (val/1000000).toFixed(1).replace('.0','') + 'Jt';
        if(val >= 1000) return (val/1000).toFixed(0) + 'K';
        return val;
      };
      
      const yAxis = document.createElement('div');
      yAxis.className = 'chart-y-axis';
      yAxis.innerHTML = `
        <span>${formatAxis(maxTotal)}</span>
        <span>${formatAxis(maxTotal/2)}</span>
        <span>0</span>
      `;
      chartContainer.appendChild(yAxis);

      // Render bars
      for (let i = 0; i < 7; i++) {
        const percent = Math.max((totals[i] / maxTotal) * 100, 2); // min 2% so it's visible
        const formattedTotal = formatAxis(totals[i]);
        
        const col = document.createElement('div');
        col.className = 'chart-col';
        col.innerHTML = `
          <div class="chart-bar-wrapper">
            <div class="chart-val-tooltip">${formattedTotal}</div>
            <div class="chart-bar" style="height: 0%"></div>
          </div>
          <div class="chart-label">${days[i].split(' ')[0]}</div>
        `;
        chartContainer.appendChild(col);
        
        // trigger animation
        setTimeout(() => {
          col.querySelector('.chart-bar').style.height = percent + '%';
        }, 50 + (i * 50));
      }
    }
    
    """
        html = html.replace(old_js, new_js)
        print("Replaced chart JS")

    with open('www/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    main()
