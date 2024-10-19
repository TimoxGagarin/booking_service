from fastapi import APIRouter

from bookings.dao import BookingDAO
from bookings.schemas import SBooking

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.get("/")
async def get_bookings() -> list[SBooking]:
    return await BookingDAO.find_all()
