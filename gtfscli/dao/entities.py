#!/usr/bin/env python
"""Refer to https://www.gtfs.jp/developpers-guide/format-reference.html
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class AgencyEntity(Base):
    """事業者情報
    """
    __tablename__ = 'agency'

    agency_id: str = Column(String, primary_key=True)    # ID
    agency_name: str = Column(String, nullable=False)    # 名称
    agency_url: str = Column(String, nullable=False)    # URL
    agency_timezone: str = Column(String, nullable=False)    # タイムゾーン(Asia/Tokyo固定)
    agency_lang: str = Column(String)    # 言語(ja固定)
    agency_phone: str = Column(String)    # 電話番号 (xx-xxxx-xxxx)
    agency_fare_url: str = Column(String)    # オンライン購入URL
    agency_email: str = Column(String)    # 事業者Eメール

    extra: 'AgencyJpEntity' = relationship("AgencyJpEntity", uselist=False)


class AgencyJpEntity(Base):
    """事業者追加情報
    """
    __tablename__ = 'agency_jp'

    # XXX: primary keyではないけどORMはprimary keyナシを認めないので追加. 後で定義が変わる可能性は高い
    agency_id: str = Column(String, ForeignKey("agency.agency_id"), primary_key=True)    # ID
    agency_official_name: str = Column(String)    # 正式名称
    agency_zip_number: str = Column(String)    # 郵便番号(xxxyyyy)
    agency_address: str = Column(String)    # 住所(All全角)
    agency_president_pos: str = Column(String)    # 代表者肩書き
    agency_president_name: str = Column(String)    # 代表者氏名


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
