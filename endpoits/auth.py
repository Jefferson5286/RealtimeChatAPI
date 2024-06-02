from asyncio import to_thread

from services.auth import *
from exceptions.user import *
from exceptions.jwt import *
from schemas.auth import *

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

    except (UserNotFoundError, AuthNotPermissionError):
        raise HTTPException(401, 'Unauthorized!')


@router.get('/refresh')
async def refresh(request: Request) -> JSONResponse:
    try:
        token = await to_thread(refresh_token, request.headers['Authorization'])

        return JSONResponse({'token': token})

    except (InvalidJSONWebTokenError, UserNotFoundError, AuthNotPermissionError):
        raise HTTPException(401, 'Unauthorized!')

    except ExpiredJSONWebToken:
        raise HTTPException(419, 'Connection will expire! authenticate again.')
