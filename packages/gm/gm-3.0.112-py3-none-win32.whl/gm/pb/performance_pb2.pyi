from typing import Text, Dict
from google.protobuf.timestamp_pb2 import Timestamp
from google.protobuf.duration_pb2 import Duration
from google.protobuf.message import Message
from google.protobuf.internal.containers import RepeatedScalarFieldContainer, RepeatedCompositeFieldContainer

from gm.pb.account_pb2 import Position


# noinspection PyAbstractClass
class Indicator(Message):
    account_id = ...  # type: Text
    pnl_ratio = ...  # type: float
    pnl_ratio_annual = ...  # type: float
    sharp_ratio = ...  # type: float
    max_drawdown = ...  # type: float
    risk_ratio = ...  # type: float
    open_count = ...  # type: int
    close_count = ...  # type: int
    win_count = ...  # type: int
    lose_count = ...  # type: int
    win_ratio = ...  # type: float
    calmar_ratio = ...  # type: float
    created_at = ...  # type: Timestamp
    updated_at = ...  # type: Timestamp

    def __init__(self,
                 account_id: Text = '',
                 pnl_ratio: float = None,
                 pnl_ratio_annual: float = None,
                 sharp_ratio: float = None,
                 max_drawdown: float = None,
                 risk_ratio: float = None,
                 open_count: int = None,
                 close_count: int = None,
                 win_count: int = None,
                 lose_count: int = None,
                 win_ratio: float = None,
                 calmar_ratio: float = None,
                 created_at: Timestamp = None,
                 updated_at: Timestamp = None
                 ): ...


# noinspection PyAbstractClass
class Indicators(Message):
    data = ...  # type: RepeatedCompositeFieldContainer[Indicator]

    def __init__(self, data: RepeatedCompositeFieldContainer[Indicator] = None): ...


# noinspection PyAbstractClass
class IndicatorDuration(Message):
    account_id = ...  # type: Text
    pnl_ratio = ...  # type: float
    pnl = ...  # type: float
    fpnl = ...  # type: float
    frozen = ...  # type: float
    cash = ...  # type: float
    nav = ...  # type: float
    positions = ...  # type: RepeatedCompositeFieldContainer[Position]
    cum_pnl = ...  # type: float
    cum_buy = ...  # type: float
    cum_sell = ...  # type: float
    cum_commission = ...  # type: float
    duration = ...  # type: Duration
    created_at = ...  # type: Timestamp
    updated_at = ...  # type: Timestamp

    def __init__(self,
                 account_id: Text = None,
                 pnl_ratio: float = None,
                 pnl: float = None,
                 fpnl: float = None,
                 frozen: float = None,
                 cash: float = None,
                 nav: float = None,
                 positions: RepeatedCompositeFieldContainer[Position] = None,
                 cum_pnl: float = None,
                 cum_buy: float = None,
                 cum_sell: float = None,
                 cum_commission: float = None,
                 duration: Duration = None,
                 created_at: Timestamp = None,
                 updated_at: Timestamp = None
                 ): ...


# noinspection PyAbstractClass
class IndicatorDurations(Message):
    data = ...  # type: RepeatedCompositeFieldContainer[IndicatorDuration]

    def __init__(self, data: RepeatedCompositeFieldContainer[IndicatorDuration] = None): ...
