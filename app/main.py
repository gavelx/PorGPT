from fastapi import FastAPI

app = FastAPI(
    title="PorGPT - Emissor de NF-e",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"status": "Emissor NF-e ativo"}
