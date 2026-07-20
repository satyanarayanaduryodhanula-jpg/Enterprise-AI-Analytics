from fastapi import FastAPI
import subprocess
app=FastAPI()
@app.get("/")
def home():
    return{"Message":"Welcome to SmartMart API"}
@app.get("/products")
def get_products():
    return[{"id":1, "name":"Laptop", "price":65000},
{"id":2, "name":"Mouse", "Price":800}]
@app.get("/customers")
def get_customers():
    return[{"id":1,"name":"Satya","State":"Hyderabad"},
           {"id":2,"name":"Sai","State":"Delhi"}]
@app.get("/orders")
def get_orders():
    return[{"id":1,"name":"Shampoo"},
           {"id":2,"name":"Soap"}]
@app.get("/inventory")
def get_inventory():
    return[{"id":1,"ItemName":"Keyboard","Category":"Electronics"},
           {"id":2,"ItemName":"ComputerSrews","Category":"Electronics"}]
@app.post("/generate-ai-report")
def generate_ai_report():

    try:
        subprocess.run(
            ["python", "ai/enterprise_ai.py"],
            check=True
        )

        return {
            "status": "Success",
            "message": "AI Report Generated Successfully"
        }

    except Exception as e:
        return {
            "status": "Failed",
            "error": str(e)
        }