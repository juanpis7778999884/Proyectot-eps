from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.crud.crud_base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return db.execute(stmt).scalars().first()

    def get_by_role(self, db: Session, *, role: str, skip: int = 0, limit: int = 100) -> List[User]:
        stmt = select(User).where(User.role == role).offset(skip).limit(limit)
        return list(db.execute(stmt).scalars().all())

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        data = obj_in.model_dump()
        password = data.pop("password", None)
        db_obj = User(**data)
        if password is not None:
            db_obj.hashed_password = get_password_hash(password)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


user = CRUDUser(User)
