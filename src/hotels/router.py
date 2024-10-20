from datetime import date, datetime, timezone

from fastapi import APIRouter, Query

from exceptions import HotelIsNotPresentException
from hotels.dao import HotelsDAO
from hotels.rooms.router import router as router_rooms

router = APIRouter(prefix="/hotels", tags=["Hotels"])
router.include_router(router_rooms)


@router.get("/")
async def get_hotels(
    location: str,
    date_from: date = Query(datetime.now(timezone.utc).date()),
    date_to: date = Query(datetime.now(timezone.utc).date()),
):
    hotels = await HotelsDAO.find_all(location, date_from, date_to)
    if not hotels:
        raise HotelIsNotPresentException
    return hotels


@router.get("/id/{hotel_id}")
async def get_hotel(hotel_id: int):
    hotel = await HotelsDAO.find_by_id(hotel_id)
    if not hotel:
        raise HotelIsNotPresentException
    return hotel
