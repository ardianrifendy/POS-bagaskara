const { chromium } = require('playwright');
const path = require('path');

const FILE = 'file:///D:/AntiGravity/BagaskaraCell/www/index.html';
const OUT  = 'D:/AntiGravity/BagaskaraCell/screenshots';

const TABS = [
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'history',   label: 'History' },
  { id: 'form',      label: 'Invoice' },
  { id: 'products',  label: 'Products' },
  { id: 'katalog',   label: 'Katalog' },
  { id: 'settings',  label: 'Settings' },
];

(async () => {
  const fs = require('fs');
  if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({
    viewport: { width: 390, height: 844 }, // iPhone 14 size
    deviceScaleFactor: 2,
  });
  const page = await ctx.newPage();

  await page.goto(FILE, { waitUntil: 'networkidle' });
  await page.waitForTimeout(1000);

  // Dismiss onboarding modal
  await page.evaluate(() => {
    const modal = document.getElementById('onboarding-modal');
    if (modal) modal.style.display = 'none';
  });
  await page.waitForTimeout(400);

  for (const tab of TABS) {
    // Click the nav button for this tab
    await page.evaluate((id) => {
      if (typeof switchTab === 'function') switchTab(id);
      else {
        const btn = document.getElementById(`nav-${id}`);
        if (btn) btn.click();
      }
    }, tab.id);
    await page.waitForTimeout(800);

    const file = path.join(OUT, `${tab.id}.png`);
    await page.screenshot({ path: file, fullPage: false });
    console.log(`✓ ${tab.label} → ${file}`);
  }

  // Back to dashboard for full-page scroll screenshot
  await page.evaluate(() => { if (typeof switchTab === 'function') switchTab('dashboard'); });
  await page.waitForTimeout(800);
  await page.screenshot({ path: path.join(OUT, 'dashboard_full.png'), fullPage: true });
  console.log('✓ Dashboard (full page) → screenshots/dashboard_full.png');

  await browser.close();
  console.log('\nDone! Semua screenshot tersimpan di:', OUT);
})();
