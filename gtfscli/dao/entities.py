#!/usr/bin/env python
"""Refer to https://www.gtfs.jp/developpers-guide/format-reference.html
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class StopEntity(Base):
    """停留所・標柱
    """
    __tablename__ = 'stops'

    stop_id: str = Column(String, primary_key=True)    # ID
    stop_code: str = Column(String)    # 番号
    stop_name: str = Column(String, nullable=False)    # 名称
    stop_desc: str = Column(String)    # 追加情報
    stop_lat: str = Column(String, nullable=False)    #緯度
    stop_lon: str = Column(String, nullable=False)    #経度
    zone_id: str = Column(String)    # 運賃エリアID (標柱のみ)
    stop_url: str = Column(String)    # 特化情報のURL
    location_type: int = Column(Integer)    # 標柱(0) or 停留所(1)
    parent_station: str = Column(String)    # 親駅情報 (標柱のみ)
    # GTFS-JPでは不要だが、存在することはある
    stop_timezone: str = Column(String)
    # GTFS-JPでは不要だが、存在することはある
    wheelchair_boarding: int = Column(Integer)
    platform_code: str = Column(String)    # のりば情報(ID) (標柱のみ)

    stop_times = relationship("StopTimeEntity", backref="stops")


class StopTimeEntity(Base):
    """通過時刻情報
    """
    __tablename__ = 'stop_times'

    trip_id: str = Column(String, nullable=False, primary_key=True)    # 便ID
    arrival_time: str = Column(String, nullable=False)    # 到着時刻 (HH:MM:SS)
    departure_time: str = Column(String, nullable=False)    # 出発時刻 (HH:MM:SS)
    stop_id: str = Column(String, ForeignKey("stops.stop_id"), nullable=False)    # 標柱ID
    stop_sequence: int = Column(Integer, nullable=False, primary_key=True)    # 通過順位
    stop_headsign: str = Column(String)    # 停留所行先
    pickup_type: int = Column(Integer)    # 乗車区分 (0: 通常, 1: 乗車不可, 2: 要電話予約, 3:要運転手連絡)
    drop_off_type: int = Column(Integer)    # 降車区分(0:通常, 1:降車不可, 2:要電話予約, 3:要運転手連絡)
    shape_dist_traveled: int = Column(Integer)    # 通算距離(m)
    timepoint: int = Column(Integer)    # 発着時刻制度

    stop = relationship("StopEntity")
