from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoits import user, chat
from config import env


app = FastAPI()

# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=env.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(chat.router)
