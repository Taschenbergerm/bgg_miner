import json
import pathlib

from fastapi import FastAPI

file = pathlib.Path(__file__).parent / "out" / "boardgames_chunk_157000_157319.json"
db = json.load(file.open())

app = FastAPI()


@app.get("/boardgames/{id}")
async def get_boardgame(id: int):
    return db[id]


@app.get("/boardgames/")
async def get_all_boardgames():
    return db


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
