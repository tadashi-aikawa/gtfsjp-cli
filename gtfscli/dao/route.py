#!/usr/bin/env python

from typing import Iterable, Optional

from sqlalchemy.orm import Session

from gtfscli.dao.entities import RouteEntity


class RouteDao():
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def all(self) -> Iterable[RouteEntity]:
        return self.session.query(RouteEntity)

    def find_by_id(self, id_: str) -> Optional[RouteEntity]:
        return self.session.query(RouteEntity).get(id_)
