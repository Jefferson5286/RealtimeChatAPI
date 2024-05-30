from fastapi import FastAPI

from endpoits import user, chat


app = FastAPI()

app.include_router(user.router)
app.include_router(chat.router)
