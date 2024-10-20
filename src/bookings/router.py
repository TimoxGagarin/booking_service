from datetime import date

from fastapi import APIRouter, Depends, status

from bookings.dao import BookingDAO
from bookings.schemas import SBooking
from exceptions import RoomCannotBeBookedException
from users.dependencies import get_current_user
from users.models import Users

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBookedException
    return booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_booking(
    booking_id: int,
    user: Users = Depends(get_current_user),
):
    await BookingDAO.delete(user_id=user.id, id=booking_id)
