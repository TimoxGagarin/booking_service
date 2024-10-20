from pydantic import BaseModel


class SRoom(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    services: list[str]
    price: int
    quantity: int
    image_id: int
    total_cost: int


class SAllRooms(BaseModel):
    rooms_left: int
    rooms: list[SRoom]
