from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
SALES_FILE = DATA_DIR / "demo_sales_2026.csv"
KPI_FILE = DATA_DIR / "demo_kpi_2026.csv"

BRAND = ["#0C6A57", "#D2574E", "#13718A", "#E2A13A", "#2F5C88", "#6F57B1"]
TEXT = "#13263E"
MUTED = "#5D7088"
GRID = "#D8E1EB"
PANEL = "#FFFFFF"
PLOT = "#FBFCFE"
BORDER = "#CFD8E3"
SHADOW = "rgba(15, 30, 52, 0.12)"
BODY_FONT = '"Aptos", "Segoe UI", sans-serif'
HEAD_FONT = '"Bahnschrift SemiBold", "Segoe UI Semibold", sans-serif'


st.set_page_config(
    page_title="Demo 2026 Sales & Marketing Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


@st.cache_data(show_spinner=False)
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    sales = pd.read_csv(SALES_FILE)
    kpi = pd.read_csv(KPI_FILE)
    sales["contract_date"] = pd.to_datetime(sales["contract_date"], errors="coerce")
    sales["period_start"] = pd.to_datetime(sales["period_start"], errors="coerce")
    kpi["period_start"] = pd.to_datetime(kpi["period_start"], errors="coerce")
    numeric_sales = ["revenue_before_vat", "year", "month", "quarter"]
    numeric_kpi = [
        "month",
        "kpi_target",
        "actual_revenue",
        "actual_deals",
        "actual_customers",
        "kpi_completion",
        "gap_to_target",
    ]
    for column in numeric_sales:
        sales[column] = pd.to_numeric(sales[column], errors="coerce")
    for column in numeric_kpi:
        kpi[column] = pd.to_numeric(kpi[column], errors="coerce")
    return sales, kpi


def inject_styles() -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                radial-gradient(circle at top left, rgba(12, 106, 87, 0.14), transparent 24%),
                radial-gradient(circle at top right, rgba(210, 87, 78, 0.10), transparent 18%),
                linear-gradient(180deg, #EEF3F7 0%, #E5EDF6 100%);
            color: {TEXT};
            font-family: {BODY_FONT};
        }}
        .block-container {{
            max-width: 1440px;
            padding-top: 2rem;
            padding-bottom: 2.8rem;
        }}
        h1, h2, h3, h4 {{
            font-family: {HEAD_FONT};
            color: {TEXT};
            letter-spacing: -0.02em;
        }}
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #10233F 0%, #0B1728 100%);
            border-right: 1px solid rgba(255, 255, 255, 0.08);
        }}
        section[data-testid="stSidebar"] * {{
            color: #F5F8FC;
        }}
        .hero {{
            background: linear-gradient(135deg, #FFFFFF 0%, #F7FAFD 72%, #EFF5FB 100%);
            border: 1.5px solid {BORDER};
            border-radius: 28px;
            padding: 1.7rem 1.85rem 1.5rem 1.85rem;
            box-shadow: 0 24px 54px {SHADOW};
            margin-bottom: 1rem;
        }}
        .hero-kicker {{
            color: #0C6A57;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.18em;
            text-transform: uppercase;
            margin-bottom: 0.45rem;
        }}
        .hero-title {{
            font-family: {HEAD_FONT};
            font-size: 2.25rem;
            line-height: 1.02;
            margin: 0 0 0.42rem 0;
            color: {TEXT};
        }}
        .hero-copy {{
            color: {MUTED};
            max-width: 930px;
            font-size: 1rem;
            line-height: 1.58;
            margin: 0;
        }}
        .metric-card {{
            background: linear-gradient(180deg, #FFFFFF 0%, #F7FBFD 100%);
            border: 1.5px solid {BORDER};
            border-radius: 22px;
            padding: 1rem 1.05rem 0.95rem 1.05rem;
            min-height: 126px;
            box-shadow: 0 20px 40px rgba(16, 35, 63, 0.11);
        }}
        .metric-label {{
            color: {MUTED};
            font-size: 0.88rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }}
        .metric-value {{
            color: {TEXT};
            font-family: {HEAD_FONT};
            font-size: 1.95rem;
            line-height: 1.05;
            margin: 0.62rem 0 0.35rem 0;
        }}
        .metric-copy {{
            color: {MUTED};
            font-size: 0.95rem;
            line-height: 1.45;
        }}
        .insight-card {{
            background: #FFFFFF;
            border: 1.5px solid {BORDER};
            border-radius: 22px;
            padding: 1.05rem 1.12rem 0.95rem 1.12rem;
            box-shadow: 0 18px 38px rgba(16, 35, 63, 0.11);
            min-height: 240px;
        }}
        .insight-card h3 {{
            margin: 0 0 0.6rem 0;
            font-size: 1.1rem;
        }}
        .insight-card ul {{
            margin: 0;
            padding-left: 1.05rem;
        }}
        .insight-card li {{
            color: {TEXT};
            line-height: 1.5;
            margin-bottom: 0.55rem;
        }}
        div.stPlotlyChart,
        div[data-testid="stDataFrame"] {{
            background: #FFFFFF;
            border: 1.5px solid {BORDER};
            border-radius: 22px;
            padding: 0.72rem 0.72rem 0.58rem 0.72rem;
            box-shadow: 0 22px 44px rgba(16, 35, 63, 0.12);
        }}
        div[data-baseweb="tab-list"] {{
            background: rgba(255, 255, 255, 0.92);
            border: 1.2px solid #D4DDEA;
            border-radius: 999px;
            padding: 0.28rem;
            gap: 0.35rem;
            box-shadow: 0 12px 24px rgba(16, 35, 63, 0.08);
        }}
        div[data-baseweb="tab-list"] button {{
            border-radius: 999px;
            color: {MUTED};
            font-weight: 700;
            min-height: 46px;
            padding: 0 1rem;
        }}
        div[data-baseweb="tab-list"] button[aria-selected="true"] {{
            background: linear-gradient(135deg, #10233F 0%, #0C6A57 100%);
            color: white;
        }}
        .caption {{
            color: {MUTED};
            font-size: 0.96rem;
            margin-top: -0.2rem;
            margin-bottom: 0.8rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_currency(value: float) -> str:
    if pd.isna(value):
        return "-"
    abs_value = abs(value)
    if abs_value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if abs_value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    return f"{value:,.0f}"


def format_pct(value: float) -> str:
    if pd.isna(value):
        return "-"
    return f"{value * 100:.1f}%"


def style_figure(figure: go.Figure, title: str, *, height: int = 400, show_legend: bool = False) -> go.Figure:
    figure.update_layout(
        title=dict(text=title, x=0, xanchor="left", font=dict(family=HEAD_FONT, size=21, color=TEXT)),
        paper_bgcolor=PANEL,
        plot_bgcolor=PLOT,
        font=dict(family=BODY_FONT, size=13, color=TEXT),
        margin=dict(l=12, r=12, t=68, b=16),
        height=height,
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            x=0,
            bgcolor="rgba(0,0,0,0)",
            title="",
        ),
        hoverlabel=dict(bgcolor="white", font=dict(family=BODY_FONT, size=12, color=TEXT)),
    )
    figure.update_xaxes(
        tickfont=dict(color=TEXT, size=12),
        title_font=dict(color=MUTED, size=13, family=BODY_FONT),
        linecolor="#CBD5E0",
        tickcolor="#AAB7C7",
    )
    figure.update_yaxes(
        tickfont=dict(color=TEXT, size=12),
        title_font=dict(color=MUTED, size=13, family=BODY_FONT),
        linecolor="#CBD5E0",
        tickcolor="#AAB7C7",
    )
    figure.update_traces(marker_line_width=0, textfont_color=TEXT)
    return figure


def apply_scope(sales: pd.DataFrame, start_date, end_date) -> pd.DataFrame:
    mask = sales["contract_date"].dt.date.between(start_date, end_date)
    return sales.loc[mask].copy()


def scope_months(frame: pd.DataFrame) -> list[int]:
    return sorted(frame["month"].dropna().astype(int).unique().tolist())


def monthly_revenue(frame: pd.DataFrame) -> pd.DataFrame:
    return (
        frame.groupby("period_start", dropna=False)
        .agg(
            revenue=("revenue_before_vat", "sum"),
            deals=("deal_id", "nunique"),
            customers=("customer_key", "nunique"),
        )
        .reset_index()
        .sort_values("period_start")
    )


def summarize(frame: pd.DataFrame, dimension: str, *, top_n: int | None = None) -> pd.DataFrame:
    summary = (
        frame.groupby(dimension, dropna=False)
        .agg(revenue=("revenue_before_vat", "sum"), deals=("deal_id", "nunique"), customers=("customer_key", "nunique"))
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    return summary.head(top_n) if top_n else summary


def aggregate_department_kpi(kpi: pd.DataFrame) -> pd.DataFrame:
    frame = kpi[kpi["row_type"] == "department_total"].copy()
    grouped = (
        frame.groupby("department", dropna=False)
        .agg(
            kpi_target=("kpi_target", "sum"),
            actual_revenue=("actual_revenue", "sum"),
            actual_deals=("actual_deals", "sum"),
            actual_customers=("actual_customers", "sum"),
        )
        .reset_index()
        .sort_values("actual_revenue", ascending=False)
    )
    grouped["kpi_completion"] = np.where(grouped["kpi_target"] > 0, grouped["actual_revenue"] / grouped["kpi_target"], np.nan)
    grouped["gap_to_target"] = grouped["actual_revenue"] - grouped["kpi_target"]
    return grouped


def aggregate_employee_kpi(kpi: pd.DataFrame) -> pd.DataFrame:
    frame = kpi[kpi["row_type"] == "employee"].copy()
    grouped = (
        frame.groupby(["salesperson", "department"], dropna=False)
        .agg(
            kpi_target=("kpi_target", "sum"),
            actual_revenue=("actual_revenue", "sum"),
            actual_deals=("actual_deals", "sum"),
            actual_customers=("actual_customers", "sum"),
        )
        .reset_index()
        .sort_values("actual_revenue", ascending=False)
    )
    grouped["kpi_completion"] = np.where(grouped["kpi_target"] > 0, grouped["actual_revenue"] / grouped["kpi_target"], np.nan)
    grouped["gap_to_target"] = grouped["actual_revenue"] - grouped["kpi_target"]
    return grouped[grouped["salesperson"].fillna("").ne("")]


def marketing_source_summary(frame: pd.DataFrame) -> pd.DataFrame:
    summary = (
        frame.groupby(["lead_source", "marketing_channel"], dropna=False)
        .agg(
            revenue=("revenue_before_vat", "sum"),
            opportunity_count=("opportunity_id", "nunique"),
            deal_count=("deal_id", "nunique"),
            customer_count=("customer_key", "nunique"),
        )
        .reset_index()
        .sort_values("revenue", ascending=False)
    )
    total_revenue = float(summary["revenue"].sum())
    summary["proxy_conversion_rate"] = np.where(
        summary["opportunity_count"] > 0,
        summary["deal_count"] / summary["opportunity_count"],
        np.nan,
    )
    summary["revenue_per_opportunity"] = np.where(
        summary["opportunity_count"] > 0,
        summary["revenue"] / summary["opportunity_count"],
        np.nan,
    )
    summary["revenue_share"] = np.where(total_revenue > 0, summary["revenue"] / total_revenue, np.nan)
    return summary


def forecast_revenue(monthly: pd.DataFrame, periods: int = 2) -> pd.DataFrame:
    if monthly.shape[0] < 3:
        return pd.DataFrame(columns=["period_start", "forecast_revenue"])
    ordered = monthly.sort_values("period_start").reset_index(drop=True)
    x_values = np.arange(len(ordered), dtype=float)
    y_values = ordered["revenue"].astype(float).to_numpy()
    slope, intercept = np.polyfit(x_values, y_values, 1)
    future_x = np.arange(len(ordered), len(ordered) + periods, dtype=float)
    future_y = np.maximum((slope * future_x) + intercept, 0.0)
    future_dates = pd.date_range(ordered["period_start"].max() + pd.offsets.MonthBegin(1), periods=periods, freq="MS")
    return pd.DataFrame({"period_start": future_dates, "forecast_revenue": future_y})


def make_bar(frame: pd.DataFrame, *, x: str, y: str, title: str, orientation: str = "v", percent_axis: bool = False) -> go.Figure:
    ordered = frame.sort_values(y, ascending=orientation == "h")
    figure = px.bar(
        ordered,
        x=x if orientation == "v" else y,
        y=y if orientation == "v" else x,
        orientation=orientation,
        color_discrete_sequence=BRAND,
        template="plotly_white",
    )
    if orientation == "h":
        figure.update_xaxes(showgrid=True, gridcolor=GRID, zeroline=False)
        figure.update_yaxes(showgrid=False)
        if percent_axis:
            figure.update_xaxes(tickformat=".0%")
    else:
        figure.update_xaxes(showgrid=False)
        figure.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False)
        if percent_axis:
            figure.update_yaxes(tickformat=".0%")
    return style_figure(figure, title)


def make_donut(frame: pd.DataFrame, *, names: str, values: str, title: str) -> go.Figure:
    figure = px.pie(frame, names=names, values=values, hole=0.58, color_discrete_sequence=BRAND, template="plotly_white")
    figure.update_traces(
        textposition="inside",
        textinfo="percent+label",
        insidetextfont=dict(color="white", size=12),
        hovertemplate="<b>%{label}</b><br>Doanh số: %{value:,.0f}<br>Tỷ trọng: %{percent}<extra></extra>",
    )
    return style_figure(figure, title)


def make_line(actual: pd.DataFrame, forecast: pd.DataFrame) -> go.Figure:
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=actual["period_start"],
            y=actual["revenue"],
            mode="lines+markers+text",
            name="Actual",
            text=[format_currency(value) for value in actual["revenue"]],
            textposition="top center",
            line=dict(color=BRAND[0], width=3.6),
            marker=dict(size=9, color=BRAND[0]),
            fill="tozeroy",
            fillcolor="rgba(12, 106, 87, 0.10)",
        )
    )
    if not forecast.empty:
        figure.add_trace(
            go.Scatter(
                x=forecast["period_start"],
                y=forecast["forecast_revenue"],
                mode="lines+markers+text",
                name="Forecast",
                text=[format_currency(value) for value in forecast["forecast_revenue"]],
                textposition="top center",
                line=dict(color=BRAND[1], width=2.6, dash="dash"),
                marker=dict(size=8, color=BRAND[1]),
            )
        )
    figure.update_xaxes(showgrid=False)
    figure.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False)
    return style_figure(figure, "Doanh số theo tháng", height=430, show_legend=True)


def make_kpi_chart(frame: pd.DataFrame) -> go.Figure:
    ordered = frame.sort_values("actual_revenue", ascending=False)
    figure = go.Figure()
    figure.add_bar(x=ordered["department"], y=ordered["kpi_target"], name="KPI", marker_color="#CCD6E2")
    figure.add_bar(
        x=ordered["department"],
        y=ordered["actual_revenue"],
        name="Actual",
        marker_color=BRAND[0],
        text=[format_currency(value) for value in ordered["actual_revenue"]],
        textposition="outside",
    )
    figure.update_layout(barmode="group")
    figure.update_xaxes(showgrid=False)
    figure.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False)
    return style_figure(figure, "KPI vs Actual theo phòng ban", show_legend=True)


def make_bubble(frame: pd.DataFrame) -> go.Figure:
    figure = px.scatter(
        frame,
        x="opportunity_count",
        y="revenue_per_opportunity",
        size="revenue",
        color="marketing_channel",
        text="lead_source",
        size_max=58,
        color_discrete_sequence=BRAND,
        template="plotly_white",
    )
    figure.update_traces(textposition="top center")
    figure.update_xaxes(showgrid=True, gridcolor=GRID, zeroline=False, title="Số lead / cơ hội")
    figure.update_yaxes(showgrid=True, gridcolor=GRID, zeroline=False, title="Doanh thu / lead")
    return style_figure(figure, "Bản đồ hiệu suất nguồn lead", height=430, show_legend=True)


def render_metric(label: str, value: str, caption: str) -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-copy">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_insights(title: str, items: list[str]) -> None:
    bullets = "".join(f"<li>{item}</li>" for item in items)
    st.markdown(
        f"""
        <div class="insight-card">
            <h3>{title}</h3>
            <ul>{bullets}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_business_insights(monthly: pd.DataFrame, departments: pd.DataFrame, employees: pd.DataFrame, sources: pd.DataFrame) -> dict[str, list[str]]:
    insights: dict[str, list[str]] = {"Kinh doanh": [], "Nhân sự": [], "Marketing": [], "Khuyến nghị": []}

    if not monthly.empty:
        peak = monthly.sort_values("revenue", ascending=False).iloc[0]
        low = monthly.sort_values("revenue", ascending=True).iloc[0]
        insights["Kinh doanh"].append(
            f"Tháng cao điểm là {peak['period_start']:%b %Y} với {format_currency(float(peak['revenue']))}; thấp nhất là {low['period_start']:%b %Y} với {format_currency(float(low['revenue']))}."
        )
        if monthly.shape[0] >= 2:
            last_delta = float(monthly["revenue"].iloc[-1] - monthly["revenue"].iloc[-2])
            trend = "tăng" if last_delta >= 0 else "giảm"
            insights["Kinh doanh"].append(f"Xu hướng gần nhất đang {trend} {format_currency(abs(last_delta))} so với tháng liền trước.")

    if not departments.empty:
        best = departments.iloc[0]
        weakest = departments.sort_values("kpi_completion").iloc[0]
        insights["Kinh doanh"].append(
            f"{best['department']} dẫn đầu doanh thu với {format_currency(float(best['actual_revenue']))}, trong khi {weakest['department']} mới đạt {format_pct(float(weakest['kpi_completion']))} KPI."
        )
        if float((departments["kpi_completion"] >= 1).mean()) < 0.5:
            insights["Khuyến nghị"].append("Tỷ lệ phòng ban đạt KPI còn thấp; nên rà lại phân bổ target giữa BU mạnh và BU yếu.")

    if not employees.empty:
        best_person = employees.iloc[0]
        concentration = float(employees.head(5)["actual_revenue"].sum() / employees["actual_revenue"].sum()) if employees["actual_revenue"].sum() else np.nan
        insights["Nhân sự"].append(
            f"Top performer hiện tại là {best_person['salesperson']} với {format_currency(float(best_person['actual_revenue']))} doanh số."
        )
        if pd.notna(concentration):
            insights["Nhân sự"].append(f"Top 5 nhân sự đang chiếm {format_pct(concentration)} tổng doanh số, cho thấy mức độ tập trung tương đối cao.")
            if concentration > 0.7:
                insights["Khuyến nghị"].append("Nên giảm phụ thuộc vào nhóm top performer bằng coaching và phân bổ lead tốt hơn cho lớp giữa.")

    if not sources.empty:
        top_revenue = sources.iloc[0]
        top_conversion = sources.sort_values("proxy_conversion_rate", ascending=False).iloc[0]
        weakest_efficiency = sources[sources["opportunity_count"] >= 3].sort_values("revenue_per_opportunity").head(1)
        insights["Marketing"].append(
            f"Kênh tạo doanh thu cao nhất là {top_revenue['lead_source']} với {format_currency(float(top_revenue['revenue']))}."
        )
        insights["Marketing"].append(
            f"Kênh có proxy conversion tốt nhất là {top_conversion['lead_source']} ở mức {format_pct(float(top_conversion['proxy_conversion_rate']))}."
        )
        if not weakest_efficiency.empty:
            row = weakest_efficiency.iloc[0]
            insights["Khuyến nghị"].append(
                f"Cần xem lại {row['lead_source']}: giá trị trung bình trên mỗi cơ hội chỉ ở mức {format_currency(float(row['revenue_per_opportunity']))}."
            )

    return insights


def main() -> None:
    inject_styles()
    sales, kpi = load_data()

    min_date = sales["contract_date"].min().date()
    max_date = sales["contract_date"].max().date()

    st.sidebar.markdown("## Bộ lọc thời gian")
    selected = st.sidebar.date_input("Khoảng ngày", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    if isinstance(selected, (list, tuple)):
        start_date, end_date = selected
    else:
        start_date = end_date = selected
    st.sidebar.caption("Các chiều khác được cố định ở trạng thái All để giao diện tập trung vào xu hướng tổng quan.")

    display_sales = apply_scope(sales, start_date, end_date)
    if display_sales.empty:
        st.warning("Không có dữ liệu trong khoảng thời gian đang chọn.")
        st.stop()

    month_scope = scope_months(display_sales)
    kpi_scope = kpi[kpi["month"].isin(month_scope)].copy()
    department_kpi = aggregate_department_kpi(kpi_scope)
    employee_kpi = aggregate_employee_kpi(kpi_scope)
    monthly = monthly_revenue(display_sales)
    forecast = forecast_revenue(monthly)
    source_summary = marketing_source_summary(display_sales)

    total_revenue = float(display_sales["revenue_before_vat"].sum())
    total_deals = int(display_sales["deal_id"].nunique())
    total_customers = int(display_sales["customer_key"].nunique())
    total_kpi = float(department_kpi["kpi_target"].sum()) if not department_kpi.empty else 0.0
    achieved_pct = float(department_kpi["actual_revenue"].sum() / total_kpi) if total_kpi > 0 else np.nan
    gap_to_target = float(department_kpi["actual_revenue"].sum() - total_kpi) if total_kpi > 0 else 0.0
    avg_deal_value = total_revenue / max(total_deals, 1)
    alerts = department_kpi[department_kpi["kpi_completion"] < 0.8].sort_values("kpi_completion")
    insights = build_business_insights(monthly, department_kpi, employee_kpi, source_summary)

    st.markdown(
        """
        <div class="hero">
            <div class="hero-kicker">Demo 2026 Performance Center</div>
            <div class="hero-title">Dashboard doanh số và marketing</div>
            <p class="hero-copy">
                Bộ dữ liệu trong phiên bản public đã được chuẩn hóa và ẩn danh. Dashboard chỉ giữ bộ lọc thời gian để ai cũng có thể xem nhanh bức tranh tổng quan về doanh số, KPI và hiệu quả nguồn lead.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_cols = st.columns(4)
    with metric_cols[0]:
        render_metric("Tổng doanh số", format_currency(total_revenue), "Doanh số trước VAT trong phạm vi thời gian đang xem.")
    with metric_cols[1]:
        render_metric("% đạt KPI", format_pct(achieved_pct), f"Chênh lệch so với KPI: {format_currency(gap_to_target)}.")
    with metric_cols[2]:
        render_metric("Tổng deal", f"{total_deals:,}", f"Số khách hàng duy nhất: {total_customers:,}.")
    with metric_cols[3]:
        render_metric("Giá trị deal TB", format_currency(avg_deal_value), "Giá trị trung bình trên mỗi deal đã chốt.")

    overview_tab, marketing_tab, insight_tab = st.tabs(["Doanh số", "Marketing", "Insight"])

    with overview_tab:
        st.plotly_chart(make_line(monthly, forecast), use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(make_bar(summarize(display_sales, "department"), x="department", y="revenue", title="Doanh số theo phòng ban"), use_container_width=True)
        with col2:
            st.plotly_chart(make_bar(summarize(display_sales, "region"), x="region", y="revenue", title="Doanh số theo vùng miền"), use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(make_donut(summarize(display_sales, "need_group"), names="need_group", values="revenue", title="Doanh số theo nhu cầu"), use_container_width=True)
        with col4:
            st.plotly_chart(make_bar(summarize(display_sales, "apartment_group"), x="apartment_group", y="revenue", title="Doanh số theo loại hình căn hộ"), use_container_width=True)

        col5, col6 = st.columns(2)
        with col5:
            st.plotly_chart(make_bar(employee_kpi.head(5), x="salesperson", y="actual_revenue", title="Top 5 nhân sự có doanh số cao nhất", orientation="h"), use_container_width=True)
        with col6:
            st.plotly_chart(make_bar(employee_kpi.sort_values("kpi_completion", ascending=False).head(5), x="salesperson", y="kpi_completion", title="Top 5 nhân sự có % KPI cao nhất", orientation="h", percent_axis=True), use_container_width=True)

        st.plotly_chart(make_kpi_chart(department_kpi), use_container_width=True)

        table_left, table_right = st.columns(2)
        with table_left:
            st.markdown("### Bảng tổng hợp nhân sự")
            st.dataframe(
                employee_kpi[["salesperson", "department", "actual_revenue", "kpi_target", "kpi_completion", "actual_deals"]].rename(
                    columns={
                        "salesperson": "Nhân sự",
                        "department": "Phòng ban",
                        "actual_revenue": "Actual",
                        "kpi_target": "KPI",
                        "kpi_completion": "% KPI",
                        "actual_deals": "Số deal",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )
        with table_right:
            st.markdown("### Hiệu suất phòng ban")
            st.dataframe(
                department_kpi[["department", "actual_revenue", "kpi_target", "kpi_completion", "actual_deals", "actual_customers"]].rename(
                    columns={
                        "department": "Phòng ban",
                        "actual_revenue": "Actual",
                        "kpi_target": "KPI",
                        "kpi_completion": "% KPI",
                        "actual_deals": "Số deal",
                        "actual_customers": "Khách hàng",
                    }
                ),
                use_container_width=True,
                hide_index=True,
            )

    with marketing_tab:
        st.markdown('<div class="caption">Các chỉ số marketing hiện dùng opportunity_id trong dữ liệu hợp đồng như một proxy cho lead/cơ hội.</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(make_bar(source_summary, x="lead_source", y="revenue", title="Doanh thu theo nguồn lead"), use_container_width=True)
        with col2:
            st.plotly_chart(make_bar(source_summary, x="lead_source", y="opportunity_count", title="Số lượng lead theo nguồn"), use_container_width=True)

        col3, col4 = st.columns(2)
        with col3:
            st.plotly_chart(make_bar(source_summary, x="lead_source", y="proxy_conversion_rate", title="Proxy conversion rate theo nguồn", percent_axis=True), use_container_width=True)
        with col4:
            st.plotly_chart(make_bar(source_summary, x="lead_source", y="revenue_per_opportunity", title="Doanh thu trung bình / lead"), use_container_width=True)

        st.plotly_chart(make_bubble(source_summary), use_container_width=True)
        st.dataframe(
            source_summary[
                [
                    "lead_source",
                    "marketing_channel",
                    "revenue",
                    "opportunity_count",
                    "deal_count",
                    "proxy_conversion_rate",
                    "revenue_per_opportunity",
                ]
            ].rename(
                columns={
                    "lead_source": "Nguồn lead",
                    "marketing_channel": "Nhóm kênh",
                    "revenue": "Doanh thu",
                    "opportunity_count": "Lead/Cơ hội",
                    "deal_count": "Deal",
                    "proxy_conversion_rate": "Proxy conversion",
                    "revenue_per_opportunity": "Doanh thu / lead",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    with insight_tab:
        if alerts.empty:
            st.success("Không có phòng ban nào nằm dưới ngưỡng cảnh báo 80% KPI trong phạm vi tháng đang xem.")
        else:
            alert_text = ", ".join(
                f"{row.department} ({format_pct(float(row.kpi_completion))})"
                for row in alerts.itertuples(index=False)
            )
            st.warning(f"Cảnh báo KPI: {alert_text}")

        col1, col2 = st.columns(2)
        with col1:
            render_insights("Tổng quan kinh doanh", insights["Kinh doanh"])
        with col2:
            render_insights("Nhân sự", insights["Nhân sự"])

        col3, col4 = st.columns(2)
        with col3:
            render_insights("Marketing", insights["Marketing"])
        with col4:
            render_insights("Khuyến nghị", insights["Khuyến nghị"])

        st.markdown("### Ghi chú phiên bản public")
        st.dataframe(
            pd.DataFrame(
                [
                    {"Hạng mục": "Nguồn dữ liệu", "Chi tiết": "CSV đã chuẩn hóa, lưu trong thư mục data/ của repo."},
                    {"Hạng mục": "Mức độ công khai", "Chi tiết": "Tên khách hàng, deal và nhân sự đã được ẩn danh cho bản public."},
                    {"Hạng mục": "Forecast", "Chi tiết": "Dự báo ngắn hạn dùng linear trend trên chuỗi doanh số theo tháng."},
                ]
            ),
            use_container_width=True,
            hide_index=True,
        )


if __name__ == "__main__":
    main()
