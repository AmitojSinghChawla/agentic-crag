from fastapi import FastAPI , HTTPException

app = FastAPI()


@app.get("/")
def health():
    """ simple end point to check if the app is working """
    return {"status": "running"}

