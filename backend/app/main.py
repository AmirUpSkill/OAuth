from fastapi import FastAPI

# --- Create an instance --- 
app = FastAPI(title="Mission OAuth SaaS API")

@app.get("/")
def read_root():
    """
        A Simple Root Endpoint to Confirm the API is Running . 
    """
    return {
        "message" : "Welcome to the Mission OAuth SaaS API"

    }