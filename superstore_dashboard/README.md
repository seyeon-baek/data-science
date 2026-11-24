# Superstore Sales Dashboard

Kaggle Superstore Sales 데이터로 만든 Plotly Dash 대시보드입니다.

## 1. 환경 설치
```bash
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 2. 실행
```bash
python clean_data.py   # data/superstore_clean.csv 생성
python app.py          # 브라우저에서 http://127.0.0.1:8050 접속
```

## 3. 데이터 정제
- 원본: data/raw/super_store_sales.csv (9,800행, 2015-01 ~ 2018-12)
- Order Date(일/월/연) → 연-월(Order Month)로 변환
- 사용 컬럼: Order Month, Region, Category, Sub-Category, Order ID, Sales
- 원본에 Profit, Quantity 컬럼이 없어 Quantity는 주문 라인 수로 대체함

## 4. 시각화 구성
1. 월별 매출 추세 (라인) – 추세
2. 지역 × 카테고리 매출 구성 (누적 막대) – 구성
3. 주문 라인당 매출 분포 (박스플롯) – 분포
4. 판매 건수 vs 건당 평균 매출 (버블) – 상관
- 필터: Region, Category, 기간 슬라이더 / hover, 확대 지원