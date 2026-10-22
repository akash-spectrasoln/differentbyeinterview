


from fastapi import FastAPI
from pydantic import BaseModel
from .models import get_db
import re

app = FastAPI()

class user(BaseModel):
    username: str
    email: str
    password: str

@app.post("/user")
async def create_user(user: user):
    user.email = re.sub(r'[^@]+@[^@]+\.[^@]+', user.email, user.email)
    db = next(get_db())
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created successfully", "user": user}
@app.get("/user/{user_id}")
async def get_user(user_id: int):
    db = next(get_db())
    user = db.query(user).filter(user.id == user_id).first()
    if user is None:
        return {"message": "User not found"}
    return {"user": user}