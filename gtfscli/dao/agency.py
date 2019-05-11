#!/usr/bin/env python

from typing import Iterable

from sqlalchemy.orm import Session

from gtfscli.dao.entities import AgencyEntity


class AgencyDao():
    session: Session

    def __init__(self, session: Session):
        self.session = session

    def all(self) -> Iterable[AgencyEntity]:
        return self.session.query(AgencyEntity)
