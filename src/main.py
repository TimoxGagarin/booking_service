from datetime import date
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Query

from bookings.router import router as router_bookings

app = FastAPI(docs_url="/")
app.include_router(router_bookings)


class HotelSearchArgs:
    def __init__(
        self,
        location: str,
        date_from: date,
        date_to: date,
        stars: Annotated[int | None, Query(ge=1, le=5)] = None,
        has_spa: bool | None = None,
    ):
        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.stars = stars
        self.has_spa = has_spa


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
