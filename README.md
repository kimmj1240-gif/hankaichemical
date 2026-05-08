# 한카케미칼 — 플라스틱 레진 일일 가격 추적기

매일 신재(virgin) / 재생(recycled) 플라스틱 레진 가격을 자동으로 수집해
저장소 히스토리에 누적하고, 정적 대시보드로 보여줍니다.

## 구성

```
data/
  resins.json     # 추적 대상 레진 마스터 (신재 14종 + 재생 7종)
  prices.csv      # 일자별 가격 누적 (자동 추가)
scripts/
  collect_prices.py     # 매일 한 행씩 가격을 모아 prices.csv에 append
  build_dashboard.py    # prices.csv → index.html 정적 대시보드
  dashboard_template.html
.github/workflows/
  daily-prices.yml      # KST 09:30 매일 자동 실행 + GitHub Pages 배포
index.html        # 빌드 산출물 (대시보드, GitHub Pages 루트)
```

## 매일 동작 흐름

1. GitHub Actions가 매일 09:30 KST에 `collect_prices.py` 실행
2. 각 레진별로 한 행을 `data/prices.csv`에 추가 (가격은 비어 있으면 `awaiting input`)
3. `build_dashboard.py`가 `index.html`을 다시 만들어 GitHub Pages로 배포
4. 변경분이 있으면 봇이 같은 브랜치로 커밋 — 커밋 히스토리가 곧 가격 히스토리

## 가격을 채우는 3가지 방법

### 1) 수동 입력 (가장 안정적)
`data/prices.csv`의 빈 `price_krw_per_kg` 칸에 숫자만 채워 커밋하면 됩니다.
대시보드는 자동으로 차트와 전일 대비를 다시 계산합니다.

### 2) 스크래퍼 추가
`scripts/collect_prices.py`의 `fetch_virgin_prices` /
`fetch_recycled_prices` 함수를 실제 데이터 소스(예: 한국석유화학협회,
공개 시세 페이지) 호출로 바꾸면 자동 채워집니다. 사이트 약관·로봇룰을
반드시 먼저 확인하세요.

### 3) 유료 API 연동
ICIS, S&P Global Platts 등 라이선스가 있는 경우 `os.environ`으로 키를
읽어 위 두 함수에서 호출하세요. 키는 GitHub Actions Secrets로 주입.

## 로컬 실행

```bash
python scripts/collect_prices.py   # 오늘자 빈 행 추가 (이미 있으면 skip, FORCE=1 로 강제)
python scripts/build_dashboard.py  # index.html 갱신
```

## 추가/제외할 레진 변경

`data/resins.json`을 편집하면 다음 수집 시점부터 반영됩니다.
대시보드의 신재/재생 탭과 차트 선택 목록도 자동 갱신.
