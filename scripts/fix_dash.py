import sys

def main():
    with open('www/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Inject call in updateDashboardStats
    if 'renderDashboardChart();' not in html.split('function updateDashboardStats() {')[1]:
        html = html.replace('function updateDashboardStats() {', 'function updateDashboardStats() {\n      renderDashboardChart();')
        print("Called renderDashboardChart inside updateDashboardStats")
        
    chart_js = """
    function renderDashboardChart() {
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
        
        // adjust for local timezone offset for accurate YYYY-MM-DD
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

      // Render bars
      for (let i = 0; i < 7; i++) {
        const percent = Math.max((totals[i] / maxTotal) * 100, 2); // min 2% so it's visible
        const formattedTotal = totals[i].toLocaleString('id-ID');
        
        const col = document.createElement('div');
        col.className = 'chart-col';
        col.innerHTML = `
          <div class="chart-bar-wrapper">
            <div class="chart-val-tooltip">Rp ${formattedTotal}</div>
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
    if 'function renderDashboardChart' not in html:
        html = html.replace('function updateDashboardStats() {', chart_js + '\n    function updateDashboardStats() {')
        print("Inserted renderDashboardChart function")

    with open('www/index.html', 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    main()
