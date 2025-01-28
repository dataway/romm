from typing import Any, Sequence

from decorators.database import begin_session
from models.collection import Collection, VirtualCollection
from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql import ColumnExpressionArgument
from utils.database import json_array_contains_value

from .base_handler import DBBaseHandler


class DBCollectionsHandler(DBBaseHandler):
    @begin_session
    def add_collection(
        self, collection: Collection, session: Session = None
    ) -> Collection:
        collection = session.merge(collection)
        session.flush()

        return session.query(Collection).filter_by(id=collection.id).one()

    @begin_session
    def get_collection(self, id: int, session: Session = None) -> Collection | None:
        return session.scalar(select(Collection).filter_by(id=id).limit(1))

    @begin_session
    def get_virtual_collection(
        self, id: str, session: Session = None
    ) -> VirtualCollection | None:
        name, type = VirtualCollection.from_id(id)
        return session.scalar(
            select(VirtualCollection).filter_by(name=name, type=type).limit(1)
        )

    @begin_session
    def get_collection_by_name(
        self, name: str, user_id: int, session: Session = None
    ) -> Collection | None:
        return session.scalar(
            select(Collection).filter_by(name=name, user_id=user_id).limit(1)
        )

    @begin_session
    def get_collections(self, session: Session = None) -> Sequence[Collection]:
        return (
            session.scalars(select(Collection).order_by(Collection.name.asc()))
            .unique()
            .all()
        )

    @begin_session
    def get_virtual_collections(
        self, session: Session = None
    ) -> Sequence[VirtualCollection]:
        return (
            session.scalars(
                select(VirtualCollection)
                .filter_by(type="collection")
                .order_by(VirtualCollection.name.asc())
            )
            .unique()
            .all()
        )

    @begin_session
    def get_collections_by_rom_id(
        self,
        rom_id: int,
        *,
        order_by: Sequence[str | ColumnExpressionArgument[Any]] | None = None,
        session: Session = None,
    ) -> Sequence[Collection]:
        query = select(Collection).filter(
            json_array_contains_value(Collection.roms, rom_id, session=session)
        )
        if order_by is not None:
            query = query.order_by(*order_by)

        return session.scalars(query).all()

    @begin_session
    def get_virtual_collections_by_rom_id(
        self,
        rom_id: int,
        *,
        order_by: Sequence[str | ColumnExpressionArgument[Any]] | None = None,
        session: Session = None,
    ) -> Sequence[VirtualCollection]:
        query = select(VirtualCollection).filter(
            json_array_contains_value(VirtualCollection.roms, rom_id, session=session)
        )
        if order_by is not None:
            query = query.order_by(*order_by)

        return session.scalars(query).all()

    @begin_session
    def update_collection(
        self, id: int, data: dict, session: Session = None
    ) -> Collection:
        session.execute(
            update(Collection)
            .where(Collection.id == id)
            .values(**data)
            .execution_options(synchronize_session="evaluate")
        )
        return session.query(Collection).filter_by(id=id).one()

    @begin_session
    def delete_collection(self, id: int, session: Session = None) -> None:
        session.execute(
            delete(Collection)
            .where(Collection.id == id)
            .execution_options(synchronize_session="evaluate")
        )
