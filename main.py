from fastapi import FastAPI
from apps import routes
from tools.email import send_confirm_code

app = FastAPI()


for route in routes:
    app.include_router(route)


@app.get('/email')
async def get_email():
    await send_confirm_code()
