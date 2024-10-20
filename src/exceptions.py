from fastapi import HTTPException, status

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="User is already exists."
)

IncorrectEmailOrPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password."
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token had expired."
)

TokenAbsentException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token absent."
)

IncorrectTokenFormatException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect token format."
)

UserIsNotPresentException = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
