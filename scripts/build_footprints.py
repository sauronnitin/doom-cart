import json
from pathlib import Path

SEC = 31_536_000
OUT = Path(__file__).resolve().parent.parent / "data" / "footprints.json"


def src(name, url, year, note):
    return {"name": name, "url": url, "year": year, "note": note}


def ps(units):
    return None if units is None else round(units / SEC, 2)


# ---- derived numbers ----
coffee_kg = 173_459_000 * 60            # USDA 2025/26 world consumption, 60-kg bags (green bean equiv.)
coffee_cups = coffee_kg / 0.018          # 18 g green coffee per cup (Nab & Maslin / UCL)
beef_kg_cwe = 60_353_000 * 1000          # USDA 2025 beef & veal consumption, carcass weight equiv.
burger_units = beef_kg_cwe / 0.113
bottle_units = 1_000_000 * 60 * 24 * 365  # UNEP: one million plastic drinking bottles per minute

UCL = "https://www.ucl.ac.uk/news/2021/jan/analysis-heres-carbon-cost-your-daily-coffee-and-how-make-it-climate-friendly"
WFN_COFFEE = "https://tools.waterfootprint.org/product-gallery/details.php?product=15"
WFN_BEEF = "https://tools.waterfootprint.org/product-gallery/details.php?product=3"
WFN_COTTON = "https://tools.waterfootprint.org/product-gallery/details.php?product=16"
USDA_COFFEE = "https://apps.fas.usda.gov/psdonline/circulars/coffee.pdf"
USDA_LIVESTOCK = "https://apps.fas.usda.gov/psdonline/circulars/livestock_poultry.pdf"
ADEME_RECON = "https://librairie.ademe.fr/economie-circulaire-et-dechets/5833-assessment-of-the-environmental-impact-of-a-set-of-refurbished-products.html"
WAPO = "https://www.washingtonpost.com/graphics/business/batteries/congo-cobalt-mining-for-lithium-ion-battery/"

products = [
    {
        "id": "coffee",
        "name": "Cup of coffee",
        "co2_kg": 0.28,
        "co2_src": src("Nab & Maslin 2020, Geo: Geography and Environment (summarised by UCL / The Conversation)", UCL, 2020,
                       "Peer-reviewed LCA synthesis, conventional Arabica from Brazil/Vietnam exported to UK; one espresso made with ~18 g green coffee, no milk, cup not included. Latte 0.55 kg. ADEME Agribalyse 3.2 gives 0.635 kg/L brewed coffee incl. packaging (about 0.16 kg per 250 ml), so the plausible range is ~0.1-0.3 kg."),
        "water_l": 132,
        "water_src": src("Water Footprint Network product gallery (Mekonnen & Hoekstra 2010/2011)", WFN_COFFEE, 2011,
                         "TOTAL water footprint (96% green, 1% blue = ~1.3 L, 3% grey) for a 125 ml cup made with 7 g roasted coffee. Global average, 1996-2005 data."),
        "cobalt_g": None,
        "cobalt_src": None,
        "global_units_per_year": round(coffee_cups),
        "per_second": ps(coffee_cups),
        "volume_src": src("USDA FAS, Coffee: World Markets and Trade (July 2026)", USDA_COFFEE, 2026,
                          "World consumption 2025/26 = 173.459 million 60-kg bags (green bean equivalent) = 10.41 Mt; divided by 18 g green coffee per cup (same dose as the CO2 figure). DERIVED. At WFN's 7 g roasted (~8.5 g green) per cup the count would be roughly double (~1.2 trillion)."),
        "swap": {"label": "Sustainably grown beans (and skip dairy milk)", "reduction_pct": 79,
                 "src": src("Nab & Maslin 2020 via UCL", UCL, 2020,
                            "Espresso falls from 0.28 to 0.06 kg CO2e with sustainably produced coffee. A reusable cup alone saves much less, because the beans dominate the footprint (estimate, no source).")},
    },
    {
        "id": "bottle",
        "name": "Single-use plastic water bottle (0.5 L PET)",
        "co2_kg": 0.16,
        "co2_src": src("ADEME Impact CO2 (Agribalyse 3.2, updated 2025-01-15), 'Eau en bouteille'", "https://impactco2.fr/outils/boisson/eauenbouteille", 2025,
                       "Cradle-to-grave 321 g CO2e per litre (packaging 58%, transport 36%), halved for 0.5 L. French market; small bottles carry more PET per litre, so likely an underestimate. Cross-check: NIH NEMS review sums resin 0.038-0.063 + bottle forming 0.034-0.046 kg per 500 ml bottle (~0.09 kg, excl. transport and chilling): https://nems.nih.gov/Documents/PETWaterBottlesEnvironmentalImpact.pdf"),
        "water_l": 1.5,
        "water_src": src("Pacific Institute, Bottled Water and Energy Fact Sheet (Gleick)", "https://pacinst.org/wp-content/uploads/2013/02/bottled_water_and_energy.pdf", 2007,
                         "BLUE (withdrawn) water: ~3 L of water used to produce 1 L of bottled water (2006 US data), scaled to 0.5 L; includes the water in the bottle. Old, US-only."),
        "cobalt_g": None,
        "cobalt_src": None,
        "global_units_per_year": bottle_units,
        "per_second": ps(bottle_units),
        "volume_src": src("UNEP, 'Our planet is drowning in plastic pollution'", "https://www.unep.org/news-and-stories/story/our-planet-drowning-plastic-pollution", 2018,
                          "'One million plastic drinking bottles are purchased every minute' = 525.6 billion/yr. Covers ALL plastic drink bottles, not only 0.5 L water. Traces to Euromonitor data (480 billion bottles in 2016, Guardian 2017)."),
        "swap": {"label": "Refill a reusable bottle with tap water", "reduction_pct": 99,
                 "src": src("ADEME Impact CO2, 'Eau du robinet'", "https://impactco2.fr/outils/boisson/eaudurobinet", 2025,
                            "Tap water 0.132 g CO2e/L vs bottled 321 g/L (>99.9% lower). Excludes making the reusable bottle itself, which is small once amortised over many refills.")},
    },
    {
        "id": "burger",
        "name": "Beef burger (113 g / quarter-pound patty)",
        "co2_kg": round(0.113 * 99.48, 2),
        "co2_src": src("Poore & Nemecek 2018, Science (via Our World in Data)", "https://ourworldindata.org/grapher/ghg-per-kg-poore", 2018,
                       "Global mean 99.48 kg CO2e per kg beef (beef herd), farm-to-retail, x 0.113 kg. Patty only, no bun. Beef from dairy herds is 33.3 kg/kg (= 3.76 kg per patty); US beef is far below the global mean, so this is the high, global-average case."),
        "water_l": round(0.113 * 15415),
        "water_src": src("Water Footprint Network product gallery (Mekonnen & Hoekstra 2012)", WFN_BEEF, 2012,
                         "TOTAL water footprint 15,415 L/kg beef (94% green, 4% blue = ~70 L per patty, 3% grey), x 0.113 kg. Mostly rain-fed feed crops and pasture."),
        "cobalt_g": None,
        "cobalt_src": None,
        "global_units_per_year": round(burger_units),
        "per_second": ps(burger_units),
        "volume_src": src("USDA FAS, Livestock and Poultry: World Markets and Trade (Oct 2026)", USDA_LIVESTOCK, 2026,
                          "World beef & veal consumption 2025 = 60.353 Mt carcass-weight equivalent, divided by 0.113 kg = quarter-pound-EQUIVALENTS of beef, not burgers actually sold. DERIVED. Carcass weight overstates edible meat (~30%), so treat as an upper bound."),
        "swap": {"label": "Plant-based burger", "reduction_pct": 90,
                 "src": src("Heller & Keoleian 2018, Univ. of Michigan CSS report CSS18-10 (commissioned by Beyond Meat)", "https://css.umich.edu/publications/research-publications/beyond-meats-beyond-burger-life-cycle-assessment-detailed", 2018,
                            "Beyond Burger vs 1/4 lb US beef, cradle-to-distribution: 90% less GHG, 46% less energy, >99% less water-scarcity impact, 93% less land.")},
    },
    {
        "id": "clothing",
        "name": "Piece of clothing (cotton T-shirt)",
        "co2_kg": 6.43,
        "co2_src": src("ADEME Impact CO2 / Base Empreinte, 'T-shirt en coton'", "https://impactco2.fr/outils/habillement/tshirtencoton", 2025,
                       "Cradle-to-grave: manufacturing 5.2 kg (81%), use (washing over 5 years) + end of life 1.23 kg. Published LCAs range ~1.7-8.8 kg. No authoritative average-garment figure exists; a crude top-down 1.2 Gt CO2e textiles production (Ellen MacArthur Foundation 2017) / ~100 billion garments (McKinsey 2016) gives ~12 kg per item (ESTIMATE, includes non-clothing textiles)."),
        "water_l": 2495,
        "water_src": src("Water Footprint Network product gallery (Mekonnen & Hoekstra 2010/2011)", WFN_COTTON, 2011,
                         "TOTAL water footprint for a 250 g cotton shirt (54% green, 33% blue = ~823 L, 13% grey). A lighter T-shirt (~150-200 g) would be proportionally lower."),
        "cobalt_g": None,
        "cobalt_src": None,
        "global_units_per_year": 100_000_000_000,
        "per_second": ps(100_000_000_000),
        "volume_src": src("McKinsey & Co., 'Style that's sustainable' (2016)", "https://www.mckinsey.com/capabilities/sustainability/our-insights/style-thats-sustainable-a-new-fast-fashion-formula", 2016,
                          "Garments produced per year 'exceeded 100 billion for the first time in 2014' (all clothing, not only T-shirts). Old; current volume is likely higher but no better primary figure was found."),
        "swap": {"label": "Buy second-hand", "reduction_pct": 42,
                 "src": src("Klooster et al. 2024, Journal of Circular Economy 2(1), doi:10.55845/ZZUG7076", "https://doi.org/10.55845/ZZUG7076", 2024,
                            "Peer-reviewed LCA of second-hand T-shirts, dresses, trousers, sweaters: 'up to 42%' lower climate impact per use within the same behaviour scenario. Benefit disappears if the item is rarely worn.")},
    },
    {
        "id": "sneaker",
        "name": "Pair of sneakers / running shoes",
        "co2_kg": 14,
        "co2_src": src("Cheah, Olivetti, Kirchain et al. 2013, Journal of Cleaner Production (MIT News summary)", "https://news.mit.edu/2013/footwear-carbon-footprint-0522", 2013,
                       "Cradle-to-grave LCA of a synthetic ASICS running shoe made in China: 14 +/- 2.7 kg CO2e (MIT News: '30 pounds'); ~2/3 from manufacturing. ADEME Impact CO2 gives 20.1 kg for 'paire de chaussures de sport' (https://impactco2.fr/outils/habillement/chaussuresdesport)."),
        "water_l": None,
        "water_src": src("none found", None, None,
                         "No credible per-pair water footprint for synthetic sneakers. WFN bovine leather is 17,093 L/kg and FoE/Trucost (2015) put a pair of LEATHER boots at ~14,500 L, but these do not apply to mostly synthetic sneakers."),
        "cobalt_g": None,
        "cobalt_src": None,
        "global_units_per_year": 24_600_000_000,
        "per_second": ps(24_600_000_000),
        "volume_src": src("APICCAPS World Footwear Yearbook 2026 (via worldfootwear.com, 2026-08-04)", "https://www.worldfootwear.com/news/246-billion-pairs-global-footwear-production-in-2025/11690.html", 2025,
                          "24.6 billion pairs of ALL footwear produced in 2025. No credible sneaker-only count found, so this is an upper bound for sneakers."),
        "swap": {"label": "Wear them twice as long (resole/repair)", "reduction_pct": 50,
                 "src": src("estimate", None, None,
                            "Estimate: use phase is negligible (MIT), so doubling wear life roughly halves emissions per year of use.")},
    },
    {
        "id": "phone",
        "name": "Smartphone",
        "co2_kg": 55,
        "manufacturing_share_pct": 77,
        "co2_src": src("Apple, iPhone 17 Product Environmental Report (Sept 2025)", "https://www.apple.com/environment/pdf/products/iphone/iPhone_17_PER_Sept2025.pdf", 2025,
                       "Life cycle (ISO 14040/44/67), 256 GB US config incl. packaging: production 77% (materials 23% + manufacturing electricity 53% + renewable-energy emissions 1%), charging over 3 yrs 18%, transport 4%, end of life <1%. 512 GB = 61 kg. Still Apple's current base iPhone (iPhone 18 PER covers Pro models only). Market average per ADEME/ARCEP 2025: 80.2 kg, 99% manufacturing (https://impactco2.fr/outils/numerique/smartphone)."),
        "water_l": 13000,
        "water_src": src("Friends of the Earth / Trucost, 'Mind your step' (May 2015)", "https://www.business-humanrights.org/en/latest-news/full-report-18/", 2015,
                         "TOTAL supply-chain water footprint, 'nearly 13 tonnes' per smartphone, about two-fifths of it grey water (pollution) from component manufacturing. Generic phone, old, model-based."),
        "cobalt_g": 7.5,
        "cobalt_src": src("Washington Post, 'The cobalt pipeline' (Frankel, 2016)", WAPO, 2016,
                          "'A smartphone battery might contain five to 10 grams of refined cobalt'; 7.5 g is the midpoint. Investigative journalism, not a lab measurement. iPhone 17 battery uses 100% recycled cobalt (Apple PER)."),
        "global_units_per_year": 1_260_000_000,
        "per_second": ps(1_260_000_000),
        "volume_src": src("IDC Worldwide Quarterly Mobile Phone Tracker, press release 2026-01-13", "https://www.idc.com/resource-center/press-releases/q425mobilephonetop5/", 2025,
                          "1.26 billion smartphones shipped worldwide in 2025 (preliminary), +1.9% YoY."),
        "swap": {"label": "Buy refurbished", "reduction_pct": 87,
                 "src": src("ADEME 2022, Assessment of the environmental impact of a set of refurbished products", ADEME_RECON, 2022,
                            "Refurbished phone used 2 yrs instead of a new one used 3 yrs avoids 24.6 kg CO2e per year = -87% climate impact per year of use (reference scenario).")},
    },
    {
        "id": "laptop",
        "name": "Laptop (13-inch)",
        "co2_kg": 119,
        "manufacturing_share_pct": 63,
        "co2_src": src("Apple, MacBook Air (M5) Product Environmental Report (Mar 2026)", "https://www.apple.com/environment/pdf/products/notebooks/MacBook_Air_M5_PER_Mar2026.pdf", 2026,
                       "Life cycle, 13-inch M5 / 16 GB / 512 GB = 119 kg CO2e (15-inch = 145 kg). Stage split is published only for the 15-inch: production 63% (materials 24% + electricity 38% + renewable 1%), use over 4 yrs 27%, transport 10%, EoL <1%; applied to the 13-inch as an approximation. Market average per ADEME/ARCEP 2025: 193 kg (14.6-inch), 95% manufacturing (https://impactco2.fr/outils/numerique/ordinateurportable)."),
        "water_l": None,
        "water_src": src("none found", None, None,
                         "No credible, citable per-laptop water footprint found (Apple PERs give no per-unit water figure)."),
        "cobalt_g": 28,
        "cobalt_src": src("Washington Post, 'The cobalt pipeline' (Frankel, 2016)", WAPO, 2016,
                          "Graphic: a laptop contains about '1 ounce' (28 g) of cobalt. 2016 figure; laptop cathode chemistries vary and many now use less cobalt. MacBook Air M5 battery uses 100% recycled cobalt (Apple PER)."),
        "global_units_per_year": 219_700_000,
        "per_second": ps(219_700_000),
        "volume_src": src("Omdia press release 2026-01-12", "https://omdia.tech.informa.com/pr/2025/dec/global-pc-shipments-grew-9percent-in-2025-but-memory-and-storage-supply-issues-threaten-2026-outlook", 2025,
                          "Notebook (incl. mobile workstation) shipments 219.7 million in 2025, +7.5%. All sizes. Total PCs 278.7 M (Gartner: >270 M)."),
        "swap": {"label": "Buy refurbished or keep it longer", "reduction_pct": 77,
                 "src": src("ADEME 2022, Assessment of the environmental impact of a set of refurbished products", ADEME_RECON, 2022,
                            "Refurbished laptop used 3 yrs instead of a new one used 5 yrs avoids 27.3 kg CO2e per year = -77% climate impact per year of use.")},
    },
]

EPA_CAR = "https://www.epa.gov/greenvehicles/greenhouse-gas-emissions-typical-passenger-vehicle"
constants = {
    "car_t_per_year": 4.6,
    "car_kg_per_km": round(0.400 / 1.609344, 4),
    "shower_l": round(17.2 * 3.785411784, 1),
    "budget_t": 2.5,
    "srcs": {
        "car_t_per_year": src("US EPA, Greenhouse Gas Emissions from a Typical Passenger Vehicle (page updated 2026-06-03)", EPA_CAR, 2023,
                              "Tailpipe CO2 only: ~4.6 t/yr, assumes 22.2 mpg and ~11,500 miles/yr (EPA-420-F-23-014)."),
        "car_kg_per_km": src("US EPA, same page", EPA_CAR, 2023,
                             "~400 g CO2 per mile tailpipe = 0.2485 kg per km (DERIVED unit conversion)."),
        "shower_l": src("US EPA WaterSense, Specification for Showerheads Supporting Statement", "https://www.epa.gov/sites/default/files/2017-01/documents/ws-products-support-statement-showerheads.pdf", 2010,
                        "Assumes 17.2 gallons per shower (8.2 min average) = 65.1 L. Newer EPA consumer material says '8 minutes x 2.1 gpm = more than 16 gallons' (~61 L)."),
        "budget_t": src("Hot or Cool Institute, 1.5-Degree Lifestyles: Towards a Fair Consumption Space for All", "https://hotorcool.org/publications/1-5-degree-lifestyles-towards-a-fair-consumption-space-for-all/", 2021,
                        "Per-capita lifestyle carbon footprint target compatible with 1.5C: 2.5 t CO2e by 2030, 1.4 t by 2040, 0.7 t by 2050 (builds on IGES et al. 2019)."),
    },
}

USGS = "https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-{}.pdf"
mnote = "USGS Mineral Commodity Summaries 2026 (first posted 2026-02-06), world total (rounded); production = 2025 estimated mine production."
minerals = [
    {"name": "Cobalt", "reserves_t": 12_000_000, "production_t": 310_000, "year": 2025,
     "src": src("USGS Mineral Commodity Summaries 2026, Cobalt", USGS.format("cobalt"), 2026, mnote + " Congo (Kinshasa) ~73% of mine output.")},
    {"name": "Nickel", "reserves_t": 140_000_000, "production_t": 3_900_000, "year": 2025,
     "src": src("USGS Mineral Commodity Summaries 2026, Nickel", USGS.format("nickel"), 2026, mnote + " Reserves are reported as '>140,000,000' t (a lower bound). Indonesia 2.6 Mt of 2025 output.")},
    {"name": "Copper", "reserves_t": 980_000_000, "production_t": 23_000_000, "year": 2025,
     "src": src("USGS Mineral Commodity Summaries 2026, Copper", USGS.format("copper"), 2026, mnote + " Table is in thousand metric tons (23,000 kt mine; 980,000 kt reserves). Refinery output 29 Mt.")},
    {"name": "Lithium", "reserves_t": 37_000_000, "production_t": 290_000, "year": 2025,
     "src": src("USGS Mineral Commodity Summaries 2026, Lithium", USGS.format("lithium"), 2026, mnote + " Lithium content; world production total excludes US output (withheld).")},
]

data = {"products": products, "constants": constants, "minerals": minerals,
        "meta": {"compiled": "2026-10-20", "seconds_per_year": SEC,
                 "notes": "Figures mix cradle-to-grave and cradle-to-retail boundaries; see each src.note. DERIVED marks values computed from cited inputs."}}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
for p in products:
    print(f"{p['id']:9} co2={p['co2_kg']:>7} water={p['water_l']!s:>6} co={p['cobalt_g']!s:>5} units={p['global_units_per_year']:.3e} /s={p['per_second']} swap={p['swap']['reduction_pct']}")
print(constants["car_kg_per_km"], constants["shower_l"])
