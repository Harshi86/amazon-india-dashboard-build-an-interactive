from pathlib import Path
import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Amazon India | Sapphire IQ", page_icon="📦", layout="wide", initial_sidebar_state="expanded")

DATA = Path(__file__).with_name("amazon_sales.csv")
NAVY = "#10233F"
BLUE = "#2D6CDF"
TEAL = "#16A6A1"
GOLD = "#F4A340"
MUTED = "#718096"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA, encoding="utf-8-sig")
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")
    for c in ["Quantity", "Unit_Price_INR", "Discount_Pct", "Total_Sales_INR", "Profit_INR"]:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    return df.dropna(subset=["Order_Date"])

df = load_data()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');
.stApp { background:#F5F7FB; color:#172B4D; font-family:'DM Sans',sans-serif; }
[data-testid="stSidebar"] {background:#10233F;}
[data-testid="stSidebar"] * {color:#EAF0FA;}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {color:#B6C5DA;}
.block-container {padding-top:1.8rem; padding-bottom:2.5rem; max-width:1480px;}
h1,h2,h3 {font-family:'Manrope',sans-serif; letter-spacing:-.035em; color:#142A49;}
.eyebrow {text-transform:uppercase; letter-spacing:.16em; font-size:11px; color:#73849A; font-weight:700; margin-bottom:5px;}
.hero {display:flex; justify-content:space-between; align-items:center; padding:6px 2px 18px;}
.hero-title {font-family:Manrope,sans-serif;font-size:32px;line-height:1.1;font-weight:800;color:#142A49;letter-spacing:-1.3px;}
.hero-sub {font-size:13px;color:#73849A;margin-top:8px;}
.badge {background:#E8F1FF;color:#2862C4;border:1px solid #D5E4FF;padding:8px 12px;border-radius:99px;font-size:12px;font-weight:700;}
.kpi {background:white;border:1px solid #E8EDF4;border-radius:15px;padding:18px 19px;box-shadow:0 3px 12px #263c5a08;min-height:112px;}
.kpi-label {font-size:12px;font-weight:600;color:#74839A;display:flex;align-items:center;gap:7px;}
.kpi-value {font-family:Manrope,sans-serif;font-size:25px;font-weight:800;color:#162E4D;margin-top:9px;letter-spacing:-.8px;}
.kpi-foot {font-size:11px;color:#91A0B4;margin-top:4px;}
.section-head {display:flex;align-items:end;justify-content:space-between;margin:24px 0 8px;}
.section-head h3 {font-size:17px;margin:0;}
.section-head span {font-size:11px;color:#91A0B4;}
.panel {background:white;border:1px solid #E8EDF4;border-radius:15px;padding:16px 18px;box-shadow:0 3px 12px #263c5a08;}
div[data-testid="stTabs"] button {font-weight:700;}
div[data-testid="stDataFrame"] {border:1px solid #E8EDF4;border-radius:12px;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ◈  SAPPHIRE IQ")
    st.markdown("Amazon India · Business intelligence")
    st.markdown("---")
    st.markdown("**FILTERS**")
    min_date, max_date = df.Order_Date.min().date(), df.Order_Date.max().date()
    date_range = st.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
    categories = sorted(df.Category.dropna().unique())
    selected_categories = st.multiselect("Category", categories, placeholder="All categories")
    states = sorted(df.Ship_State.dropna().unique())
    selected_states = st.multiselect("Ship state", states, placeholder="All states")
    statuses = sorted(df.Order_Status.dropna().unique())
    selected_statuses = st.multiselect("Order status", statuses, placeholder="All statuses")
    st.markdown("---")
    st.caption("Source: Amazon Sales Data India · 10,000 orders")

f = df.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    f = f[f.Order_Date.dt.date.between(date_range[0], date_range[1])]
if selected_categories: f = f[f.Category.isin(selected_categories)]
if selected_states: f = f[f.Ship_State.isin(selected_states)]
if selected_statuses: f = f[f.Order_Status.isin(selected_statuses)]

sales = f.Total_Sales_INR.sum()
profit = f.Profit_INR.sum()
orders = f.Order_ID.nunique()
units = f.Quantity.sum()
margin = profit / sales * 100 if sales else 0
avg_order = sales / orders if orders else 0

st.markdown(f'''<div class="hero"><div><div class="eyebrow">COMMERCE PERFORMANCE · INDIA</div><div class="hero-title">Amazon India Dashboard</div><div class="hero-sub">A clear view of sales, customers, products and operations across your marketplace.</div></div><div class="badge">● &nbsp; LIVE VIEW &nbsp; · &nbsp; {len(f):,} records</div></div>''', unsafe_allow_html=True)

def money(v, compact=False):
    if compact:
        if abs(v) >= 1e7: return f"₹{v/1e7:.2f} Cr"
        if abs(v) >= 1e5: return f"₹{v/1e5:.2f} L"
    return "₹" + format(v, ",.0f")

cards = [
    ("◉", "TOTAL SALES", money(sales, True), f"{orders:,} unique orders"),
    ("↗", "TOTAL PROFIT", money(profit, True), f"{margin:.1f}% sales margin"),
    ("▤", "TOTAL ORDERS", f"{orders:,}", "Unique filtered orders"),
    ("□", "UNITS SOLD", f"{units:,.0f}", "Total quantity across orders"),
    ("◎", "AVG. ORDER VALUE", money(avg_order), "Sales divided by unique orders"),
    ("％", "PROFIT MARGIN", f"{margin:.1f}%", "Profit divided by sales"),
]
cols = st.columns(3, gap="medium")
for c,(icon,label,value,foot) in zip(cols,cards):
    c.markdown(f'<div class="kpi"><div class="kpi-label"><span style="color:{BLUE};font-size:16px">{icon}</span>{label}</div><div class="kpi-value">{value}</div><div class="kpi-foot">{foot}</div></div>',unsafe_allow_html=True)
cols = st.columns(3, gap="medium")
for c,(icon,label,value,foot) in zip(cols,cards[3:]):
    c.markdown(f'<div class="kpi"><div class="kpi-label"><span style="color:{BLUE};font-size:16px">{icon}</span>{label}</div><div class="kpi-value">{value}</div><div class="kpi-foot">{foot}</div></div>',unsafe_allow_html=True)

st.markdown('<div class="section-head"><h3>Performance overview</h3><span>All values reflect the selected filters</span></div>', unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["◈  Overview", "▣  Products & operations", "⌖  Geography"])

def chart_style(chart, height=300):
    return chart.properties(height=height).configure_view(stroke="transparent").configure_axis(labelColor="#7A899D", titleColor="#7A899D", domainColor="#E7ECF3", tickColor="#E7ECF3", gridColor="#F0F3F7", labelFont="DM Sans", titleFont="DM Sans", labelFontSize=11).configure_title(font="Manrope", color="#183252", fontSize=14, anchor="start", offset=12).configure_legend(labelColor="#718096", titleColor="#718096", labelFont="DM Sans", titleFont="DM Sans")

with tab1:
    left,right=st.columns([1.55,1],gap="medium")
    monthly=f.assign(Month=f.Order_Date.dt.to_period("M").dt.to_timestamp()).groupby("Month",as_index=False).agg(Sales=("Total_Sales_INR","sum"),Profit=("Profit_INR","sum"))
    line=alt.Chart(monthly).transform_fold(["Sales","Profit"],as_=["Metric","INR"]).mark_line(point=alt.OverlayMarkDef(filled=True,size=36),strokeWidth=2.7).encode(x=alt.X("Month:T",title=None,axis=alt.Axis(format="%b '%y",labelAngle=0,tickCount=7)),y=alt.Y("INR:Q",title="Amount (₹)",axis=alt.Axis(format="~s")),color=alt.Color("Metric:N",scale=alt.Scale(domain=["Sales","Profit"],range=[BLUE,TEAL]),legend=alt.Legend(orient="top",title=None)),tooltip=[alt.Tooltip("Month:T",title="Month",format="%b %Y"),alt.Tooltip("Metric:N"),alt.Tooltip("INR:Q",title="Amount",format=",.0f")])
    with left: st.altair_chart(chart_style(line,300),use_container_width=True)
    status=f.groupby("Order_Status",as_index=False).agg(Orders=("Order_ID","nunique"),Sales=("Total_Sales_INR","sum"))
    donut=alt.Chart(status).mark_arc(innerRadius=68,outerRadius=105,stroke="white",strokeWidth=3).encode(theta=alt.Theta("Orders:Q"),color=alt.Color("Order_Status:N",scale=alt.Scale(scheme="tableau10"),legend=alt.Legend(orient="bottom",title=None)),tooltip=["Order_Status:N",alt.Tooltip("Orders:Q",format=","),alt.Tooltip("Sales:Q",format=",.0f")])
    with right:
        st.altair_chart(chart_style(donut,270),use_container_width=True)
        returned=status.loc[status.Order_Status.str.casefold().eq("returned"),"Orders"].sum()
        cancelled=status.loc[status.Order_Status.str.casefold().eq("cancelled"),"Orders"].sum()
        returned_sales=status.loc[status.Order_Status.str.casefold().eq("returned"),"Sales"].sum()
        cancelled_sales=status.loc[status.Order_Status.str.casefold().eq("cancelled"),"Sales"].sum()
        m1,m2=st.columns(2)
        m1.metric("Return rate",f"{returned/orders:.1%}" if orders else "0.0%",help="Returned orders divided by all filtered orders")
        m2.metric("Cancellation rate",f"{cancelled/orders:.1%}" if orders else "0.0%",help="Cancelled orders divided by all filtered orders")
        m3,m4=st.columns(2)
        m3.metric("Sales value in returned orders",money(returned_sales,True),help="Sales recorded on returned orders; a value indicator, not confirmed accounting loss")
        m4.metric("Sales value in cancelled orders",money(cancelled_sales,True),help="Sales recorded on cancelled orders; a value indicator, not confirmed accounting loss")
        status["Share"]=status.Orders/orders if orders else 0
        st.dataframe(status.rename(columns={"Order_Status":"Status","Orders":"Orders","Share":"Order share"})[["Status","Orders","Order share"]].style.format({"Orders":"{:,.0f}","Order share":"{:.1%}"}),use_container_width=True,hide_index=True)
    l,r=st.columns(2,gap="medium")
    cat=f.groupby("Category",as_index=False).agg(Sales=("Total_Sales_INR","sum"),Profit=("Profit_INR","sum"),Units=("Quantity","sum")).nlargest(8,"Sales").sort_values("Sales")
    bc=alt.Chart(cat).transform_fold(["Sales","Profit"],as_=["Metric","INR"]).mark_bar(cornerRadiusEnd=4).encode(x=alt.X("INR:Q",title="Sales / profit (₹)",axis=alt.Axis(format="~s")),y=alt.Y("Category:N",sort="-x",title=None),yOffset="Metric:N",color=alt.Color("Metric:N",scale=alt.Scale(domain=["Sales","Profit"],range=[BLUE,TEAL]),legend=alt.Legend(orient="top",title=None)),tooltip=["Category:N","Metric:N",alt.Tooltip("INR:Q",format=",.0f"),alt.Tooltip("Units:Q",title="Units sold",format=",")])
    with l: st.altair_chart(chart_style(bc,300),use_container_width=True)
    pay=f.groupby("Payment_Method",as_index=False).agg(Sales=("Total_Sales_INR","sum"),Profit=("Profit_INR","sum"),Orders=("Order_ID","nunique"))
    pc=alt.Chart(pay).transform_fold(["Sales","Profit"],as_=["Metric","INR"]).mark_bar(cornerRadiusEnd=4).encode(x=alt.X("INR:Q",title="Sales / profit (₹)",axis=alt.Axis(format="~s")),y=alt.Y("Payment_Method:N",sort="-x",title=None),yOffset="Metric:N",color=alt.Color("Metric:N",scale=alt.Scale(domain=["Sales","Profit"],range=[BLUE,TEAL]),legend=alt.Legend(orient="top",title=None)),tooltip=["Payment_Method:N","Metric:N",alt.Tooltip("INR:Q",format=",.0f"),alt.Tooltip("Orders:Q",format=",")])
    with r: st.altair_chart(chart_style(pc,300),use_container_width=True)
    st.markdown('<div class="section-head"><h3>Returns & cancellations by category</h3><span>Share of category orders</span></div>',unsafe_allow_html=True)
    cat_status=f.groupby(["Category","Order_Status"]).agg(Orders=("Order_ID","nunique")).reset_index()
    cat_totals=f.groupby("Category").Order_ID.nunique().rename("Total").reset_index()
    cat_status=cat_status.merge(cat_totals,on="Category")
    cat_status=cat_status[cat_status.Order_Status.str.casefold().isin(["returned","cancelled"])].copy()
    cat_status["Rate"]=cat_status.Orders/cat_status.Total
    rate_chart=alt.Chart(cat_status).mark_bar(cornerRadiusEnd=4).encode(x=alt.X("Rate:Q",title="Share of category orders",axis=alt.Axis(format=".0%")),y=alt.Y("Category:N",sort="-x",title=None),yOffset="Order_Status:N",color=alt.Color("Order_Status:N",scale=alt.Scale(domain=["Returned","Cancelled"],range=[GOLD,"#E86A73"]),legend=alt.Legend(orient="top",title=None)),tooltip=["Category:N","Order_Status:N",alt.Tooltip("Rate:Q",format=".1%"),alt.Tooltip("Orders:Q",format=",")])
    st.altair_chart(chart_style(rate_chart,260),use_container_width=True)

with tab2:
    l,r=st.columns(2,gap="medium")
    products=f.groupby("Product",as_index=False).agg(Sales=("Total_Sales_INR","sum"),Profit=("Profit_INR","sum"),Units=("Quantity","sum"),Orders=("Order_ID","nunique")).sort_values("Sales",ascending=False).head(10).sort_values("Sales")
    prod=alt.Chart(products).mark_bar(cornerRadiusEnd=5,color=TEAL).encode(x=alt.X("Sales:Q",title="Sales (₹)",axis=alt.Axis(format="~s")),y=alt.Y("Product:N",sort="-x",title=None),tooltip=["Product:N",alt.Tooltip("Sales:Q",format=",.0f"),alt.Tooltip("Profit:Q",format=",.0f"),"Units:Q"])
    with l: st.altair_chart(chart_style(prod,390),use_container_width=True)
    fulfill=f.groupby("Fulfillment",as_index=False).agg(Orders=("Order_ID","nunique"),Sales=("Total_Sales_INR","sum"),Profit=("Profit_INR","sum"))
    fc=alt.Chart(fulfill).transform_fold(["Sales","Profit"],as_=["Metric","INR"]).mark_bar(cornerRadiusEnd=4).encode(x=alt.X("INR:Q",title="Sales / profit (₹)",axis=alt.Axis(format="~s")),y=alt.Y("Fulfillment:N",sort="-x",title=None),yOffset="Metric:N",color=alt.Color("Metric:N",scale=alt.Scale(domain=["Sales","Profit"],range=[BLUE,TEAL]),legend=alt.Legend(orient="top",title=None)),tooltip=["Fulfillment:N","Metric:N",alt.Tooltip("INR:Q",format=",.0f"),alt.Tooltip("Orders:Q",format=",")])
    with r: st.altair_chart(chart_style(fc,390),use_container_width=True)
    cat_all=f.groupby("Category",as_index=False).agg(Sales=("Total_Sales_INR","sum"),Profit=("Profit_INR","sum"),Units=("Quantity","sum"),Orders=("Order_ID","nunique"))
    st.markdown('<div class="section-head"><h3>Category performance</h3><span>Sales, profit and units sold</span></div>',unsafe_allow_html=True)
    st.dataframe(cat_all.sort_values("Sales",ascending=False).rename(columns={"Category":"Category","Sales":"Sales (₹)","Profit":"Profit (₹)","Units":"Units sold","Orders":"Orders"}).style.format({"Sales (₹)":"₹{:,.0f}","Profit (₹)":"₹{:,.0f}","Units sold":"{:,.0f}","Orders":"{:,.0f}"}),use_container_width=True,hide_index=True)
    st.markdown('<div class="section-head"><h3>Top products</h3><span>Ranked by sales</span></div>',unsafe_allow_html=True)
    st.dataframe(products.sort_values("Sales",ascending=False).rename(columns={"Sales":"Sales (₹)","Profit":"Profit (₹)","Units":"Units","Orders":"Orders"}).style.format({"Sales (₹)":"₹{:,.0f}","Profit (₹)":"₹{:,.0f}","Units":"{:,.0f}","Orders":"{:,.0f}"}),use_container_width=True,hide_index=True)

with tab3:
    state=f.groupby("Ship_State",as_index=False).agg(Sales=("Total_Sales_INR","sum"),Profit=("Profit_INR","sum"),Orders=("Order_ID","nunique"),Units=("Quantity","sum")).sort_values("Sales",ascending=False)
    l,r=st.columns([1.4,1],gap="medium")
    sc=alt.Chart(state.head(15).sort_values("Sales")).transform_fold(["Sales","Profit"],as_=["Metric","INR"]).mark_bar(cornerRadiusEnd=4).encode(x=alt.X("INR:Q",title="Sales / profit (₹)",axis=alt.Axis(format="~s")),y=alt.Y("Ship_State:N",sort="-x",title=None),yOffset="Metric:N",color=alt.Color("Metric:N",scale=alt.Scale(domain=["Sales","Profit"],range=[BLUE,TEAL]),legend=alt.Legend(orient="top",title=None)),tooltip=["Ship_State:N","Metric:N",alt.Tooltip("INR:Q",format=",.0f"),alt.Tooltip("Orders:Q",format=",")])
    with l: st.altair_chart(chart_style(sc,480),use_container_width=True)
    state["Share"] = state.Sales / state.Sales.sum() * 100 if state.Sales.sum() else 0
    with r:
        st.markdown('<div class="section-head"><h3>State performance</h3><span>Sorted by sales</span></div>',unsafe_allow_html=True)
        st.dataframe(state.rename(columns={"Ship_State":"State","Sales":"Sales (₹)","Profit":"Profit (₹)","Orders":"Orders","Units":"Units","Share":"Sales share (%)"}).style.format({"Sales (₹)":"₹{:,.0f}","Profit (₹)":"₹{:,.0f}","Orders":"{:,.0f}","Units":"{:,.0f}","Sales share (%)":"{:.1f}%"}),use_container_width=True,hide_index=True,height=480)

st.markdown('<div style="text-align:center;color:#9AA7B8;font-size:11px;padding:24px 0 2px">Amazon India · Sapphire IQ &nbsp; · &nbsp; Interactive sales intelligence</div>',unsafe_allow_html=True)
