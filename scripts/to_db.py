"""live.json -> db_batch.json: one doc per store/category under live/, plus meta/scrape."""
import sys, json, re, pathlib
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
d = json.loads(src.read_text(encoding="utf-8"))
PACK = re.compile(r"(\d{1,3})\s*(?:-|\s)?(?:pack|count|ct\b|pods|k-cups|k cups|bottles|pk\b|pairs|patties)|pack of (\d{1,3})", re.I)

def units(title, cat):
    if cat not in ("coffee", "bottle", "clothing", "burger"): return 1
    nums = [int(m.group(1) or m.group(2)) for m in PACK.finditer(title)]
    nums = [n for n in nums if 1 < n <= 200]
    return max(nums) if nums else 1

ops, cats = [], set()
for store, byc in d["stores"].items():
    for cat, v in byc.items():
        cats.add(cat)
        top = []
        for i in v["top"]:
            u = units(i["title"], cat)
            top.append({k: i.get(k) for k in ("title", "url", "price", "rating", "reviews", "badge", "bought_month", "bought_day", "eco_cert")} | {"units_per_item": u})
        body = {"store": store, "cat": cat, "query": v["query"], "search_url": v["url"], "listings": v["listings"],
                "with_badge": v["with_badge"], "median_price": v.get("median_price"),
                "bought_month_lb": v.get("bought_month_lower_bound"), "bought_day_lb": v.get("bought_day_lower_bound"),
                "eco_share": v.get("eco_share"), "top": top, "scraped_at": d["scraped_at"]}
        ops.append({"action": "set", "collection": "live", "doc_id": f"{store}-{cat}", "data": body})
ops.append({"action": "set", "collection": "meta", "doc_id": "scrape", "data": {"scraped_at": d["scraped_at"], "source": "Bright Data Web Unlocker", "stores": sorted(d["stores"]), "cats": sorted(cats)}})
out.write_text(json.dumps(ops, indent=1), encoding="utf-8")
print(len(ops), "ops;", sum(len(json.dumps(o)) for o in ops), "bytes")
for o in ops[:14]:
    b = o["data"]
    if "top" in b: print(o["doc_id"], b["listings"], b.get("bought_month_lb") or b.get("bought_day_lb"), [(t["badge"], t["units_per_item"], t["title"][:40]) for t in b["top"][:2]])
