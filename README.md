# Doom Cart

See what your shopping costs the planet. Doom Cart is a one-screen dashboard that shows how everyday purchases affect climate, water and mineral reserves, which online stores emit the most, and which swaps actually help.

Built for Patch the Conference (Bright Data, San Francisco, 2026-10-24).

Live prototype: https://claude.ai/artifact/48wavgiSaiG8siKm9stEvC (private, share from the page menu)

## What it does

- **Live counters:** global purchases of 7 everyday products, ticking per second, plus days since Earth Overshoot Day.
- **Globe:** where a product's materials come from, with arcs to a US buyer.
- **Search:** type a product or paste an Amazon, Walmart, Target, Shein or Temu link to see its footprint.
- **Selling now:** real Amazon and Walmart listings with "bought in past month" badges and estimated CO₂ per month.
- **Stores:** reported emissions for Walmart, Amazon, Target, Shein, eBay and Temu.
- **Action forecast:** tick swaps (refurbished phone, plant-based burger, second-hand clothes) and see your CO₂ to 2030, then scaled to a million people.
- **Resource clocks:** when known cobalt, nickel, copper and lithium reserves run out at a chosen demand growth.
- **Receipt:** your year of shopping, against a 2.5 t yearly climate budget.

## Data

| Data | Source | File |
|---|---|---|
| Per-item CO₂, water, cobalt | Apple product reports, ADEME, Poore & Nemecek 2018, Water Footprint Network, MIT | `data/footprints.json` |
| Global units per year | IDC, Omdia, UNEP, USDA, World Footwear Yearbook | `data/footprints.json` |
| Store emissions | Each company's 2025 sustainability report | `data/retailers.json` |
| Mineral reserves | USGS Mineral Commodity Summaries 2026 | `data/footprints.json` |
| Live listings | Amazon and Walmart US search pages, scraped with Bright Data | `data/live.json` |
| Overshoot date | Global Footprint Network, 2026 | in page |

Known weak spots: the burger uses the global beef average (US beef is lower), coffee CO₂ and water assume different doses per cup, sneakers and laptops have no water figure, and cobalt per device comes from 2016 reporting. Store totals are not like-for-like because each company counts its supply chain differently.

## Source APIs and endpoints

### Live data

| API | Endpoint | Used for |
|---|---|---|
| Bright Data Web Unlocker | `POST https://api.brightdata.com/request` with `{"zone": "mcp_unlocker", "url": ..., "format": "raw"}` and `Authorization: Bearer <key>` | Fetching store search pages without bot blocks |
| Amazon US search (via Bright Data) | `https://www.amazon.com/s?k=<query>` | Listings, prices, ratings, "bought in past month" badges, sustainability labels |
| Walmart US search (via Bright Data) | `https://www.walmart.com/search?q=<query>` (parsed from the page's `__NEXT_DATA__` JSON) | Listings, prices, review counts, "bought since yesterday" badges |
| claude.ai artifact database | `db` capability, collections `live` and `meta` | Serving the latest scrape to the page |

Search queries per category: coffee pods, bottled water, beef burger patties, t-shirt, running shoes, unlocked smartphone, laptop.

### Reference data

| Figure | Source |
|---|---|
| Coffee CO₂ | Nab & Maslin 2020, via UCL: https://www.ucl.ac.uk/news/2021/jan/analysis-heres-carbon-cost-your-daily-coffee-and-how-make-it-climate-friendly |
| Coffee, burger, T-shirt water | Water Footprint Network product gallery: https://tools.waterfootprint.org/product-gallery/ |
| Coffee and beef volumes | USDA FAS PSD circulars: https://apps.fas.usda.gov/psdonline/circulars/coffee.pdf, https://apps.fas.usda.gov/psdonline/circulars/livestock_poultry.pdf |
| Bottle and T-shirt CO₂, tap water swap | ADEME Impact CO2: https://impactco2.fr/outils/boisson/eauenbouteille, https://impactco2.fr/outils/habillement/tshirtencoton, https://impactco2.fr/outils/boisson/eaudurobinet |
| Bottle water | Pacific Institute: https://pacinst.org/wp-content/uploads/2013/02/bottled_water_and_energy.pdf |
| Bottle volume | UNEP: https://www.unep.org/news-and-stories/story/our-planet-drowning-plastic-pollution |
| Burger CO₂ | Poore & Nemecek 2018, via Our World in Data: https://ourworldindata.org/grapher/ghg-per-kg-poore |
| Plant-based swap | University of Michigan CSS: https://css.umich.edu/publications/research-publications/beyond-meats-beyond-burger-life-cycle-assessment-detailed |
| Clothing volume | McKinsey: https://www.mckinsey.com/capabilities/sustainability/our-insights/style-thats-sustainable-a-new-fast-fashion-formula |
| Second-hand swap | Klooster et al. 2024: https://doi.org/10.55845/ZZUG7076 |
| Sneaker CO₂ | MIT: https://news.mit.edu/2013/footwear-carbon-footprint-0522 |
| Footwear volume | World Footwear: https://www.worldfootwear.com/news/246-billion-pairs-global-footwear-production-in-2025/11690.html |
| Phone CO₂ | Apple iPhone 17 report: https://www.apple.com/environment/pdf/products/iphone/iPhone_17_PER_Sept2025.pdf |
| Phone water | Friends of the Earth / Trucost: https://www.business-humanrights.org/en/latest-news/full-report-18/ |
| Cobalt per device | Washington Post: https://www.washingtonpost.com/graphics/business/batteries/congo-cobalt-mining-for-lithium-ion-battery/ |
| Phone volume | IDC: https://www.idc.com/resource-center/press-releases/q425mobilephonetop5/ |
| Refurbished swaps | ADEME 2022: https://librairie.ademe.fr/economie-circulaire-et-dechets/5833-assessment-of-the-environmental-impact-of-a-set-of-refurbished-products.html |
| Laptop CO₂ | Apple MacBook Air M5 report: https://www.apple.com/environment/pdf/products/notebooks/MacBook_Air_M5_PER_Mar2026.pdf |
| Laptop volume | Omdia: https://omdia.tech.informa.com/pr/2025/dec/global-pc-shipments-grew-9percent-in-2025-but-memory-and-storage-supply-issues-threaten-2026-outlook |
| Car CO₂ per year and per km | US EPA: https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle |
| Litres per shower | EPA WaterSense: https://www.epa.gov/sites/default/files/2017-01/documents/ws-products-support-statement-showerheads.pdf |
| 2.5 t climate budget | Hot or Cool Institute: https://hotorcool.org/publications/1-5-degree-lifestyles-towards-a-fair-consumption-space-for-all/ |
| Mineral reserves and production | USGS MCS 2026: https://pubs.usgs.gov/periodicals/mcs2026/ (cobalt, nickel, copper, lithium PDFs) |
| Overshoot Day 2026 | Global Footprint Network: https://footprintnetwork.org/2026/06/05/announcement-earth-overshoot-day-2026-falls-on-july-30/ |

### Store emissions reports

| Store | Report |
|---|---|
| Amazon | https://sustainability.aboutamazon.com/2025-amazon-sustainability-report.pdf |
| Walmart | https://corporate.walmart.com/content/dam/corporate/documents/esgreport/2026/FY2026-Walmart-ESG-Report.pdf |
| Target | https://corporate.target.com/getmedia/059a4de0-74c8-42fa-b590-c44a7b724b6c/2026-Sustainability-and-Governance-Report-Appendix.pdf |
| Shein | https://cdn.sanity.io/files/44sbcf22/production/c03664f8e909ab0b86cfa90012999d570dce1457.pdf |
| eBay | https://static.ebayinc.com/static/assets/Uploads/Documents/eBay-Impact-2025-Report.pdf |
| Temu (PDD 20-F) | https://www.sec.gov/Archives/edgar/data/1737806/000110465926050727/pdd-20251231x20f.htm |

### Front-end libraries (CDN)

- D3 7.9.0: `https://cdnjs.cloudflare.com/ajax/libs/d3/7.9.0/d3.min.js`
- d3-sankey 0.12.3: `https://cdn.jsdelivr.net/npm/d3-sankey@0.12.3/dist/d3-sankey.min.js`
- topojson-client 3.1.0: `https://cdn.jsdelivr.net/npm/topojson-client@3.1.0/dist/topojson-client.min.js`
- world-atlas 2.0.2 (inlined): `https://cdn.jsdelivr.net/npm/world-atlas@2.0.2/countries-110m.json`
- Fonts: Google Fonts (Chakra Petch, IBM Plex Sans, IBM Plex Mono)

### Planned

- OpenAI API: classify any scraped product title into a footprint category.
- FalkorDB: graph of product, material, source country and store.

## Files

```
doom-cart/
  doom-src.html        page source (world map is a __WORLD__ placeholder)
  cart-doom.html       built page with the map inlined
  data/                footprints, retailers, live scrape, world map
  scripts/
    scrape_stores.py   scrape Amazon + Walmart via Bright Data
    to_db.py           turn the scrape into database documents
    build_footprints.py  rebuild data/footprints.json from cited figures
```

## Run it

Requires Python 3.11 with `beautifulsoup4` and `lxml`, and a Bright Data API key with a Web Unlocker zone.

1. Add your key to a `.env` file in the repo root (it is gitignored):
   ```
   BRIGHTDATA_API_KEY=your-key
   ```
2. Scrape the stores:
   ```
   python scripts/scrape_stores.py .env data/scrape
   ```
   Add `--reparse` to re-read saved pages without new requests.
3. Build the database documents:
   ```
   python scripts/to_db.py data/scrape/live.json data/db_batch.json
   ```
4. Build the page by replacing `__WORLD__` in `doom-src.html` with the contents of `data/countries-110m.json`, then open `cart-doom.html` in a browser.

The "Selling now" tab reads from the artifact's page database, so it only fills in when the page is opened on claude.ai. Opened as a local file, it shows a notice instead.

## Stack

D3 7.9, d3-sankey, topojson-client, world-atlas 110m, Bright Data Web Unlocker. No build step.

## Sponsor tools

- **Bright Data:** live store listings and sales badges.
- **OpenAI** (planned): sort any scraped product into a footprint category.
- **FalkorDB** (planned): graph of product, material, country and store.
