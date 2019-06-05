#!/usr/bin/env python

from typing import Iterable, Optional

from sqlalchemy.orm import Session

from gtfsjpcli.dao.entities import StopEntity


class StopDao():
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def all(self) -> Iterable[StopEntity]:
        return self.session.query(StopEntity)

    def find_by_id(self, id_: str) -> Optional[StopEntity]:
        return self.session.query(StopEntity).get(id_)

    def search_by_name(self, name: str) -> Iterable[StopEntity]:
        return self.session.query(StopEntity).filter(StopEntity.stop_name.like(f"%{name}%"))
