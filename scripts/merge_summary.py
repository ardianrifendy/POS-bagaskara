import re

with open('www/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove dashboard-switcher
old_switcher = """      <!-- View Switcher -->
      <div class="dashboard-switcher">
        <button class="switcher-btn active" id="btn-dash-ringkasan" onclick="switchDashboardView('ringkasan')">Ringkasan</button>
        <button class="switcher-btn" id="btn-dash-laporan" onclick="switchDashboardView('laporan')">Laporan Bulanan</button>
      </div>"""
html = html.replace(old_switcher, "")

# 2. Modify dash-view-laporan div
old_laporan = """      <!-- VIEW B: LAPORAN BULANAN & PENGELUARAN -->
      <div id="dash-view-laporan" style="display: none;">
        <!-- Period Selector -->
        <div class="card" style="padding:14px 18px;">
          <div class="period-selector">"""

new_laporan = """      <!-- VIEW B: LAPORAN BULANAN & PENGELUARAN -->
      <div id="dash-view-laporan">
        <!-- Period Selector -->
        <div class="card" style="padding:14px 18px; margin-top:16px;">
          <div class="card-title" style="margin-bottom:12px; font-size:16px; border-bottom:1px solid rgba(255,255,255,0.05); padding-bottom:8px;">Laporan Bulanan</div>
          <div class="period-selector">"""
html = html.replace(old_laporan, new_laporan)

# 3. Remove switchDashboardView function
old_func = """    function switchDashboardView(viewId) {
      const ringkasanEl = document.getElementById('dash-view-ringkasan');
      const laporanEl = document.getElementById('dash-view-laporan');
      const btnRingkasan = document.getElementById('btn-dash-ringkasan');
      const btnLaporan = document.getElementById('btn-dash-laporan');

      if (viewId === 'ringkasan') {
        ringkasanEl.style.display = 'block';
        laporanEl.style.display = 'none';
        btnRingkasan.classList.add('active');
        btnLaporan.classList.remove('active');
        updateDashboardStats();
      } else {
        ringkasanEl.style.display = 'none';
        laporanEl.style.display = 'block';
        btnRingkasan.classList.remove('active');
        btnLaporan.classList.add('active');
        renderLaporanTab();
      }
    }"""
html = html.replace(old_func, "")

with open('www/index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Done!")
