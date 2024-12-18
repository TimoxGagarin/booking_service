import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "location,date_from,date_to,count,status_code",
    [
        (None, "2030-05-01", "2030-05-15", 6, 200),
        ("Коми", "2030-05-01", "2030-05-15", 2, 200),
        (None, "2030-05-01", "2030-07-15", 6, 400),
        (None, "2030-08-01", "2030-07-15", None, 400),
        ("Республика Алтай", "2023-06-01", "2023-06-30", 3, 200),
    ],
)
async def test_add_and_get_booking(
    authenticated_client: AsyncClient, location, date_from, date_to, count, status_code
):
    response = authenticated_client.get(
        "/hotels",
        params={
            "location": location,
            "date_from": date_from,
            "date_to": date_to,
        },
    )
    assert response.status_code == status_code

    if status_code == 200:
        assert len(response.json()) == count
