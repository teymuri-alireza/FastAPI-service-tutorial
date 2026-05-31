from pydantic import BaseModel

class StatusResponse(BaseModel):
    status: str
    message: str

class UserResponseSchema(BaseModel):
    id: int
    name: str

class UserCreateSchema(BaseModel):
    name: str

class UserUpdateSchema(BaseModel):
    id: int
    name: str
