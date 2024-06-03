from typing import Dict
from fastapi import WebSocket, APIRouter

router = APIRouter(prefix='/chat')
connections: Dict[str, WebSocket] = dict()


async def websocket_connection_manager(websocket: WebSocket, sender: str):
    connections[sender] = websocket

    try:
        while True:
            content = await websocket.receive_json()

            message = content['message']
            target = content['target']

            if target in connections.keys():
                target_socket = connections[target]
                await target_socket.send_json({'message': message, 'sender': sender})

    except Exception as e:
        del connections[sender]
        print(e)


@router.websocket('/{token}')
async def chat_of_target(websocket: WebSocket, token: str):
    await websocket_connection_manager(websocket, token)
