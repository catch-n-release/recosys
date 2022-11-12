from fastapi import FastAPI
from app.routers import users_router, movies_router, recommendations_router, data_integrity_router, train_test_check_router, predictor_check_router
from app import log, movie_recommender


async def on_startup() -> None:
    log.info("Starting Application.")
    movie_recommender.load_recommender()


app = FastAPI(on_startup=[on_startup])

app.include_router(users_router, tags=["users"])
app.include_router(movies_router, tags=["movies"])
app.include_router(
    recommendations_router,
    tags=["recommendations"],
)
app.include_router(data_integrity_router, tags=["data_integrity_checks"])
app.include_router(train_test_check_router, tags=["train_test_checks"])
app.include_router(predictor_check_router, tags=["predictor_checks"])
