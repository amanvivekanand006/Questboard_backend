from fastapi import FastAPI

app = FastAPI()

from apis.admin import api_router as admin_router

app.include_router(admin_router)