const fs = require('fs');
const catalogPath = 'd:\\AntiGravity\\BagaskaraCell\\www\\phone-catalog.json';
const catalog = JSON.parse(fs.readFileSync(catalogPath, 'utf8'));

const poco = [
  { brand:'Poco', model:'X7 Pro 5G', fullName:'Poco X7 Pro 5G', storage:'256 GB', ram:'8 GB', battery:'6550 mAh', display:'6.67"', chipset:'Dimensity 8400 Ultra', gsmarenaUrl:'' },
  { brand:'Poco', model:'X7 5G', fullName:'Poco X7 5G', storage:'256 GB', ram:'8 GB', battery:'5500 mAh', display:'6.67"', chipset:'Dimensity 7300 Ultra', gsmarenaUrl:'' },
  { brand:'Poco', model:'M7 Pro 5G', fullName:'Poco M7 Pro 5G', storage:'256 GB', ram:'8 GB', battery:'5110 mAh', display:'6.67"', chipset:'Dimensity 7300 Ultra', gsmarenaUrl:'' },
  { brand:'Poco', model:'M7 5G', fullName:'Poco M7 5G', storage:'256 GB', ram:'8 GB', battery:'5110 mAh', display:'6.67"', chipset:'Helio G100 Ultra', gsmarenaUrl:'' },
  { brand:'Poco', model:'F6 Pro', fullName:'Poco F6 Pro', storage:'512 GB', ram:'12 GB', battery:'5000 mAh', display:'6.67"', chipset:'Snapdragon 8s Gen 3', gsmarenaUrl:'' },
  { brand:'Poco', model:'F6', fullName:'Poco F6', storage:'256 GB', ram:'8 GB', battery:'5000 mAh', display:'6.67"', chipset:'Snapdragon 8s Gen 3', gsmarenaUrl:'' },
  { brand:'Poco', model:'F5 Pro', fullName:'Poco F5 Pro', storage:'256 GB', ram:'12 GB', battery:'5160 mAh', display:'6.67"', chipset:'Snapdragon 8+ Gen 1', gsmarenaUrl:'' },
  { brand:'Poco', model:'F5', fullName:'Poco F5', storage:'256 GB', ram:'8 GB', battery:'5000 mAh', display:'6.67"', chipset:'Snapdragon 7+ Gen 2', gsmarenaUrl:'' },
  { brand:'Poco', model:'X6 Pro 5G', fullName:'Poco X6 Pro 5G', storage:'512 GB', ram:'12 GB', battery:'5000 mAh', display:'6.67"', chipset:'Dimensity 8300 Ultra', gsmarenaUrl:'' },
  { brand:'Poco', model:'X6 5G', fullName:'Poco X6 5G', storage:'256 GB', ram:'8 GB', battery:'5100 mAh', display:'6.67"', chipset:'Snapdragon 7s Gen 2', gsmarenaUrl:'' },
  { brand:'Poco', model:'X5 Pro 5G', fullName:'Poco X5 Pro 5G', storage:'256 GB', ram:'8 GB', battery:'5000 mAh', display:'6.67"', chipset:'Snapdragon 778G', gsmarenaUrl:'' },
  { brand:'Poco', model:'C75', fullName:'Poco C75', storage:'256 GB', ram:'8 GB', battery:'5160 mAh', display:'6.88"', chipset:'Helio G81 Ultra', gsmarenaUrl:'' },
  { brand:'Poco', model:'C65', fullName:'Poco C65', storage:'256 GB', ram:'8 GB', battery:'5000 mAh', display:'6.74"', chipset:'Helio G85', gsmarenaUrl:'' },
  { brand:'Poco', model:'C61', fullName:'Poco C61', storage:'128 GB', ram:'4 GB', battery:'5000 mAh', display:'6.71"', chipset:'Helio G36', gsmarenaUrl:'' },
  { brand:'Poco', model:'M6 Pro', fullName:'Poco M6 Pro', storage:'256 GB', ram:'8 GB', battery:'5000 mAh', display:'6.67"', chipset:'Helio G99 Ultra', gsmarenaUrl:'' },
];

const iqoo = [
  { brand:'iQOO', model:'Z11 Pro 5G', fullName:'iQOO Z11 Pro 5G', storage:'256 GB', ram:'8 GB', battery:'6000 mAh', display:'6.78"', chipset:'Dimensity 8400', gsmarenaUrl:'' },
  { brand:'iQOO', model:'Z11 5G', fullName:'iQOO Z11 5G', storage:'256 GB', ram:'8 GB', battery:'6000 mAh', display:'6.78"', chipset:'Dimensity 7300', gsmarenaUrl:'' },
  { brand:'iQOO', model:'Neo 10 Pro', fullName:'iQOO Neo 10 Pro', storage:'256 GB', ram:'12 GB', battery:'6100 mAh', display:'6.78"', chipset:'Dimensity 9400', gsmarenaUrl:'' },
  { brand:'iQOO', model:'Neo 10', fullName:'iQOO Neo 10', storage:'256 GB', ram:'8 GB', battery:'6100 mAh', display:'6.78"', chipset:'Snapdragon 8s Gen 3', gsmarenaUrl:'' },
  { brand:'iQOO', model:'Z9 Turbo+', fullName:'iQOO Z9 Turbo+', storage:'256 GB', ram:'8 GB', battery:'6000 mAh', display:'6.78"', chipset:'Dimensity 8300', gsmarenaUrl:'' },
  { brand:'iQOO', model:'Z9s Pro', fullName:'iQOO Z9s Pro', storage:'256 GB', ram:'8 GB', battery:'5500 mAh', display:'6.78"', chipset:'Snapdragon 7 Gen 3', gsmarenaUrl:'' },
  { brand:'iQOO', model:'Z9s', fullName:'iQOO Z9s', storage:'128 GB', ram:'8 GB', battery:'5500 mAh', display:'6.67"', chipset:'Dimensity 7300', gsmarenaUrl:'' },
  { brand:'iQOO', model:'Z9x', fullName:'iQOO Z9x', storage:'128 GB', ram:'6 GB', battery:'6000 mAh', display:'6.72"', chipset:'Snapdragon 6 Gen 1', gsmarenaUrl:'' },
  { brand:'iQOO', model:'Neo 9 Pro', fullName:'iQOO Neo 9 Pro', storage:'256 GB', ram:'8 GB', battery:'5160 mAh', display:'6.78"', chipset:'Snapdragon 8 Gen 2', gsmarenaUrl:'' },
  { brand:'iQOO', model:'Z9 Lite 5G', fullName:'iQOO Z9 Lite 5G', storage:'128 GB', ram:'4 GB', battery:'5000 mAh', display:'6.56"', chipset:'Dimensity 6300', gsmarenaUrl:'' },
];

catalog.catalog.push(...poco, ...iqoo);
catalog.total = catalog.catalog.length;
catalog.generated = new Date().toISOString();

fs.writeFileSync(catalogPath, JSON.stringify(catalog, null, 2), 'utf8');

// Count per brand
const brands = {};
catalog.catalog.forEach(p => { brands[p.brand] = (brands[p.brand] || 0) + 1; });
console.log('\n✅ Katalog diperbarui!\n');
console.log('Per merek:');
Object.entries(brands).sort((a,b) => b[1] - a[1]).forEach(([b,c]) => console.log(`  ${b}: ${c}`));
console.log(`\nTotal: ${catalog.total} phones`);
