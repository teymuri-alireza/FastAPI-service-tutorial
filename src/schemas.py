from pydantic import BaseModel, field_validator

class StatusResponse(BaseModel):
    status: str
    message: str

class UserBaseModel(BaseModel):
    name: str

    @field_validator("name")
    def validate_name(cls, name: str):
        if not name.isalpha():
            raise ValueError("Name must contain only alphabetic characters.")
        return name

class UserResponseSchema(UserBaseModel):
    id: int

class UserCreateSchema(UserBaseModel):
    pass

class UserUpdateSchema(UserBaseModel):
    id: int
