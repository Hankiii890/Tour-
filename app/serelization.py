from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Session_local, engine
from database import Clients
from pydantic import BaseModel
from sqlalchemy.orm import Session

app = FastAPI()


class UserCreate(BaseModel):
    name: str
    email: str
    phone: str


# Зависимость для получения сессии базы данных
def get_db():
    db = Session_local()
    try:
        yield db
    finally:
        db.close()


@app.post("/register/")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = Clients(name=user.name, email=user.email, phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user