import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

df = pd.read_csv("data/superstore_clean.csv")
months = sorted(df["Order Month"].unique())
COLORS = {"Furniture": "#2a78d6", "Office Supplies": "#eb6834", "Technology": "#1baf7a"}

app = Dash(__name__)
app.layout = html.Div([
    html.H2("Superstore Sales Dashboard"),
    dcc.Dropdown(sorted(df["Region"].unique()), multi=True, id="region",
                 placeholder="Region 선택 (비우면 전체)"),
    dcc.Checklist(list(COLORS), list(COLORS), id="category", inline=True),
    dcc.RangeSlider(0, len(months) - 1, step=1, value=[0, len(months) - 1], id="period",
                    marks={i: m for i, m in enumerate(months) if m.endswith("-01")}),
    dcc.Graph(id="trend"),
    html.Div([dcc.Graph(id="compose", style={"flex": 1}),
              dcc.Graph(id="dist", style={"flex": 1})], style={"display": "flex"}),
    dcc.Graph(id="corr"),
], style={"maxWidth": "1200px", "margin": "auto", "fontFamily": "sans-serif"})

@app.callback(
    Output("trend", "figure"), Output("compose", "figure"),
    Output("dist", "figure"), Output("corr", "figure"),
    Input("region", "value"), Input("category", "value"), Input("period", "value"))
def update(regions, cats, period):
    d = df[df["Category"].isin(cats)]
    if regions:
        d = d[d["Region"].isin(regions)]
    lo, hi = months[period[0]], months[period[1]]
    d = d[(d["Order Month"] >= lo) & (d["Order Month"] <= hi)]

    # ① 추세: 월별 매출
    t = d.groupby(["Order Month", "Category"], as_index=False)["Sales"].sum()
    f1 = px.line(t, x="Order Month", y="Sales", color="Category",
                 color_discrete_map=COLORS, title="① 월별 매출 추세")
    f1.update_layout(hovermode="x unified")

    # ② 구성: 지역 × 카테고리
    c = d.groupby(["Region", "Category"], as_index=False)["Sales"].sum()
    f2 = px.bar(c, x="Region", y="Sales", color="Category",
                color_discrete_map=COLORS, title="② 지역 × 카테고리 매출 구성")

    # ③ 분포: 주문 라인당 매출
    f3 = px.box(d, x="Category", y="Sales", color="Category", log_y=True,
                color_discrete_map=COLORS, title="③ 주문 라인당 매출 분포 (로그 축)")

    # ④ 상관: 판매 건수 vs 건당 평균 매출
    s = d.groupby(["Sub-Category", "Category"], as_index=False).agg(
        Lines=("Sales", "size"), Sales=("Sales", "sum"))
    s["AvgSale"] = s["Sales"] / s["Lines"]
    f4 = px.scatter(s, x="Lines", y="AvgSale",category_orders={"Category": list(COLORS)},size="Sales", color="Category",
                    hover_name="Sub-Category", color_discrete_map=COLORS,
                    title="④ 판매 건수 vs 건당 평균 매출 (하위 카테고리)")
    return f1, f2, f3, f4

if __name__ == "__main__":
    app.run(debug=False)