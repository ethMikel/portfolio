import base64, os, sys

D = os.path.dirname(os.path.abspath(__file__))
A = os.path.join(D, "assets")

def uri(name, mime):
    with open(os.path.join(A, name), "rb") as f:
        return "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())

src = open(os.path.join(D, "page.src.html"), encoding="utf-8").read()

subs = {
    "__FONT_GALMURI__": uri("galmuri11.woff2", "font/woff2"),
    "__IMG_DRAFT__":    uri("draft.png",  "image/png"),
    "__IMG_SIM__":      uri("sim.png",    "image/png"),
    "__IMG_RESULT__":   uri("result.png", "image/png"),
    "__IMG_TOOL__":     uri("tool.png",   "image/png"),
}
plate = uri("title.png", "image/png")

missing = [k for k in subs if k not in src]
if missing:
    sys.exit("placeholder 누락: %s" % missing)
if "var(--plate)" not in src:
    sys.exit("plate placeholder 누락")

for k, v in subs.items():
    src = src.replace(k, v)
src = src.replace("var(--plate)", 'url("%s")' % plate)

leftover = [t for t in ("__FONT", "__IMG", "--plate") if t in src]
if leftover:
    sys.exit("치환 안 된 자리 남음: %s" % leftover)

out = os.path.join(D, "donghyeon.html")
open(out, "w", encoding="utf-8").write(src)
print("wrote %s  %.2f MB" % (out, os.path.getsize(out) / 1024 / 1024))
