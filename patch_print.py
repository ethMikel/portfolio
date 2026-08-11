import os, sys

D = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(D, "page.src.html")
s = open(P, encoding="utf-8").read()
done = []

def rep(old, new, label):
    global s
    if old not in s:
        sys.exit(f"[FAIL] 못 찾음: {label}")
    s = s.replace(old, new, 1)
    done.append(label)

# ── 1. 상단바에 PDF 버튼 ──────────────────────────────────────────────
rep(
"""    <a class="brand" href="#/">전동현<em>Jeon Donghyeon</em></a>
    <a class="back" href="#/" data-back hidden>&larr; 메인</a>""",
"""    <a class="brand" href="#/">전동현<em>Jeon Donghyeon</em></a>
    <div class="tbr">
      <a class="back" href="#/" data-back hidden>&larr; 메인</a>
      <button class="pdfbtn" type="button" data-pdf>PDF 저장</button>
    </div>""",
"PDF 버튼")

rep(
""".back[hidden]{display:none;}""",
""".back[hidden]{display:none;}
.tbr{display:flex;align-items:center;gap:var(--s3);}
.pdfbtn{font-size:13px;font-weight:600;color:var(--g600);border:1px solid var(--g200);
  padding:7px 14px;border-radius:999px;transition:color .2s var(--ease),border-color .2s var(--ease);}
.pdfbtn:hover{color:var(--blue);border-color:var(--blue);}
body[data-view="game"] .pdfbtn{color:var(--paper-300);border-color:var(--ink-500);}
body[data-view="tools"] .pdfbtn{color:#7d8a8e;border-color:#242c30;}
body[data-view="net"] .pdfbtn{color:#8b81a0;border-color:#2c2438;}
body[data-view="codex"] .pdfbtn{color:#7d7a74;border-color:#26262a;}""",
"PDF 버튼 스타일")

# ── 2. 인쇄 스타일. 여섯 화면을 한 문서로 ─────────────────────────────
rep(
"""@media (max-width:820px){""",
"""/* ── 인쇄. 여섯 화면을 순서대로 한 부의 문서로 찍는다 ─────────────────
   화면의 어두운 배경은 body[data-view]에 걸려 있어서, 전체를 한 번에 찍을 땐
   각 화면 요소에 자기 배경을 직접 준다. 안 주면 어두운 글자가 흰 종이에 사라진다. */
body.printing .view{display:block!important;}
body.printing #prog,body.printing #wipe{display:none!important;}
body.printing .hero > *,body.printing .rise,body.printing .lg,body.printing .axis span,
body.printing .figs > div,body.printing .figs2 > div,body.printing .tiles .tile{
  opacity:1!important;transform:none!important;transition:none!important;animation:none!important;}
body.printing .bar .fill,body.printing .abr .t i{transform:scaleX(1)!important;transition:none!important;}
body.printing #v-game{background:var(--ink-900);color:var(--paper-100);}
body.printing #v-tools{background:#0f1214;color:#d6dee1;}
body.printing #v-net{background:#131019;color:#ded8e8;}
body.printing #v-codex{background:#0d0d0e;color:#d7d3cc;}

@media print{
  *{-webkit-print-color-adjust:exact;print-color-adjust:exact;}
  @page{size:A4;margin:9mm;}
  html{scroll-behavior:auto;}
  .topbar,#prog,#wipe,.pdfbtn,.back{display:none!important;}
  footer{display:none!important;}
  .view{display:block!important;break-before:page;}
  #v-home{break-before:auto;}
  #v-game{background:var(--ink-900);color:var(--paper-100);}
  #v-tools{background:#0f1214;color:#d6dee1;}
  #v-net{background:#131019;color:#ded8e8;}
  #v-codex{background:#0d0d0e;color:#d7d3cc;}
  .hero{padding-top:var(--s6);}
  .hero > *,.rise,.lg,.axis span,.figs > div,.figs2 > div,.tiles .tile{
    opacity:1!important;transform:none!important;animation:none!important;}
  .bar .fill,.abr .t i{transform:scaleX(1)!important;}
  .card,.sm,.aiw,.tw,.tile,.term,blockquote,figure,.frame,.gframe,.gframe2,.item,.map > div,.fl{
    break-inside:avoid;}
  .card .go{display:none;}
  .card:hover{box-shadow:none;}
}

@media (max-width:820px){""",
"인쇄 CSS")

# ── 3. 인쇄 준비 스크립트 ─────────────────────────────────────────────
rep(
"""      c.addEventListener('pointerleave', function(){
        c.classList.remove('pull');
        c.style.setProperty('--dx','0px'); c.style.setProperty('--dy','0px');
      });
    });
  }
})();""",
"""      c.addEventListener('pointerleave', function(){
        c.classList.remove('pull');
        c.style.setProperty('--dx','0px'); c.style.setProperty('--dy','0px');
      });
    });
  }

  /* 인쇄 준비. 카운터를 최종값으로 채우고 전 화면을 켠다.
     ?print 로 열면 즉시 (헤드리스 PDF 생성용), 버튼과 Cmd+P는 beforeprint에서. */
  function printPrep(){
    if (document.body.classList.contains('printing')) return;
    document.body.classList.add('printing');
    document.querySelectorAll('.rise,#chart,#ab,.figs,.figs2,.tiles').forEach(function(el){ el.classList.add('on'); });
    document.querySelectorAll('[data-count]').forEach(function(el){
      var t = parseInt(el.getAttribute('data-count'),10);
      el.textContent = fmt(t) + (el.getAttribute('data-suffix') || '');
    });
  }
  if (new URLSearchParams(location.search).has('print')) printPrep();
  addEventListener('beforeprint', printPrep);
  addEventListener('afterprint', function(){ document.body.classList.remove('printing'); });
  var pb = document.querySelector('[data-pdf]');
  if (pb) pb.addEventListener('click', function(){ window.print(); });
})();""",
"인쇄 스크립트")

open(P, "w", encoding="utf-8").write(s)
print("적용 완료:")
for x in done: print("  -", x)
