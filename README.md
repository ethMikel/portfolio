# 전동현 — 레쥬메와 포트폴리오

https://ethmikel.github.io/portfolio/

## 고치는 법

`page.src.html` 하나만 고친다. 이미지와 폰트 자리는 `__IMG_*__` 같은 자리표시자로 둔다.

```bash
python3.12 build.py pages     # docs/index.html 생성 (배포용)
python3.12 build.py artifact  # donghyeon.html 생성 (Artifact 미리보기용, base64 인라인)
git add -A && git commit -m "..." && git push
```

푸시하면 같은 주소가 갱신된다.

## 항목 추가

1. 메인 `.cards`에 `<button class="card rise" style="--ac:var(--c-새이름);" data-go="새이름">`
2. `<div class="view 클래스" id="v-새이름" data-route="/새이름" data-tone="테마" data-ac="var(--c-새이름)">`
3. `:root`에 `--c-새이름` 색 토큰
4. `body[data-view="테마"]`와 `.클래스` CSS 한 덩어리

라우트 표와 전환 색은 화면 태그에서 자동으로 읽는다. 스크립트는 고칠 일이 없다.
화면 없이 카드만 두면 그 카드는 자동으로 숨는다.

## 규칙

- 가운뎃점(·)과 줄표(—) 금지. 이모지 금지
- 숫자는 실측값만. 상세는 `~/workspace/career/HANDOFF_토스레쥬메페이지_20260808.md`
