from fastapi import FastAPI

app = FastAPI(title="Help Desk")


@app.get("/")
def home():
    return {"message": "Help desk chal raha hai"}
