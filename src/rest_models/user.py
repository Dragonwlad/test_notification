from pydantic import BaseModel, constr


class RegisterRequest(BaseModel):
    username: constr(min_length=3, max_length=50)
    password: constr(min_length=6, max_length=128)
