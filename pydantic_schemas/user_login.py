from pydantic import BaseModel # type: ignore

class UserLogin(BaseModel):
    email: str
    password: str