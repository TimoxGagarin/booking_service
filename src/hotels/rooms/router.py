from datetime import date

from fastapi import APIRouter

from exceptions import NoRoomsInHotelException
from hotels.rooms.dao import RoomsDAO
from hotels.rooms.schemas import SAllRooms

router = APIRouter(tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_hotel_rooms(hotel_id: int, date_from: date, date_to: date) -> SAllRooms:
    rooms = await RoomsDAO.find_all(hotel_id, date_from, date_to)
    if rooms is None:
        raise NoRoomsInHotelException
    return rooms
