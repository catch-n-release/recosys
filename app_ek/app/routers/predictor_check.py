from fastapi import APIRouter, status
from fastapi.responses import HTMLResponse, FileResponse

from app import app_config
from ml.src.sifts import run_predictor_eval_suite

router = APIRouter()


@router.get(
    "/predictor_check",
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
async def predictor_check():
    try:
        run_predictor_eval_suite()
        return FileResponse(app_config.app.path.algo_eval_sift_html)
    except Exception as e:
        raise e
