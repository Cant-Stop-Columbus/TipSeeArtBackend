from api import app

@app.get("/")
async def root():
    return {"Welcome": "to the PaySeeArt API!"}