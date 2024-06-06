from fastapi import FastAPI
from fastapi_pagination import add_pagination
from fastapi_python.routers import api_router

app = FastAPI(title='WorkoutApi')

app.include_router(api_router)
add_pagination(app) 