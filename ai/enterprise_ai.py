import sys
sys.stdout.reconfigure(encoding="utf-8")

import pandas as pd
from sqlalchemy import create_engine
from google import genai

# PostgreSQL Connection
engine = create_engine(
    "postgresql+psycopg2://postgres:saibaba@localhost:5432/enterprise_analytics"
)

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

print("========== SALES DATA ==========\n")
print(df)

client = genai.Client(api_key="AQ.Ab8RN6JD0KgjJJocN2prAUxfztRUyT7BfLAB5Bywrtr6No9WIQ")

prompt = f"""
You are a Senior Business Analyst.

Analyze this sales data:

{df.to_string(index=False)}

Provide:
1. Top-selling product
2. Lowest-selling product
3. Revenue analysis
4. Inventory suggestions
5. Business recommendations
"""

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)

print("\n========== AI INSIGHTS ==========\n")
from sqlalchemy import text

with engine.begin() as conn:
    conn.execute(
        text("""
            INSERT INTO ai_insights(report)
            VALUES (:report)
        """),
        {"report": response.text}
    )

print("AI report saved successfully!")