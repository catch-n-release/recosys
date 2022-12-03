from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse, FileResponse

from app import app_config
from ml.src.sifts import run_train_test_sift_suite

router = APIRouter()


@router.get("/train_test_check",
            status_code=status.HTTP_200_OK,
            response_class=HTMLResponse)
async def train_test_check():
    try:
        run_train_test_sift_suite()
        return FileResponse(app_config.app.path.tt_sift_html)
    except Exception as e:
        raise e
