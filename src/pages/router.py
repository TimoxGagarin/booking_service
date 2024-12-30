from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi_versioning import version

from hotels.router import get_hotels

router = APIRouter(prefix="/pages", tags=["Frontend"])

templates = Jinja2Templates(directory="src/templates")


@router.get("/hotels")
@version(1, 0)
async def get_hotels_page(request: Request, hotels=Depends(get_hotels)):
    return templates.TemplateResponse(
        name="hotels.html", context={"request": request, "hotels": hotels}
    )
