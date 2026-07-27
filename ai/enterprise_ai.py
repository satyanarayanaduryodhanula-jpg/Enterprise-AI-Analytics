import sys
sys.stdout.reconfigure(encoding="utf-8")

import os
import json
import pandas as pd

from dotenv import load_dotenv
from sqlalchemy import text
from google import genai
from database.db import engine


# ==============================
# Load Environment Variables
# ==============================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )


# ==============================
# Fetch Sales Data
# ==============================

query = """
SELECT
    p.product_name,
    SUM(o.quantity) AS total_quantity,
    SUM(o.quantity * p.price) AS revenue
FROM orders o
JOIN products p
ON o.product_id = p.product_id
GROUP BY p.product_name
ORDER BY revenue DESC;
"""

df = pd.read_sql(query, engine)

print("\n========== SALES DATA ==========\n")
print(df)

# ==============================
# Gemini Client
# ==============================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ==============================
# Prompt
# ============================== 

# ==============================
# Prompt
# ==============================

prompt = f"""
You are an AI Business Analyst.

Analyze the following sales data.

Sales Data:
{df.to_string(index=False)}

Return ONLY valid JSON.

Do not write explanations.
Do not use markdown.
Do not use headings.

Return exactly this JSON:

{{
  "business_health": 95,
  "best_product": "",
  "worst_product": "",
  "total_revenue": 0,
  "average_revenue": 0,
  "inventory_risk": "",
  "recommendation": ""
}}

Replace the values using the sales data.

Output ONLY JSON.
"""

# ==============================
# Gemini Response
# ==============================

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)

print("\n========== GEMINI RAW RESPONSE ==========\n")
print(response.text)

# ==============================
# Convert JSON Text to Dictionary
# ==============================

json_text = response.text.strip()

# Remove markdown if Gemini returns ```json ... ```
if json_text.startswith("```"):
    json_text = json_text.replace("```json", "")
    json_text = json_text.replace("```", "")
    json_text = json_text.strip()

ai_data = json.loads(json_text)

print("\n========== PYTHON DICTIONARY ==========\n")
print(ai_data)

print("\nBusiness Health :", ai_data["business_health"])
print("Best Product    :", ai_data["best_product"])
print("Worst Product   :", ai_data["worst_product"])
print("Revenue         :", ai_data["total_revenue"])

# ==============================
# Save into PostgreSQL
# ==============================

with engine.begin() as conn:

    conn.execute(

        text("""

INSERT INTO ai_insights(

business_health,
best_product,
worst_product,
total_revenue,
average_revenue,
inventory_risk,
recommendation

)

VALUES(

:business_health,
:best_product,
:worst_product,
:total_revenue,
:average_revenue,
:inventory_risk,
:recommendation

)

"""),

        ai_data

    )

print("\n AI report saved successfully!")
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os
# ==============================
# Generate PDF Report
# ==============================

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER

from datetime import datetime
import os


# ==============================
# Create Reports Folder
# ==============================

os.makedirs("ai/reports", exist_ok=True)

pdf_path = "ai/reports/latest_ai_report.pdf"


# ==============================
# PDF Document
# ==============================

doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    rightMargin=50,
    leftMargin=50,
    topMargin=50,
    bottomMargin=50
)


# ==============================
# Styles
# ==============================

styles = getSampleStyleSheet()

title_style = styles["Title"]
title_style.alignment = TA_CENTER
title_style.fontSize = 22
title_style.spaceAfter = 10

subtitle_style = styles["Heading3"]
subtitle_style.alignment = TA_CENTER

body_style = styles["BodyText"]
body_style.fontSize = 10
body_style.leading = 15

heading_style = styles["Heading2"]
heading_style.fontSize = 15
heading_style.spaceAfter = 10


# ==============================
# PDF Content
# ==============================

story = []


# Title

story.append(
    Paragraph(
        "Enterprise AI Analytics Report",
        title_style
    )
)

story.append(
    Paragraph(
        "AI-Generated Business Performance Report",
        subtitle_style
    )
)

story.append(Spacer(1, 8))

story.append(
    Paragraph(
        f"Generated: {datetime.now().strftime('%d-%b-%Y %I:%M %p')}",
        styles["BodyText"]
    )
)

story.append(Spacer(1, 25))


# ==============================
# KPI Table
# ==============================

kpi_data = [

    ["Business Metric", "Value"],

    [
        "Business Health",
        f"{ai_data['business_health']}%"
    ],

    [
        "Best Product",
        str(ai_data["best_product"])
    ],

    [
        "Worst Product",
        str(ai_data["worst_product"])
    ],

    [
        "Total Revenue",
        f"INR {float(ai_data['total_revenue']):,.0f}"
    ],

    [
        "Average Revenue",
        f"INR {float(ai_data['average_revenue']):,.0f}"
    ]

]


kpi_table = Table(
    kpi_data,
    colWidths=[180, 250]
)


kpi_table.setStyle(

    TableStyle([

        # Header
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            colors.HexColor("#1E3A8A")
        ),

        (
            "TEXTCOLOR",
            (0, 0),
            (-1, 0),
            colors.white
        ),

        (
            "FONTNAME",
            (0, 0),
            (-1, 0),
            "Helvetica-Bold"
        ),

        # First column
        (
            "FONTNAME",
            (0, 1),
            (0, -1),
            "Helvetica-Bold"
        ),

        # Table
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.5,
            colors.grey
        ),

        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "MIDDLE"
        ),

        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            10
        ),

        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            10
        ),

        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            8
        ),

        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            8
        )

    ])

)


story.append(kpi_table)

story.append(Spacer(1, 30))


# ==============================
# Inventory Risk
# ==============================

story.append(
    Paragraph(
        "Inventory Risk",
        heading_style
    )
)

story.append(
    Paragraph(
        str(ai_data["inventory_risk"]),
        body_style
    )
)

story.append(Spacer(1, 25))


# ==============================
# AI Recommendation
# ==============================

story.append(
    Paragraph(
        "AI Recommendation",
        heading_style
    )
)

story.append(
    Paragraph(
        str(ai_data["recommendation"]),
        body_style
    )
)

story.append(Spacer(1, 35))


# ==============================
# Footer
# ==============================

story.append(
    Paragraph(
        "<b>Enterprise AI Analytics</b>",
        body_style
    )
)

story.append(
    Paragraph(
        "Automatically generated from enterprise sales data using AI.",
        body_style
    )
)


# ==============================
# Build PDF
# ==============================

doc.build(story)

print("PDF Generated Successfully!")