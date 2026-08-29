"""page.src.html 하나에서 두 가지 결과물을 만든다.

  python3.12 build.py pages     → docs/index.html  (GitHub Pages용. 이미지는 별도 파일)
  python3.12 build.py artifact  → donghyeon.html   (Artifact용. 전부 base64 인라인)

Artifact는 외부 호스트를 못 부르니 인라인이 강제된다.
Pages는 같은 저장소에서 파일을 그냥 부르면 되니 인라인하면 손해다(용량 2.3MB → 80KB).
"""
import base64, os, shutil, sys

D = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(D, "assets")
MODE = sys.argv[1] if len(sys.argv) > 1 else "pages"

IMAGES = {
    "__IMG_DRAFT__":  "draft.png",
    "__IMG_SIM__":    "sim.png",
    "__IMG_RESULT__": "result.png",
    "__IMG_TOOL__":   "tool.png",
    "__IMG_MINI__":   "minini.png",
    "__IMG_HUB__":    "hub.png",
    "__IMG_SITED__":  "site-d.png",
    "__IMG_NETL__":   "net-login.png",
    "__IMG_NETB__":   "net-board.png",
}
PLATE = "title.png"
FONT = "galmuri11.woff2"

def data_uri(name, mime):
    with open(os.path.join(A, name), "rb") as f:
        return "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())

src = open(os.path.join(D, "page.src.html"), encoding="utf-8").read()

for ph in list(IMAGES) + ["__FONT_GALMURI__"]:
    if ph not in src:
        sys.exit("자리표시자 누락: %s" % ph)
if "var(--plate)" not in src:
    sys.exit("자리표시자 누락: var(--plate)")

if MODE == "artifact":
    src = src.replace("__FONT_GALMURI__", data_uri(FONT, "font/woff2"))
    for ph, fn in IMAGES.items():
        src = src.replace(ph, data_uri(fn, "image/png"))
    src = src.replace("var(--plate)", 'url("%s")' % data_uri(PLATE, "image/png"))
    out = os.path.join(D, "donghyeon.html")
    open(out, "w", encoding="utf-8").write(src)

else:
    src = src.replace("__FONT_GALMURI__", "assets/" + FONT)
    for ph, fn in IMAGES.items():
        src = src.replace(ph, "assets/" + fn)
    src = src.replace("var(--plate)", 'url("assets/%s")' % PLATE)

    # <title>만 뽑아 head로 올린다
    title = "전동현"
    if src.lstrip().startswith("<title>"):
        end = src.index("</title>") + len("</title>")
        title = src[src.index("<title>") + 7:src.index("</title>")]
        src = src[end:].lstrip("\n")

    desc = "숫자가 안 보이면 볼 도구를 만듭니다. 가상자산 마케팅 4년, 그리고 AI로 만든 것들."
    favicon = ("data:image/svg+xml,"
               "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
               "<text y='.9em' font-size='90'>%F0%9F%8F%9B</text></svg>")

    doc = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="전동현">
<meta name="color-scheme" content="light">
<meta property="og:type" content="profile">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:locale" content="ko_KR">
<meta property="og:image" content="https://ethmikel.github.io/portfolio/assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="전동현. 숫자가 안 보이면, 볼 도구를 만듭니다.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://ethmikel.github.io/portfolio/assets/og.png">
<link rel="icon" href="{favicon}">
</head>
<body>
{src}
</body>
</html>
"""
    docs = os.path.join(D, "docs")
    os.makedirs(docs, exist_ok=True)
    open(os.path.join(docs, "index.html"), "w", encoding="utf-8").write(doc)
    dest = os.path.join(docs, "assets")
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    shutil.copytree(A, dest)
    open(os.path.join(docs, ".nojekyll"), "w").close()   # _로 시작하는 파일이 없어도 습관
    out = os.path.join(docs, "index.html")

print("%s  %.0f KB" % (out, os.path.getsize(out) / 1024))
