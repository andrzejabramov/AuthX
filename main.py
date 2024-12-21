from fastapi import FastAPI, HTTPException, Response
from authx import AuthX, AuthXConfig
from fastapi.params import Depends
from pydantic import BaseModel

app = FastAPI()

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

class UserLoginSchema(BaseModel):
    username: str
    password: str


@app.post("/login")
async def login(credentials: UserLoginSchema, responce: Response):
    if credentials.username == "test" and credentials.password == "test":
        token = security.create_access_token(uid="12345")
        responce.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Неверные логин или пароль")

@app.get("/protected", dependencies=[Depends(security.access_token_required)])
async def protected():
    return {"data": "TOP SECRET"}

