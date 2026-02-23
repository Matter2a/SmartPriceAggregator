from fastapi import FastAPI

app = FastAPI(title="Smart Price Aggregator")

@app.get("/")
async def root():
    return {"status": "ok"}
