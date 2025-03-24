from fastapi import FastAPI
from apis import *

app = FastAPI()

from apis.admin import api_router as admin_router
from apis.quests import api_router as quest_router
from apis.Users import api_router as user_router

app.include_router(admin_router)
app.include_router(quest_router)
app.include_router(user_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # List of allowed origins
    allow_credentials=True,  # Allows credentials (such as cookies, authorization headers, etc.) to be sent in cross-origin requests
    allow_methods=["*"],  # Allows all methods (such as GET, POST, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
    expose_headers=["*"]
)
