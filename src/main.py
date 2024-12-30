import time
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI
from redis import asyncio as aioredis
from sqladmin import Admin

from src.admin.auth import authentication_backend
from src.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UserAdmin
from src.bookings.router import router as router_bookings
from src.config import settings
from src.database import engine
from src.hotels.router import router as router_hotels
from src.images.router import router as router_images
from src.logger import logger
from src.pages.router import router as router_pages
from src.users.router import router as router_users

sentry_sdk.init(settings.SENTRY_DSN, traces_sample_rate=1.0)


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf-8"
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan, docs_url="/")


app.include_router(router_users)
app.include_router(router_bookings)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)

app = VersionedFastAPI(
    app,
    version_format="{major}.{minor}",
    prefix_format="/v{major}.{minor}",
    default_version=(1, 0),
    enable_latest=False,
)

app.mount("/static", StaticFiles(directory="src/static"), "static")


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info("Request handling time", extra={"process_time": round(process_time, 4)})
    return response


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

admin = Admin(app, engine, authentication_backend=authentication_backend)


admin.add_view(UserAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(HotelsAdmin)
