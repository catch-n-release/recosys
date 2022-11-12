"""Router for all data integrity check point.

Attributes:
    router (Fast ):  Used to add data integrity check routes.

"""
from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse, FileResponse

from app import app_config
from ml.sifts import run_data_integrity_suite

router = APIRouter()


@router.get("/data_integrity_check",
            status_code=status.HTTP_200_OK,
            response_class=HTMLResponse)
async def data_integrity_check():
    """Functionality to run data integrity checks using deepchecks.

    Returns:
        HTML: Deepchecks report for data intergity suite.

    Raises:
        e: All generic exceptions.
    """
    try:
        run_data_integrity_suite()
        return FileResponse(app_config.app.path.di_sift_html)
    except Exception as e:
        raise e
