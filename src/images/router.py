import shutil

from fastapi import APIRouter, UploadFile
from fastapi_versioning import version

from tasks.tasks import process_pic

router = APIRouter(prefix="/images", tags=["Images uploading"])


@router.post("/hotels")
@version(1, 0)
async def add_hotel_image(name: int, file: UploadFile):
    path = f"static/images/{name}.webp"
    with open("src/" + path, "wb+") as file_obj:
        shutil.copyfileobj(file.file, file_obj)
    process_pic.delay(path)
