import sys
from pathlib import Path


if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from database import Base, DATABASE_PATH, SessionLocal, create_database, engine
from entities.user import User


USERS = [
    {"name": "Ana Souza", "email": "ana.souza@example.com", "password": "123456", "is_active": True},
    {"name": "Bruno Lima", "email": "bruno.lima@example.com", "password": "123456", "is_active": True},
    {"name": "Carla Dias", "email": "carla.dias@example.com", "password": "123456", "is_active": True},
    {"name": "Diego Rocha", "email": "diego.rocha@example.com", "password": "123456", "is_active": True},
    {"name": "Eva Martins", "email": "eva.martins@example.com", "password": "123456", "is_active": False},
    {"name": "Felipe Alves", "email": "felipe.alves@example.com", "password": "123456", "is_active": True},
    {"name": "Gabi Costa", "email": "gabi.costa@example.com", "password": "123456", "is_active": True},
    {"name": "Heitor Nunes", "email": "heitor.nunes@example.com", "password": "123456", "is_active": False},
    {"name": "Iris Lopes", "email": "iris.lopes@example.com", "password": "123456", "is_active": True},
    {"name": "Joao Pereira", "email": "joao.pereira@example.com", "password": "123456", "is_active": True},
]


def run_seed() -> None:
    create_database()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    for item in USERS:
        db.add(User(**item))
    db.commit()
    db.close()


if __name__ == "__main__":
    run_seed()
    print(f"SQLite criado com {len(USERS)} usuarios em: {DATABASE_PATH}")
