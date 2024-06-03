from typing import Dict

from exceptions.jwt import InvalidJSONWebTokenError
from config import env

from fastapi import WebSocket, WebSocketDisconnect, APIRouter, HTTPException, Depends
from jose import jwt
from jose.constants import ALGORITHMS
from jose.exceptions import JWTError


router = APIRouter(prefix='/chat')
connections: Dict[str, WebSocket] = dict()


async def websocket_connection_manager(websocket: WebSocket, sender: str):
    connections[sender] = websocket

    while True:
        content = await websocket.receive_json()

        message = content['message']
        target = content['target']

        if target in connections.keys():
            target_socket = connections[target]

            await target_socket.send_json({
                'message': message,
                'sender': sender
            })


@router.websocket('/{token}')
async def chat_of_target(websocket: WebSocket, token: str):
    try:
        await websocket_connection_manager(websocket, token)

    except InvalidJSONWebTokenError:
        await websocket.close()

        raise HTTPException(401, 'Unauthorized!')

    except Exception as e:
        await websocket.close()
        print(e)
        raise HTTPException(500, 'Internal server Error.')
