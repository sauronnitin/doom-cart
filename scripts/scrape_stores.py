"""Scrape Amazon + Walmart US search results per product category via Bright Data Web Unlocker.
Usage: python scrape_stores.py <env_file> <out_dir> [--reparse]
Writes raw HTML per page and live.json with parsed listings + sales-badge totals."""
import sys, json, re, time, pathlib, concurrent.futures as cf, urllib.request, urllib.parse
from bs4 import BeautifulSoup

ENV, OUT = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
REPARSE = "--reparse" in sys.argv
OUT.mkdir(parents=True, exist_ok=True)
KEY = next(l.split("=", 1)[1].strip() for l in ENV.read_text().splitlines() if l.startswith("BRIGHTDATA_API_KEY="))

CATS = {  # id: search query (what a shopper would type)
    "coffee": "coffee pods",
    "bottle": "bottled water",
    "burger": "beef burger patties",
    "clothing": "t-shirt",
    "sneaker": "running shoes",
    "phone": "unlocked smartphone",
    "laptop": "laptop",
}
RELEVANT = {"coffee": r"coffee|k-cup|espresso", "bottle": r"water", "burger": r"beef|burger", "clothing": r"shirt|tee|t-shirt",
    "sneaker": r"shoe|sneaker|runn|trainer", "phone": r"phone|unlocked|5g|smartphone", "laptop": r"laptop|macbook|notebook|chromebook"}
EXCLUDE = {"burger": r"buns?|brioche|bread|chicken|turkey|veggie|plant|seasoning|press|grill|spatula", "bottle": r"filter|pitcher|reusable|insulated|stainless|tumbler",
    "coffee": r"maker|machine|grinder|mug|filter", "phone": r"case|charger|screen protector|cable", "laptop": r"bag|sleeve|stand|case|backpack"}
URLS = {
    "amazon": "https://www.amazon.com/s?k={q}",
    "walmart": "https://www.walmart.com/search?q={q}",
}

def fetch(url, tries=3):
    for k in range(tries):
        try: return _fetch(url)
        except Exception as e:
            if k == tries - 1: raise
            time.sleep(3)

def _fetch(url):
    body = json.dumps({"zone": "mcp_unlocker", "url": url, "format": "raw"}).encode()
    req = urllib.request.Request("https://api.brightdata.com/request", data=body,
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=200) as r:
        return r.read().decode("utf-8", "replace")

def badge_to_n(text):
    m = re.search(r"([\d.,]+)\s*([KkMm]?)\+?\s*bought", text or "")
    if not m: return None
    n = float(m.group(1).replace(",", ""))
    return int(n * {"k": 1e3, "m": 1e6}.get(m.group(2).lower(), 1))

def money(text):
    m = re.search(r"\$\s?([\d,]+\.?\d*)", text or "")
    return float(m.group(1).replace(",", "")) if m else None

def parse_amazon(html):
    soup, items = BeautifulSoup(html, "lxml"), []
    for d in soup.select('div[data-component-type="s-search-result"]'):
        asin = d.get("data-asin")
        h2s = [h.get_text(" ", strip=True) for h in d.select("h2")]
        if not asin or not h2s: continue
        title = " ".join(h2s) if len(h2s) > 1 and len(h2s[0]) < 40 else max(h2s, key=len)
        txt = d.get_text(" ", strip=True)
        bm = re.search(r"[\d.,]+[KkMm]?\+?\s*bought in past month", txt)
        rating = d.select_one("span.a-icon-alt")
        reviews = d.select_one('a[href*="customerReviews"] span, span.a-size-base.s-underline-text')
        price = d.select_one("span.a-price > span.a-offscreen")
        items.append({
            "id": asin, "title": title[:220],
            "url": f"https://www.amazon.com/dp/{asin}",
            "price": money(price.get_text() if price else None),
            "rating": float(rating.get_text().split()[0]) if rating and rating.get_text()[:1].isdigit() else None,
            "reviews": reviews.get_text(strip=True) if reviews else None,
            "badge": bm.group(0) if bm else None,
            "bought_month": badge_to_n(bm.group(0)) if bm else None,
            "sponsored": "Sponsored" in txt[:200],
            "eco_cert": ("Sustainability features" in txt) or ("Climate Pledge" in txt),
        })
    return items

def parse_walmart(html):
    soup, items = BeautifulSoup(html, "lxml"), []
    tag = soup.select_one("script#__NEXT_DATA__")
    if not tag: return items
    data = json.loads(tag.string)
    def walk(o):
        if isinstance(o, dict):
            if o.get("__typename") == "Product" and o.get("name") and o.get("usItemId"):
                yield o
            for v in o.values(): yield from walk(v)
        elif isinstance(o, list):
            for v in o: yield from walk(v)
    seen = set()
    for p in walk(data):
        pid = p.get("usItemId")
        if pid in seen: continue
        seen.add(pid)
        badges = json.dumps(p)
        bm = re.search(r"[\d.,]+[KkMm]?\+?\s*bought since yesterday", badges)
        pr = (p.get("priceInfo") or {}).get("currentPrice") or {}
        items.append({
            "id": pid, "title": p["name"][:220],
            "url": "https://www.walmart.com" + p["canonicalUrl"] if p.get("canonicalUrl") else f"https://www.walmart.com/ip/{pid}",
            "price": pr.get("price") if isinstance(pr, dict) else None,
            "rating": p.get("averageRating"),
            "reviews": p.get("numberOfReviews"),
            "badge": bm.group(0) if bm else None,
            "bought_day": badge_to_n(bm.group(0)) if bm else None,
            "sponsored": bool(p.get("isSponsoredFlag")),
            "eco_cert": False,
        })
    return items

def job(store, cat, q):
    path = OUT / f"{store}_{cat}.html"
    url = URLS[store].format(q=urllib.parse.quote_plus(q))
    if not (REPARSE and path.exists()):
        t = time.time(); html = fetch(url); path.write_text(html, encoding="utf-8")
        took = round(time.time() - t, 1)
    else:
        html, took = path.read_text(encoding="utf-8"), 0
    raw = parse_amazon(html) if store == "amazon" else parse_walmart(html)
    seen, items = set(), []
    for i in raw:
        key = re.sub(r"[^a-z0-9]", "", i["title"].lower())[:60]
        if i["id"] in seen or key in seen or not re.search(RELEVANT[cat], i["title"], re.I): continue
        if EXCLUDE.get(cat) and re.search(EXCLUDE[cat], i["title"], re.I): continue
        seen.update([i["id"], key]); items.append(i)
    return store, cat, q, url, items, took, len(html)

results = {"scraped_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "stores": {}}
with cf.ThreadPoolExecutor(max_workers=7) as ex:
    futs = [ex.submit(job, s, c, q) for s in URLS for c, q in CATS.items()]
    for f in cf.as_completed(futs):
        try:
            store, cat, q, url, items, took, size = f.result()
        except Exception as e:
            print("FAIL", e); continue
        organic = [i for i in items if not i["sponsored"]]
        if store == "amazon":
            month = sum(i["bought_month"] or 0 for i in items)
            summ = {"bought_month_lower_bound": month, "with_badge": sum(1 for i in items if i["bought_month"]),
                    "eco_share": round(sum(i["eco_cert"] for i in items) / max(1, len(items)), 3)}
        else:
            day = sum(i["bought_day"] or 0 for i in items)
            summ = {"bought_day_lower_bound": day, "with_badge": sum(1 for i in items if i["bought_day"])}
        top = sorted(items, key=lambda i: (-(i.get("bought_month") or i.get("bought_day") or 0), -(int(re.sub(r"[^0-9]", "", str(i.get("reviews") or 0)) or 0))))[:5]
        results["stores"].setdefault(store, {})[cat] = {"query": q, "url": url, "listings": len(items),
            **summ, "median_price": sorted([i["price"] for i in items if i["price"]])[len([i for i in items if i["price"]]) // 2] if any(i["price"] for i in items) else None,
            "top": top}
        print(f"{store:8} {cat:9} listings={len(items):3} badges={summ['with_badge']:3} "
              f"total={summ.get('bought_month_lower_bound', summ.get('bought_day_lower_bound'))} size={size} took={took}s")
(OUT / "live.json").write_text(json.dumps(results, indent=1), encoding="utf-8")
print("wrote", OUT / "live.json")
