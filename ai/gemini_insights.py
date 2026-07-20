import sys
sys.stdout.reconfigure(encoding="utf-8")

from google import genai

client = genai.Client(
    api_key="AQ.Ab8RN6JD0KgjJJocN2prAUxfztRUyT7BfLAB5Bywrtr6No9WIQ"
)

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Say exactly: Hello Satya. Do not use emojis."
)

print(response.text)