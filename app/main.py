from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import FileResponse

from sqlalchemy import text
from database.db import engine

import subprocess

app = FastAPI(title="Enterprise AI Analytics")

# Static Files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")


# ===========================
# Dashboard
# ===========================

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html"
    )


# ===========================
# KPI DATA
# ===========================

@app.get("/kpi-data")
def kpi_data():

    with engine.connect() as conn:

        revenue = conn.execute(text("""
        SELECT COALESCE(SUM(o.quantity * p.price),0)
        FROM orders o
        JOIN products p
        ON o.product_id = p.product_id
        """)).scalar()

        orders = conn.execute(text("""
        SELECT COUNT(*)
        FROM orders
        """)).scalar()

        customers = conn.execute(text("""
        SELECT COUNT(*)
        FROM customers
        """)).scalar()

    average = revenue / orders if orders else 0

    return {
        "revenue": float(revenue),
        "orders": orders,
        "customers": customers,
        "average_order": round(float(average), 2)
    }


# ===========================
# SALES CHART
# ===========================

@app.get("/sales-chart")
def sales_chart():

    with engine.connect() as conn:

        rows = conn.execute(text("""
        SELECT
            p.product_name,
            SUM(o.quantity * p.price) AS revenue
        FROM orders o
        JOIN products p
        ON o.product_id = p.product_id
        GROUP BY p.product_name
        ORDER BY revenue DESC
        """)).mappings().all()

    return [
        {
            "product": row["product_name"],
            "revenue": float(row["revenue"])
        }
        for row in rows
    ]


# ===========================
# LATEST AI REPORT
# ===========================

@app.get("/latest-ai-report")
def latest_ai_report():

    with engine.connect() as conn:

        result = conn.execute(text("""
        SELECT *
        FROM ai_insights
        ORDER BY generated_at DESC
        LIMIT 1
        """))

        row = result.mappings().first()

    if row is None:
        return {
            "message": "No AI report available."
        }

    report = dict(row)

    report["generated_at"] = report["generated_at"].strftime("%d-%b-%Y %I:%M %p")

    return report


# ===========================
# GENERATE AI REPORT
# ===========================

@app.post("/generate-ai-report")
def generate_ai_report():

    subprocess.run(
        ["python", "-m", "ai.enterprise_ai"],
        check=True
    )

    return {
        "message": "AI Report Generated Successfully"
    }
@app.get("/download-report")
def download_report():

    pdf_path = "ai/reports/latest_ai_report.pdf"

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename="Enterprise_AI_Analytics_Report.pdf"
    )