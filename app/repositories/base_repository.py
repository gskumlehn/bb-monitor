from typing import TypeVar, Generic, Type, List, Optional, Any
from app.infra.database import db

T = TypeVar('T', bound=db.Model)

class BaseRepository(Generic[T]):
    model: Type[T]

    @classmethod
    def save(cls, instance: T) -> None:
        db.session.add(instance)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id: Any) -> Optional[T]:
        return db.session.get(cls.model, id)

    @classmethod
    def delete(cls, instance: T) -> None:
        db.session.delete(instance)
        db.session.commit()