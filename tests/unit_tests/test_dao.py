import pytest

from src.users.dao import UsersDAO


@pytest.mark.parametrize(
    "id,email,is_present",
    [
        (1, "fedor@moloko.ru", True),
        (2, "sharik@moloko.ru", True),
        (3, "....", False),
    ],
)
async def test_find_by_id(id, email, is_present):
    user = await UsersDAO.find_by_id(id)

    if is_present:
        assert user.id == id
        assert user.email == email
    else:
        assert not user
