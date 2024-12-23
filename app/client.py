from sqlalchemy.orm import Session
from database import Clients


# Создание клиента
def create_client(db: Session, name: str, email: str, phone: str):
    db_client = Clients(name=name, email=email, phone=phone)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client


# Получение всех клиентов
def get_clients(db: Session):
    return db.query(Clients).all()


# Получение клиента по ID
def get_client(db: Session, client_id: int):
    return db.query(Clients).filter(Clients.id == client_id).first()


# Обновление клиента
def update_client(db: Session, client_id: int, name: str, email: str, phone: str):
    client = db.query(Clients).filter(Clients.id == client_id).first()
    if client:
        client.name = name
        client.email = email
        client.phone = phone
        db.commit()
        db.refresh(client)
    return client


# Удаление клиента
def delete_client(db: Session, client_id: int):
    client = db.query(Clients).filter(Clients.id == client_id).first()
    if client:
        db.delete(client)
        db.commit()
    return client