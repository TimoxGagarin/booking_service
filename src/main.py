from contextlib import asynccontextmanager
from datetime import date
from typing import Annotated

import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from bookings.router import router as router_bookings
from config import settings
from hotels.router import router as router_hotels
from images.router import router as router_images
from pages.router import router as router_pages
from users.router import router as router_users


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf-8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan, docs_url="/")


app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)

app.mount("/static", StaticFiles(directory="src/static"), "static")

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
