import shutil

from fastapi import APIRouter, UploadFile

router = APIRouter(prefix="/images", tags=["Images uploading"])


@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    with open(f"src/static/images/{name}.webp", "wb+") as file_obj:
        shutil.copyfileobj(file.file, file_obj)
