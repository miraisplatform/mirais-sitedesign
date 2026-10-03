"""旧サイト（Wix）の写真を images/ にダウンロードし、記事データの写真の場所を新サイト内に書き換える。
GitHub Actions から実行される。何度実行しても、取得済みの写真は飛ばす。"""
import json, os, re, sys, time, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "articles.json")
IMG_DIR = os.path.join(ROOT, "images")
WIX = re.compile(r"^https://static\.wixstatic\.com/media/([^/]+?\.(jpe?g|png|webp|gif))$", re.I)

os.makedirs(IMG_DIR, exist_ok=True)
data = json.load(open(DATA, encoding="utf-8"))
ok, failed = 0, []

def local(src):
    global ok
    m = WIX.match(src or "")
    if not m:
        return src
    name = m.group(1).replace("~", "_")
    path = os.path.join(IMG_DIR, name)
    if not os.path.exists(path):
        # 長辺1600pxに縮めた版を取得（元の巨大な写真をそのまま載せないため）
        url = f"{src}/v1/fit/w_1600,h_1600,q_85/{name}"
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as f:
                    f.write(r.read())
                break
            except Exception as e:
                if attempt == 2:
                    failed.append((src, str(e)))
                    return src
                time.sleep(2)
    ok += 1
    return f"images/{name}"

for a in data["articles"]:
    if a.get("cover"):
        a["cover"]["src"] = local(a["cover"]["src"])
    for b in a.get("body", []):
        if b["type"] == "img":
            b["src"] = local(b["src"])
        elif b["type"] == "gallery":
            for i in b["items"]:
                i["src"] = local(i["src"])

for c in data.get("about", {}).get("cans", []):
    c["img"] = local(c["img"])

json.dump(data, open(DATA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"写真: {ok} 件を配置 / 失敗 {len(failed)} 件")
for s, e in failed:
    print("  失敗:", s, e)
sys.exit(1 if failed else 0)
