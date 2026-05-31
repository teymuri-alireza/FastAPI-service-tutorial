from pydantic import BaseModel

class StatusResponse(BaseModel):
    status: str
    message: str

class UserBaseModel(BaseModel):
    name: str

class UserResponseSchema(UserBaseModel):
    id: int

class UserCreateSchema(UserBaseModel):
    pass

class UserUpdateSchema(UserBaseModel):
    id: int
