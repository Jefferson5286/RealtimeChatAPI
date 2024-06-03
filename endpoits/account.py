from asyncio import to_thread
from typing import Dict

from openapi import openapi
from utils.security import Token, extract_token_request
from services.account import get_account_data
from exceptions.user import UserNotFoundError

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from pydantic import constr


router = APIRouter(prefix='/account')


DETAILS_SCHEMA = openapi.get_responses('get', '/account/details')
FIND_SCHEMA = openapi.get_responses('get', '/account/find')


@router.get('/details', responses=DETAILS_SCHEMA)
async def account_details_from_token(token: Token = Depends(extract_token_request)) -> JSONResponse:
    try:
        data: Dict[str, str] = await to_thread(get_account_data, token.uuid)

        return JSONResponse(data)

    except UserNotFoundError:
        raise HTTPException(401, 'Unauthorized!')


@router.get('/find/{uuid}', responses=FIND_SCHEMA)
async def find_account(uuid: constr(max_length=36, min_length=36)) -> JSONResponse:
    try:
        data: Dict[str, str] = await to_thread(get_account_data, uuid)

        return JSONResponse(data)

    except UserNotFoundError:
        raise HTTPException(404, f'Target not found with uuid={uuid}')
