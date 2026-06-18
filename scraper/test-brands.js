const https = require('https');
const urls = {
  'Poco': 'https://www.gsmarena.com/poco-phones-finer-101.php',
  'iQOO': 'https://www.gsmarena.com/vivo_iqoo-phones-finer-127.php',
};

function fetch(url) {
  return new Promise((ok, no) => {
    https.get(url, { headers: { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0) Chrome/120' } }, r => {
      let d = ''; r.on('data', c => d += c); r.on('end', () => ok(d));
    }).on('error', no);
  });
}

async function go() {
  for (const [brand, url] of Object.entries(urls)) {
    const html = await fetch(url);
    const title = html.match(/<title[^>]*>([^<]+)/i);
    console.log(`${brand}: Page title = ${title ? title[1] : 'unknown'}`);
    const rx = /<li>\s*<a href="([^"]+)">\s*<img[^>]*title="([^"]*)"[^>]*>\s*<strong>\s*<span>([^<]+)<\/span>/gi;
    let m, cnt = 0, samples = [];
    while ((m = rx.exec(html)) !== null) {
      cnt++;
      if (cnt <= 3) samples.push(m[3].trim());
    }
    console.log(`  Found: ${cnt} phones`);
    if (samples.length) console.log(`  Samples: ${samples.join(', ')}`);
    console.log('');
  }
}
go();
