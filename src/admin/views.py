from sqladmin import ModelView

from bookings.models import Bookings
from hotels.models import Hotels
from hotels.rooms.models import Rooms
from users.models import Users


class UserAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [col.name for col in Hotels.__table__.c] + [Hotels.rooms]
    name = "Отель"
    name_plural = "Отели"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [col.name for col in Rooms.__table__.c] + [
        Rooms.hotel,
        Rooms.bookings,
    ]
    name = "Номер"
    name_plural = "Номера"
    icon = "fa-solid fa-bed"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [col.name for col in Bookings.__table__.c] + [
        Bookings.user,
        Bookings.room,
    ]
    name = "Бронь"
    name_plural = "Брони"
    icon = "fa-solid fa-book"
