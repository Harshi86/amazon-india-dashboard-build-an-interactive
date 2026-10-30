# Amazon India Dashboard

An interactive Streamlit dashboard for the supplied Amazon Sales Data India workbook.

## Run locally

Install Python 3.10 or newer, then run:

```powershell
python -m pip install streamlit pandas altair
python -m streamlit run app.py
```

Keep `app.py` and `amazon_sales.csv` in the same folder. The dashboard uses only local data and the filters update every KPI, chart, and table.

## Included views

- Sales, profit, order count, units sold, average order value, and profit margin
- Monthly sales and profit trends
- Delivered, shipped, returned, and cancelled order counts; return and cancellation rates
- Sales value attached to returned/cancelled orders (an indicator, not confirmed accounting loss)
- Category sales, profit, units sold, and return/cancellation shares
- Top 10 products by sales with profit and unit counts
- Sales and profit by payment method and fulfillment method
- State level sales, profit, orders, and units
- Shared date, category, state, and order status filters

The source workbook has 10,000 order rows covering April 2024 through May 2026. Sales and profit are shown as supplied in the workbook; profit margin is calculated as total profit divided by total sales.
