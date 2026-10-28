from fastapi import FastAPI

app = FastAPI()


@app.get("/saude")
def saude():
    return {"status": "de pé"}
