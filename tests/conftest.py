import asyncio
import json
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import insert

from bookings.models import Bookings
from config import settings
from database import Base, async_session_maker, engine
from hotels import models as hotel_models
from hotels.rooms.models import Rooms
from src.main import app
from users.models import Users


@pytest.fixture(scope="session", autouse=True)
async def init_db():
    assert settings.MODE == "TEST"

    async with engine.begin() as session:
        await session.run_sync(Base.metadata.drop_all)
        await session.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f"tests/mock_{model}.json", "r") as file:
            return json.load(file)

    hotels = open_mock_json("hotels")
    bookings = open_mock_json("bookings")
    rooms = open_mock_json("rooms")
    users = open_mock_json("users")

    for booking in bookings:
        booking["date_from"] = datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.strptime(booking["date_to"], "%Y-%m-%d")

    async with async_session_maker() as session:
        add_hotels = insert(hotel_models.Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
def authenticated_client():
    with TestClient(app) as client:
        client.post(
            "/auth/login",
            json={"email": "fedor@moloko.ru", "password": "kotopes"},
        )
        assert client.cookies["booking_access_token"]
        yield client


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
