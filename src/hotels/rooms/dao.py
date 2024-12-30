from datetime import date

from sqlalchemy import and_, func, or_, select

from src.bookings.models import Bookings
from src.dao.base import BaseDAO
from src.database import async_session_maker
from src.hotels.rooms.models import Rooms


class RoomsDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms = (
                select(func.count(Rooms.id))
                .select_from(Rooms)
                .join(Bookings, Rooms.id == Bookings.room_id)
                .where(
                    and_(
                        Rooms.hotel_id == hotel_id,
                        or_(
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_from <= date_to,
                            ),
                            and_(
                                Bookings.date_from <= date_from,
                                Bookings.date_to > date_from,
                            ),
                        ),
                    )
                )
            )

            rooms_left = await session.execute(booked_rooms)
            query = select(
                Rooms.id,
                Rooms.hotel_id,
                Rooms.name,
                Rooms.description,
                Rooms.services,
                Rooms.price,
                Rooms.quantity,
                Rooms.image_id,
                (Rooms.price * (date_to - date_from).days).label("total_cost"),
            ).filter_by(hotel_id=hotel_id)
            result = await session.execute(query)
            return {
                "rooms_left": rooms_left.scalar(),
                "rooms": result.mappings().all(),
            }
