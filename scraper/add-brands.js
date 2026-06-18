const https = require('https');
const fs = require('fs');

// Correct GSMArena brand slugs - verified  
const BRANDS_TO_ADD = [
  { brand: 'Poco', url: 'https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName=poco' },
  { brand: 'iQOO', url: 'https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName=iqoo' },
];

function fetch(url) {
  return new Promise((ok, no) => {
    https.get(url, { 
      headers: { 
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.gsmarena.com/',
      } 
    }, r => {
      if (r.statusCode === 301 || r.statusCode === 302) {
        return fetch(r.headers.location).then(ok).catch(no);
      }
      let d = ''; r.on('data', c => d += c); r.on('end', () => ok(d));
    }).on('error', no);
  });
}

function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function main() {
  // Load existing catalog
  const catalogPath = 'd:\\AntiGravity\\BagaskaraCell\\www\\phone-catalog.json';
  const catalog = JSON.parse(fs.readFileSync(catalogPath, 'utf8'));
  
  console.log(`Existing catalog: ${catalog.total} phones\n`);

  for (const { brand, url } of BRANDS_TO_ADD) {
    console.log(`📱 Fetching ${brand}...`);
    await sleep(3000);
    
    try {
      const html = await fetch(url);
      const title = html.match(/<title[^>]*>([^<]+)/i);
      console.log(`  Page: ${title ? title[1].trim() : 'unknown'}`);
      
      const rx = /<li>\s*<a href="([^"]+)">\s*<img[^>]*title="([^"]*)"[^>]*>\s*<strong>\s*<span>([^<]+)<\/span>/gi;
      let m;
      const phones = [];
      while ((m = rx.exec(html)) !== null) {
        const detailUrl = m[1];
        const titleAttr = m[2];
        const shortName = m[3].trim();
        
        const storage = titleAttr.match(/(\d+)\s*GB storage/i);
        const ram = titleAttr.match(/(\d+)\s*GB RAM/i);
        const battery = titleAttr.match(/(\d+)\s*mAh/i);
        const chipset = titleAttr.match(/,\s*([A-Za-z][\w\s]+\d[\w\s]*)\s*chipset/i);
        
        phones.push({
          brand,
          model: shortName,
          fullName: `${brand} ${shortName}`,
          storage: storage ? storage[1] + ' GB' : null,
          ram: ram ? ram[1] + ' GB' : null,
          battery: battery ? battery[1] + ' mAh' : null,
          display: null,
          chipset: chipset ? chipset[1].trim() : null,
          gsmarenaUrl: `https://www.gsmarena.com/${detailUrl}`,
        });
      }
      
      console.log(`  Found: ${phones.length} phones`);
      phones.slice(0, 3).forEach(p => console.log(`    - ${p.fullName} (${p.ram || '?'} / ${p.storage || '?'})`));
      
      catalog.catalog.push(...phones);
    } catch (e) {
      console.log(`  Error: ${e.message}`);
    }
  }

  catalog.total = catalog.catalog.length;
  catalog.generated = new Date().toISOString();
  
  fs.writeFileSync(catalogPath, JSON.stringify(catalog, null, 2), 'utf8');
  console.log(`\n✅ Updated catalog: ${catalog.total} phones`);
  console.log(`📁 Saved: ${catalogPath}`);
}

main().catch(console.error);
