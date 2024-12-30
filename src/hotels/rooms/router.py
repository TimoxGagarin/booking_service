from datetime import date

from fastapi import APIRouter
from fastapi_versioning import version

from src.exceptions import NoRoomsInHotelException
from src.hotels.rooms.dao import RoomsDAO
from src.hotels.rooms.schemas import SAllRooms

router = APIRouter(tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
@version(1, 0)
async def get_hotel_rooms(hotel_id: int, date_from: date, date_to: date) -> SAllRooms:
    rooms = await RoomsDAO.find_all(hotel_id, date_from, date_to)
    if rooms is None:
        raise NoRoomsInHotelException
    return rooms
