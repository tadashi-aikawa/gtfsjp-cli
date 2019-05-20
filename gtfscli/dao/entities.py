#!/usr/bin/env python
"""参考 https://www.gtfs.jp/developpers-guide/format-reference.html

必要性の低いものは一旦定義していません。

* 運行間隔情報 (frequencies.txt)
* 乗換情報 (transfers.txt)

"""

from typing import Iterable, Optional

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

BASE = declarative_base()


class AgencyEntity(BASE):
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
    agency_lang: Optional[str] = Column(String)
    """言語 - 日本の場合は『ja』固定)"""
    agency_phone: Optional[str] = Column(String)
    """電話番号 (ex: 03-2816:5700)"""
    agency_fare_url: Optional[str] = Column(String)
    """オンライン購入URL - 乗車券をオンライン購入するサイトのURL"""
    agency_email: Optional[str] = Column(String)
    """事業者Eメール"""

    jp: Optional['AgencyJpEntity'] = relationship("AgencyJpEntity", uselist=False, back_populates="origin")
    """日本特有の追加情報"""
    routes: Iterable["RouteEntity"] = relationship("RouteEntity", uselist=True, back_populates="agency")
    """紐づく事業者追加情報"""


class AgencyJpEntity(BASE):
    """事業者追加情報
    """
    __tablename__ = 'agency_jp'

    # XXX: primary keyではないけどORMはprimary keyナシを認めないので追加. 後で定義が変わる可能性は高い
    agency_id: str = Column(String, ForeignKey("agency.agency_id"), primary_key=True)
    """事業者ID (ex: 8000020130001)"""
    agency_official_name: Optional[str] = Column(String)
    """事業者正式名称 (ex: 東京都交通局)"""
    agency_zip_number: Optional[str] = Column(String)
    """事業者郵便番号 (ex: 1638001)"""
    agency_address: Optional[str] = Column(String)
    """事業者住所 (ex: 東京都新宿区西新宿二丁目８番１号)"""
    agency_president_pos: Optional[str] = Column(String)
    """代表者肩書き (ex: 局長)"""
    agency_president_name: Optional[str] = Column(String)
    """代表者氏名 (ex: 東京　太郎)"""

    origin: Iterable[AgencyEntity] = relationship("AgencyEntity", uselist=False, back_populates="jp")
    """事業者情報"""


class StopEntity(BASE):
    """停留所/標柱
    """
    __tablename__ = 'stops'

    stop_id: str = Column(String, primary_key=True)
    """停留所・標柱ID (ex: [停]100 [柱]100_10)"""
    stop_code: Optional[str] = Column(String)
    """停留所・標柱番号 - ナンバリングなどの番号"""
    stop_name: str = Column(String, nullable=False)
    """停留所・標柱名称 (ex: [停]東京駅八重洲口 [柱]東京駅八重洲口)"""
    stop_desc: Optional[str] = Column(String)
    """停留所・標柱付加情報 (最寄り施設情報など)"""
    stop_lat: str = Column(String, nullable=False)
    """緯度 - Degree/世界測地系 (ex: [停]ターミナル中心 [柱]標柱位置)"""
    stop_lon: str = Column(String, nullable=False)
    """経度 - Degree/世界測地系 (ex: [停]ターミナル中心 [柱]標柱位置)"""
    zone_id: Optional[str] = Column(String)    # 運賃エリアID (標柱のみ)
    """運賃エリアID - 対キロ制の場合は標柱IDを設定? (ex: [停]なし [柱]Z_210)"""
    stop_url: Optional[str] = Column(String)
    """停留所・標柱URL - 時刻表やバスロケの案内先"""
    location_type: Optional[int] = Column(Integer)
    """停留所・標柱区分 - 0:標柱 1:停留所"""
    parent_station: Optional[str] = Column(String)    # 親駅情報 (標柱のみ)
    """親駅情報 - 標柱の場合に停留所のstop_idを指定できる (ex: [停]なし [柱]100)"""
    stop_timezone: Optional[str] = Column(String)
    """タイムゾーン - 日本では設定不要"""
    wheelchair_boarding: Optional[int] = Column(Integer)
    """車イス情報 - 設定非推奨"""
    platform_code: Optional[str] = Column(String)    # のりば情報(ID) (標柱のみ)
    """のりば情報 - 『番』『のりば』などの語句は含めない (ex: [停]なし [柱]G,3,センタービル前)"""

    stop_times: Iterable['StopTimeEntity'] = relationship("StopTimeEntity", uselist=True, back_populates="stop")
    """紐づく通過時刻情報"""


class RouteEntity(BASE):
    """経路情報
    """
    __tablename__ = 'routes'

    route_id: str = Column(String, primary_key=True)
    """経路ID (ex: 1001)"""
    agency_id: str = Column(String, ForeignKey("agency.agency_id"), nullable=False)
    """事業者ID (ex: 8000020130001)"""
    route_short_name: Optional[str] = Column(String)
    """経路略称 - route_long_nameが無い場合は必須 (ex: 東16)"""
    route_long_name: Optional[str] = Column(String)
    """経路名 - route_short_nameが無い場合は必須 (ex: 東京駅八重洲口～月島駅前～東京ビ ッグサイト)"""
    route_desc: Optional[str] = Column(String)
    """経路情報 - trip_descを使えない場合のみ使うことを推奨"""
    route_type: int = Column(Integer, nullable=False)
    """経路タイプ - バス事業者は『3』に固定"""
    route_url: Optional[str] = Column(String)
    """経路URL - 経路情報の案内サイトURLなど"""
    route_color: Optional[str] = Column(String)
    """経路色 - 線やラベルに使用する色 (ex: FFD700)"""
    route_text_color: Optional[str] = Column(String)
    """経路文字色 - 線やラベル上の文字に使用する色 (ex: 000000)"""
    jp_parent_route_id: Optional[str] = Column(String)
    """路線ID - 複数経路を束ねるために路線と紐付ける"""

    agency: AgencyEntity = relationship("AgencyEntity", uselist=False, back_populates="routes")
    """事業者"""
    jp: Optional['RouteJpEntity'] = relationship("RouteJpEntity", uselist=False, back_populates="origin")
    """日本特有の経路追加情報"""
    trips: Iterable['TripEntity'] = relationship("TripEntity", uselist=True, back_populates="route")
    """便一覧"""
    fare_rules: Iterable['FareRuleEntity'] = relationship("FareRuleEntity", uselist=True, back_populates="route")
    """運賃定義情報一覧"""


class RouteJpEntity(BASE):
    """経路追加情報
    主キーなしだがSQL Alchemyの動作仕様を満たす為 primary_key=True を全フィールドに付けています
    """
    __tablename__ = 'routes_jp'

    route_id: str = Column(String, ForeignKey("routes.route_id"), primary_key=True)
    """経路ID (ex: 1000)"""
    route_update_date: Optional[str] = Column(String, primary_key=True, nullable=True)
    """ダイヤ改正日 (ex: 20170106)"""
    origin_stop: Optional[str] = Column(String, primary_key=True, nullable=True)
    """起点 (ex: 東京都八重洲口)"""
    via_stop: Optional[str] = Column(String, primary_key=True, nullable=True)
    """経過地 (ex: 月島駅)"""
    destination_stop: Optional[str] = Column(String, primary_key=True, nullable=True)
    """終点 (ex: 東京ビッグサイト)"""

    origin: Iterable[RouteEntity] = relationship("RouteEntity", uselist=False, back_populates="jp")
    """経路情報"""


class TripEntity(BASE):
    """便情報
    """
    __tablename__ = 'trips'

    route_id: str = Column(String, ForeignKey('routes.route_id'), nullable=False)
    """経路ID (ex: 1000)"""
    service_id: str = Column(String, ForeignKey('calendar.service_id'), nullable=False)
    """運行ID - ??? (ex: 平日（月～金）)"""
    trip_id: str = Column(String, primary_key=True)
    """便ID (ex: 1001WD001)"""
    trip_headsign: Optional[str] = Column(String)
    """便行先 (ex: 東京ビッグサイト（月島駅経由）)"""
    trip_short_name: Optional[str] = Column(String)
    """便名称 (ex: 荻エクスプレス1号)"""
    direction_id: Optional[int] = Column(Integer)
    """上下区分 - 0:復路 1:往路"""
    block_id: Optional[str] = Column(String)
    """便結合区分 - 連続乗車が可能なものに使用?"""
    shape_id: Optional[str] = Column(String)
    """描画ID (ex: S_1001)"""
    wheelchair_accessible: Optional[int] = Column(Integer)
    """車いす利用区分 - 0:情報なし 1:乗車可能性あり 2:乗車不可"""
    bikes_allowed: Optional[int] = Column(Integer)
    """自転車持込区分 - 0:情報なし 1:乗車可能性あり 2:乗車不可"""
    jp_trip_desc: Optional[str] = Column(String)
    """便情報 - 特殊な運行など便の補足説明"""
    jp_trip_desc_symbol: Optional[str] = Column(String)
    """便記号 - 時刻に付ける凡例"""
    jp_office_id: Optional[str] = Column(String, ForeignKey("office_jp.office_id"))
    """営業所ID (ex: S)"""

    route: RouteEntity = relationship("RouteEntity", uselist=True, back_populates="trips")
    """便の紐づく経路"""
    office: Optional['OfficeJpEntity'] = relationship("OfficeJpEntity", uselist=False, back_populates="trips")
    """便に紐づく営業所"""
    stop_times: Iterable['StopTimeEntity'] = relationship("StopTimeEntity", uselist=True, back_populates="trip")
    """便に紐づく停車時刻情報"""
    shapes: Iterable['ShapeEntity'] = relationship("ShapeEntity", uselist=True, back_populates="trip")
    """便に紐づく描画情報"""
    calendar: 'CalendarEntity' = relationship("CalendarEntity", uselist=False, back_populates="trips")
    """便に紐づく運行区分情報"""


class OfficeJpEntity(BASE):
    """営業所
    """
    __tablename__ = 'office_jp'

    office_id: str = Column(String, primary_key=True)
    """営業所ID (ex: S)"""
    office_name: str = Column(String, nullable=False)
    """営業所名 (ex: 深川営業所)"""
    office_url: Optional[str] = Column(String)
    """営業所URL - 営業所情報の記載されたサイトURLなど"""
    office_phone: Optional[str] = Column(String)
    """営業所電話番号 (ex: 03-3529-3322)"""

    trips: Iterable[TripEntity] = relationship("TripEntity", uselist=True, back_populates="office")
    """営業所に紐づく便一覧"""


class StopTimeEntity(BASE):
    """通過時刻情報
    """
    __tablename__ = 'stop_times'

    trip_id: str = Column(String, ForeignKey("trips.trip_id"), primary_key=True)
    """便ID (ex: 1001WD001)"""
    arrival_time: str = Column(String, nullable=False)
    """到着時刻 - HH:MM:SS形式 24時以降は 25:01:00のように表記 (ex: 7:00:00)"""
    departure_time: str = Column(String, nullable=False)
    """出発時刻 - HH:MM:SS形式 24時以降は 25:01:00のように表記 (ex: 7:00:00)"""
    stop_id: str = Column(String, ForeignKey("stops.stop_id"), nullable=False)
    """標柱ID - stops.location_type=0のstopであること (ex: 100_10)"""
    stop_sequence: int = Column(Integer, primary_key=True)
    """通過順位 - 通過順序.. 昇順になっていれば連番である必要はない (ex: 0)"""
    stop_headsign: Optional[str] = Column(String)
    """停留所行先 - 停留所により案内の行き先が変わる場合に必要 (ex: 東京ビッグサイト (月島駅経由))"""
    pickup_type: Optional[int] = Column(Integer)
    """乗車区分 - 0: 通常, 1: 乗車不可, 2: 要電話予約, 3:要運転手連絡 (ex: 0)"""
    drop_off_type: Optional[int] = Column(Integer)
    """降車区分 - 0:通常, 1:降車不可, 2:要電話予約, 3:要運転手連絡 (ex: 0)"""
    shape_dist_traveled: Optional[int] = Column(Integer)
    """通算距離 - 単位はm"""
    timepoint: Optional[int] = Column(Integer)
    """発着時間精度 - 日本では使用しない"""

    trip: TripEntity = relationship("TripEntity", uselist=False, back_populates="stop_times")
    """紐づく便情報"""
    stop: StopEntity = relationship("StopEntity", uselist=False, back_populates="stop_times")
    """紐づく停留所/標柱情報"""


class CalendarEntity(BASE):
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

    dates: 'Iterable[CalendarDateEntity]' = relationship("CalendarDateEntity", uselist=True, back_populates="calendar")
    """紐づく運行日情報一覧"""
    trips: 'Iterable[TripEntity]' = relationship("TripEntity", uselist=True, back_populates="calendar")
    """紐づく便一覧"""


class CalendarDateEntity(BASE):
    """運行日情報
    """
    __tablename__ = 'calendar_dates'

    service_id: str = Column(String, ForeignKey('calendar.service_id'), primary_key=True)
    """運行ID - ??? (ex: 平日（月～金）)"""
    date: str = Column(String, primary_key=True)
    """日付 - YYYYMMDD形式 (ex: 20170503)"""
    exception_type: int = Column(Integer, nullable=False)
    """利用タイプ - 運行: 1 非運行: 2"""

    calendar: CalendarEntity = relationship("CalendarEntity", uselist=False, back_populates="dates")
    """紐づく運行情報"""


class FareAttributeEntity(BASE):
    """運賃属性情報
    """
    __tablename__ = 'fare_attributes'

    fare_id: str = Column(String, primary_key=True)
    """運賃ID (ex: F_210)"""
    price: int = Column(Integer, nullable=False)
    """運賃 (ex: 210)"""
    currency_type: str = Column(String, primary_key=True)
    """通貨 - 日本では『JPY』で固定"""
    payment_method: int = Column(Integer, nullable=False)
    """支払いタイミング - 0:乗車後に支払う 1:乗車前に支払う"""
    transfers: str = Column(String, nullable=False)
    """乗換 - 0:料金で乗換不可 1:1度乗換可 2:2度乗換可 空白:乗換回数制限なし"""
    transfer_duration: Optional[int] = Column(Integer)
    """乗換有効期限 - 未指定と空白は等価"""

    fare_rules: Iterable['FareRuleEntity'] = relationship(
        "FareRuleEntity", uselist=True, back_populates="fare_attribute"
    )
    """紐づく運賃定義情報一覧。currency_typeがJPY固定であるため擬似的にone to manyとみなすことができる"""


class FareRuleEntity(BASE):
    """運賃定義情報
    """
    __tablename__ = 'fare_rules'

    fare_id: str = Column(String, ForeignKey("fare_attributes.fare_id"), primary_key=True)
    """運賃ID (ex: F_210)"""
    route_id: Optional[str] = Column(String, ForeignKey("routes.route_id"), primary_key=True, nullable=True)
    """経路ID (ex: 1001)"""
    origin_id: Optional[str] = Column(String, ForeignKey("stops.stop_id"), primary_key=True, nullable=True)
    """乗車地ゾーン (ex: Z_210)"""
    destination_id: Optional[str] = Column(String, ForeignKey("stops.stop_id"), primary_key=True, nullable=True)
    """降車地ゾーン (ex: Z_210)"""
    contains_id: Optional[str] = Column(String)
    """通過ゾーン - 使用していないので不要"""

    route: RouteEntity = relationship("RouteEntity", uselist=False, back_populates="fare_rules")
    """紐づく系統"""
    fare_attribute: FareAttributeEntity = relationship(
        "FareAttributeEntity", uselist=False, back_populates="fare_rules"
    )
    """紐づく運賃属性情報。fare_attributes.currency_typeがJPY固定であるため擬似的にmany to oneとみなすことができる"""
    origin_stop: StopEntity = relationship("StopEntity", primaryjoin="FareRuleEntity.origin_id==StopEntity.stop_id")
    """乗車地の停留所/標柱"""
    destination_stop: StopEntity = relationship(
        "StopEntity", primaryjoin="FareRuleEntity.destination_id==StopEntity.stop_id"
    )
    """降車地の停留所/標柱"""


class ShapeEntity(BASE):
    """描画情報
    """
    __tablename__ = 'shapes'

    shape_id: str = Column(String, ForeignKey("trips.shape_id"), primary_key=True)
    """描画ID (ex: S_1001)"""
    shape_pt_lat: str = Column(String, nullable=False)
    """描画緯度 - 度/世界測地系? (ex: 35.679752)"""
    shape_pt_lon: str = Column(String, nullable=False)
    """描画経度 - 度/世界測地系? (ex: 139.76833)"""
    shape_pt_sequence: int = Column(Integer, primary_key=True)
    """描画順序 (ex: 0)"""
    shape_dist_traveled: Optional[int] = Column(Integer)
    """描画距離 - 使用しない"""

    trip: TripEntity = relationship("TripEntity", uselist=False, back_populates="shapes")
    """紐づく便"""


class FeedInfoEntity(BASE):
    """提供情報
    主キーなしだがSQL Alchemyの動作仕様を満たす為 primary_key=True を全フィールドに付けています
    """
    __tablename__ = 'feed_info'

    feed_publisher_name: str = Column(String, primary_key=True)
    """提供組織名 (ex: 東京都交通局)"""
    feed_publisher_url: str = Column(String, primary_key=True)
    """提供組織URL"""
    feed_lang: str = Column(String, primary_key=True)
    """提供言語 - 日本の場合は『ja』"""
    feed_start_date: Optional[str] = Column(String, primary_key=True, nullable=True)
    """有効期間開始日 - YYYYMMDD形式"""
    feed_end_date: Optional[str] = Column(String, primary_key=True, nullable=True)
    """有効期間終了日 - YYYYMMDD形式"""
    feed_version: Optional[str] = Column(String, primary_key=True, nullable=True)
    """提供データバージョン (ex: 20170401A0015)"""


class TranslationEntity(BASE):
    """翻訳情報
    """
    __tablename__ = 'translations'

    trans_id: str = Column(String, primary_key=True)
    """翻訳元日本語 - name/desc/headsign/urlで終わるフィールドが対象 (ex: 数寄屋橋)"""
    lang: str = Column(String, primary_key=True)
    """言語 - 読み仮名である『ja-Hrkt』は必須 (ex: en)"""
    translation: str = Column(String, nullable=False)
    """翻訳先言語 (ex: すきやばし)"""
