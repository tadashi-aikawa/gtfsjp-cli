#!/usr/bin/env python

from typing import Iterable

from sqlalchemy.orm import Session

from gtfscli.dao.entities import TripEntity


class TripDao():
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def all(self) -> Iterable[TripEntity]:
        return self.session.query(TripEntity)

    def head(self, size: int, offset: int = 0) -> Iterable[TripEntity]:
        return self.session.query(TripEntity).offset(offset).limit(size)
