from apis import *
from fastapi import FastAPI
from apis.admin import api_router as admin_router

app = FastAPI()
api_router = APIRouter()
app.include_router(admin_router)