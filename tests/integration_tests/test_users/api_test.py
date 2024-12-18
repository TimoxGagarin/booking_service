import pytest


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("kot@pes.com", "kotopes", 200),
        ("kot@pes.com", "kotopes", 409),
        ("pes@kot.com", "pesokot", 200),
        ("abcde", "12345", 422),
    ],
)
async def test_register_user(ac, email, password, status_code):
    response = await ac.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("fedor@moloko.ru", "kotopes", 200),
        ("sharik@moloko.ru", "pesokot", 200),
        ("wrong@person.com", "1234", 401),
    ],
)
async def test_login_user(ac, email, password, status_code):
    response = await ac.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert response.status_code == status_code
