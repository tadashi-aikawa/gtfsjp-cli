#!/usr/bin/env python
"""Refer to https://www.gtfs.jp/developpers-guide/format-reference.html
"""

from typing import Iterable

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class AgencyEntity(Base):
    """事業者情報
    """
    __tablename__ = 'agency'

    agency_id: str = Column(String, primary_key=True)
    """事業者ID (ex: 8000020130001)"""
    agency_name: str = Column(String, nullable=False)
    """事業者名称 (ex: 都営バス)"""
    agency_url: str = Column(String, nullable=False)
    """事業者URL - 原則トップページ"""
    agency_timezone: str = Column(String, nullable=False)
    """タイムゾーン - 日本の場合は『Asia/Tokyo』固定"""
    agency_lang: str = Column(String)
    """言語 - 日本の場合は『ja』固定)"""
    agency_phone: str = Column(String)
    """電話番号 (ex: 03-2816:5700)"""
    agency_fare_url: str = Column(String)
    """オンライン購入URL - 乗車券をオンライン購入するサイトのURL"""
    agency_email: str = Column(String)
    """事業者Eメール"""

    extra: 'AgencyJpEntity' = relationship("AgencyJpEntity", uselist=False, back_populates="origins")
    """紐づく事業者追加情報"""


class AgencyJpEntity(Base):
    """事業者追加情報
    """
    __tablename__ = 'agency_jp'

    # XXX: primary keyではないけどORMはprimary keyナシを認めないので追加. 後で定義が変わる可能性は高い
    agency_id: str = Column(String, ForeignKey("agency.agency_id"), primary_key=True)
    """事業者ID (ex: 8000020130001)"""
    agency_official_name: str = Column(String)
    """事業者正式名称 (ex: 東京都交通局)"""
    agency_zip_number: str = Column(String)
    """事業者郵便番号 (ex: 1638001)"""
    agency_address: str = Column(String)
    """事業者住所 (ex: 東京都新宿区西新宿二丁目８番１号)"""
    agency_president_pos: str = Column(String)
    """代表者肩書き (ex: 局長)"""
    agency_president_name: str = Column(String)
    """代表者氏名 (ex: 東京　太郎)"""

    origins: Iterable[AgencyEntity] = relationship("AgencyEntity", uselist=True, back_populates="extra")
    """紐づく事業者情報"""


class StopEntity(Base):
    """停留所/標柱
    """
    __tablename__ = 'stops'

    stop_id: str = Column(String, primary_key=True)
    """停留所・標柱ID (ex: [停]100 [柱]100_10)"""
    stop_code: str = Column(String)
    """停留所・標柱番号 - ナンバリングなどの番号"""
    stop_name: str = Column(String, nullable=False)
    """停留所・標柱名称 (ex: [停]東京駅八重洲口 [柱]東京駅八重洲口)"""
    stop_desc: str = Column(String)
    """停留所・標柱付加情報 (最寄り施設情報など)"""
    stop_lat: str = Column(String, nullable=False)
    """緯度 - Degree/世界測地系 (ex: [停]ターミナル中心 [柱]標柱位置)"""
    stop_lon: str = Column(String, nullable=False)
    """経度 - Degree/世界測地系 (ex: [停]ターミナル中心 [柱]標柱位置)"""
    zone_id: str = Column(String)    # 運賃エリアID (標柱のみ)
    """運賃エリアID - 対キロ制の場合は標柱IDを設定? (ex: [停]なし [柱]Z_210)"""
    stop_url: str = Column(String)
    """停留所・標柱URL - 時刻表やバスロケの案内先"""
    location_type: int = Column(Integer)
    """停留所・標柱区分 - 0:標柱 1:停留所"""
    parent_station: str = Column(String)    # 親駅情報 (標柱のみ)
    """親駅情報 - 標柱の場合に停留所のstop_idを指定できる (ex: [停]なし [柱]100)"""
    stop_timezone: str = Column(String)
    """タイムゾーン - 日本では設定不要"""
    wheelchair_boarding: int = Column(Integer)
    """車イス情報 - 設定非推奨"""
    platform_code: str = Column(String)    # のりば情報(ID) (標柱のみ)
    """のりば情報 - 『番』『のりば』などの語句は含めない (ex: [停]なし [柱]G,3,センタービル前)"""

    stop_times: Iterable['StopTimeEntity'] = relationship("StopTimeEntity", uselist=True, back_populates="stop")
    """紐づく通過時刻情報"""


class StopTimeEntity(Base):
    """通過時刻情報
    """
    __tablename__ = 'stop_times'

    trip_id: str = Column(String, primary_key=True)
    """便ID (ex: 1001WD001)"""
    arrival_time: str = Column(String, nullable=False)
    """到着時刻 - HH:MM:SS形式 24時以降は 25:01:00のように表記 (ex: 7:00:00)"""
    departure_time: str = Column(String, nullable=False)
    """出発時刻 - HH:MM:SS形式 24時以降は 25:01:00のように表記 (ex: 7:00:00)"""
    stop_id: str = Column(String, ForeignKey("stops.stop_id"), nullable=False)
    """標柱ID - stops.location_type=0のstopであること (ex: 100_10)"""
    stop_sequence: int = Column(Integer, primary_key=True)
    """通過順位 - 通過順序.. 昇順になっていれば連番である必要はない (ex: 0)"""
    stop_headsign: str = Column(String)
    """停留所行先 - 停留所により案内の行き先が変わる場合に必要 (ex: 東京ビッグサイト (月島駅経由))"""
    pickup_type: int = Column(Integer)
    """乗車区分 - 0: 通常, 1: 乗車不可, 2: 要電話予約, 3:要運転手連絡 (ex: 0)"""
    drop_off_type: int = Column(Integer)
    """降車区分 - 0:通常, 1:降車不可, 2:要電話予約, 3:要運転手連絡 (ex: 0)"""
    shape_dist_traveled: int = Column(Integer)
    """通算距離 - 単位はm"""
    timepoint: int = Column(Integer)
    """発着時間精度 - 日本では使用しない"""

    stop: StopEntity = relationship("StopEntity", uselist=False, back_populates="stop_times")
    """紐づく停留所/標柱情報"""


class CalendarEntity(Base):
    """運行区分情報
    """
    __tablename__ = 'calendar'

    service_id: str = Column(String, primary_key=True)
    """運行ID - ??? (ex: 平日（月～金）)"""
    monday: int = Column(Integer, nullable=False)
    """月曜日 - 運行: 1 非運行: 0"""
    tuesday: int = Column(Integer, nullable=False)
    """火曜日 - 運行: 1 非運行: 0"""
    wednesday: int = Column(Integer, nullable=False)
    """水曜日 - 運行: 1 非運行: 0"""
    thursday: int = Column(Integer, nullable=False)
    """木曜日 - 運行: 1 非運行: 0"""
    friday: int = Column(Integer, nullable=False)
    """金曜日 - 運行: 1 非運行: 0"""
    saturday: int = Column(Integer, nullable=False)
    """土曜日 - 運行: 1 非運行: 0"""
    sunday: int = Column(Integer, nullable=False)
    """日曜日 - 運行: 1 非運行: 0"""
    start_date: str = Column(String, nullable=False)
    """サービス開始日 - YYYYMMDD形式 (ex: 20170101)"""
    end_date: str = Column(String, nullable=False)
    """サービス終了日 - YYYYMMDD形式 (ex: 20171231)"""

    dates: 'Iterable[CalendarDatesEntity]' = relationship(
        "CalendarDatesEntity", uselist=True, back_populates="calendar"
    )
    """紐づく運行日情報"""


class CalendarDatesEntity(Base):
    """運行日情報
    """
    __tablename__ = 'calendar_dates'

    service_id: str = Column(String, primary_key=True)
    """運行ID - ??? (ex: 平日（月～金）)"""
    date: str = Column(String, primary_key=True)
    """日付 - YYYYMMDD形式 (ex: 20170503)"""
    exception_type: int = Column(Integer, nullable=False)
    """利用タイプ - 運行: 1 非運行: 2"""

    calendar: CalendarEntity = relationship("CalendarEntity", uselist=False, back_populates="dates")
    """紐づく運行情報"""
