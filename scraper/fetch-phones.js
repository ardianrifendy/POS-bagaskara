const https = require('https');
const fs = require('fs');

const BRANDS = {
  'Samsung': 'samsung-phones-9.php',
  'Apple': 'apple-phones-48.php',
  'Xiaomi': 'xiaomi-phones-80.php',
  'OPPO': 'oppo-phones-82.php',
  'Vivo': 'vivo-phones-98.php',
  'Realme': 'realme-phones-118.php',
  'Infinix': 'infinix-phones-119.php',
  'Tecno': 'tecno-phones-120.php',
  'Nothing': 'nothing-phones-128.php',
  'Honor': 'honor-phones-121.php',
  'Asus': 'asus-phones-46.php',
  'Poco': 'poco-phones-132.php',
  'iQOO': 'iqoo-phones-127.php',
};

function fetch(url) {
  return new Promise((resolve, reject) => {
    https.get(url, {
      headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120' }
    }, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => resolve(d));
    }).on('error', reject);
  });
}

function parseList(html, brand) {
  const phones = [];
  // Pattern: <li><a href="..."><img ... title="Samsung Galaxy S26 Ultra ... 256 GB storage, 12 GB RAM..."><strong><span>Galaxy S26 Ultra</span></strong></a></li>
  const regex = /<li>\s*<a href="([^"]+)">\s*<img[^>]*title="([^"]*)"[^>]*>\s*<strong>\s*<span>([^<]+)<\/span>/gi;

  let m;
  while ((m = regex.exec(html)) !== null) {
    const url = m[1];
    const title = m[2]; // Contains full description with specs
    const shortName = m[3].trim();

    // Parse specs from title attribute
    const storage = title.match(/(\d+)\s*GB storage/i);
    const ram = title.match(/(\d+)\s*GB RAM/i);
    const battery = title.match(/(\d+)\s*mAh/i);
    const display = title.match(/(\d+\.?\d*)[^d]*display/i);
    const chipset = title.match(/,\s*([A-Za-z][\w\s]+\d[\w\s]*)\s*chipset/i);

    phones.push({
      brand,
      model: shortName,
      fullName: `${brand} ${shortName}`,
      storage: storage ? storage[1] + ' GB' : null,
      ram: ram ? ram[1] + ' GB' : null,
      battery: battery ? battery[1] + ' mAh' : null,
      display: display ? display[1] + '"' : null,
      chipset: chipset ? chipset[1].trim() : null,
      gsmarenaUrl: `https://www.gsmarena.com/${url}`,
    });
  }
  return phones;
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function main() {
  console.log('=== BagaskaraCell Phone Catalog Builder ===\n');
  const allPhones = [];

  for (const [brand, slug] of Object.entries(BRANDS)) {
    process.stdout.write(`📱 ${brand}...`);
    try {
      const html = await fetch(`https://www.gsmarena.com/${slug}`);
      const phones = parseList(html, brand);
      allPhones.push(...phones);
      console.log(` ${phones.length} phones`);
    } catch (e) {
      console.log(` Error: ${e.message}`);
    }
    await sleep(1200);
  }

  console.log(`\n✅ Total: ${allPhones.length} phones\n`);

  // Show sample
  console.log('Sample data:');
  allPhones.slice(0, 5).forEach(p => {
    console.log(`  ${p.fullName} | ${p.ram || '?'} RAM | ${p.storage || '?'} | ${p.battery || '?'}`);
  });

  const output = {
    generated: new Date().toISOString(),
    source: 'GSMArena',
    total: allPhones.length,
    catalog: allPhones,
  };

  const outPath = 'd:\\AntiGravity\\BagaskaraCell\\www\\phone-catalog.json';
  fs.writeFileSync(outPath, JSON.stringify(output, null, 2), 'utf8');
  console.log(`\n📁 Saved: ${outPath}`);
}

main().catch(console.error);
