from asyncio import to_thread

from services.auth import *
from exceptions.user import *
from exceptions.jwt import *
from schemas.auth import *
from openapi import openapi
from utils.security import Token, extract_token_request

from fastapi import APIRouter, HTTPException, Response, Depends
from fastapi.responses import JSONResponse


router = APIRouter(prefix='/auth')

LOGIN_SCHEMA = openapi.get_responses('post', '/auth/login')
REGISTER_SCHEMA = openapi.get_responses('post', '/auth/register')
REFRESH_SCHEMA = openapi.get_responses('get', '/auth/refresh')


@router.post('/register', responses=REGISTER_SCHEMA)
async def register(data: UserRegisterSchema) -> Response:
    try:
        await to_thread(create_user, data)

        return Response(status_code=201)

    except EmailAlreadyRegisteredError:
        raise HTTPException(409, 'E-mail already registered!')


@router.post('/login', responses=LOGIN_SCHEMA)
async def login(data: UserLoginSchema) -> JSONResponse:
    try:
        token = await to_thread(login_account, data)

        return JSONResponse({'token': token})

    except (UserNotFoundError, AuthNotPermissionError):
        raise HTTPException(401, 'Unauthorized!')


@router.get('/refresh', responses=REFRESH_SCHEMA)
async def refresh(token: Token = Depends(extract_token_request)) -> JSONResponse:
    try:
        new_token = await to_thread(refresh_token, token)

        return JSONResponse({'token': new_token})

    except (UserNotFoundError, AuthNotPermissionError):
        raise HTTPException(401, 'Unauthorized! Invalid Token.')
