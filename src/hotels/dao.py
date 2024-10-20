from datetime import date

from sqlalchemy import and_, func, or_, select

from bookings.models import Bookings
from dao.base import BaseDAO
from database import async_session_maker
from hotels.models import Hotels
from hotels.rooms.models import Rooms


class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(cls, hotel_location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms = (
                select(Rooms.id)
                .join(Bookings, Rooms.id == Bookings.room_id)
                .where(
                    and_(
                        or_(
                            and_(
                                Bookings.date_from <= date_to,
                                Bookings.date_to >= date_from,
                            ),
                            and_(
                                Bookings.date_from >= date_from,
                                Bookings.date_to <= date_to,
                            ),
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            # Основной запрос
            query = (
                select(
                    Hotels.id,
                    Hotels.name,
                    Hotels.location,
                    Hotels.services,
                    Hotels.rooms_quantity,
                    Hotels.image_id,
                    (Hotels.rooms_quantity - func.count(booked_rooms.c.id)).label(
                        "rooms_left"
                    ),
                )
                .outerjoin(Rooms, Hotels.id == Rooms.hotel_id)
                .outerjoin(booked_rooms, booked_rooms.c.id == Rooms.id)
                .where(Hotels.location.like(f"%{hotel_location}%"))
                .group_by(Hotels.id)
                .having(func.count(booked_rooms.c.id) < Hotels.rooms_quantity)
            )

            result = await session.execute(query)
            return result.mappings().all()
