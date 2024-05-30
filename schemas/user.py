from pydantic import BaseModel, constr, EmailStr


class UserRegisterSchema(BaseModel):
    username: constr(max_length=50)
    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
