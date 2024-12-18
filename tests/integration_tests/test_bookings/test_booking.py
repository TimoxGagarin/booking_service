import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id,date_from,date_to,rooms_left,status_code",
    [
        (4, "2030-05-01", "2030-05-15", 3, 201),
        (4, "2030-05-01", "2030-05-15", 4, 201),
        (4, "2030-05-01", "2030-05-15", 5, 201),
        (4, "2030-05-01", "2030-05-15", 6, 201),
        (4, "2030-05-01", "2030-05-15", 7, 201),
        (4, "2030-05-01", "2030-05-15", 8, 201),
        (4, "2030-05-01", "2030-05-15", 9, 201),
        (4, "2030-05-01", "2030-05-15", 10, 201),
        (4, "2030-05-01", "2030-05-15", 10, 409),
        (4, "2030-05-01", "2030-05-15", 10, 409),
    ],
)
async def test_add_and_get_booking(
    authenticated_client: AsyncClient,
    room_id,
    date_from,
    date_to,
    rooms_left,
    status_code,
):
    response = authenticated_client.post(
        "/bookings",
        params={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code

    response = authenticated_client.get("/bookings")
    assert len(response.json()) == rooms_left


@pytest.mark.parametrize(
    "id,count,status_code",
    [
        (4, 10, 204),
        (5, 9, 204),
    ],
)
async def test_get_and_delete_booking(
    authenticated_client: AsyncClient,
    id,
    count,
    status_code,
):
    response = authenticated_client.get("/bookings")
    assert len(response.json()) == count

    response = authenticated_client.delete(f"/bookings/{id}")
    assert response.status_code == status_code

    response = authenticated_client.get("/bookings")
    assert len(response.json()) == count - 1
