from asyncio import to_thread

from services.user import *
from exceptions.user import *
from schemas.user import *

from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import JSONResponse


router = APIRouter(prefix='/auth')


@router.post('/register')
async def register(data: UserRegisterSchema) -> Response:
    try:
        await to_thread(create_user, data)

        return Response(status_code=201)

    except EmailAlreadyRegisteredError:
        raise HTTPException(409, 'E-mail already registered!')


@router.post('/login')
async def login(data: UserLoginSchema) -> JSONResponse:
    try:
        token = await to_thread(login_account, data)

        return JSONResponse({'token': token})

    except UserNotFoundError:
        raise HTTPException(401, 'Unauthorized!')

    except AuthNotPermissionError:
        raise HTTPException(401, 'Unauthorized!')


@router.get('/refresh')
async def refresh(request: Request) -> JSONResponse:
    try:
        last_token = request.headers['Authorization']

        token = await to_thread(refresh_token, last_token)

        return JSONResponse({'token': token})

    except InvalidJSONWebTokenError:
        raise HTTPException(401, 'Unauthorized!')
