from datetime import date, datetime, timezone

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache
from fastapi_versioning import version

from src.exceptions import (
    DateFromGreaterThanDateTo,
    HotelIsNotPresentException,
    TooLongDelta,
)
from src.hotels.dao import HotelsDAO
from src.hotels.rooms.router import router as router_rooms

router = APIRouter(prefix="/hotels", tags=["Hotels"])
router.include_router(router_rooms)


@router.get("")
@version(1, 0)
@cache(expire=20)
async def get_hotels(
    location: str,
    date_from: date = Query(datetime.now(timezone.utc).date()),
    date_to: date = Query(datetime.now(timezone.utc).date()),
):
    if date_from > date_to:
        raise DateFromGreaterThanDateTo
    if (date_to - date_from).days > 30:
        raise TooLongDelta
    hotels = await HotelsDAO.find_all(location, date_from, date_to)
    if not hotels:
        raise HotelIsNotPresentException
    return hotels


@router.get("/id/{hotel_id}")
@version(1, 0)
async def get_hotel(hotel_id: int):
    hotel = await HotelsDAO.find_by_id(hotel_id)
    if not hotel:
        raise HotelIsNotPresentException
    return hotel
