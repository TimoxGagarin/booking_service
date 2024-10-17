from typing import Annotated

import uvicorn
from fastapi import FastAPI, Path, Query

app = FastAPI(docs_url="/")


@app.get("/hotels/{hotel_id}")
def get_hotels(
    hotel_id: Annotated[int, Path()],
    date_from: Annotated[int, Query()],
    date_to: Annotated[int, Query()],
):
    return [hotel_id, date_from, date_to]


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
