from fastapi import APIRouter


route = APIRouter(prefix='/auth')


@route.post('/register')
async def route_register():
    #todo: fazer implementação real de registro
    pass


@route.post('/validate_code')
async def route_validate_code():
    #todo: implementar a validação de confirmação de código de login/registro
    pass


@route.post('/login')
async def route_login():
    #todo: fazer implementação real de login
    pass
