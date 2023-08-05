from typing import Any, Text, List, Tuple, Union
from grpc import ServicerContext, Server, Channel
from grpc._channel import _Rendezvous

from gm.pb.fundamental_pb2 import (
    GetFundamentalsReq, GetFundamentalsRsp, GetInstrumentInfosReq,
    GetInstrumentsReq, GetConstituentsReq, GetSectorReq, GetSectorRsp, GetIndustryReq, GetIndustryRsp, GetConceptReq,
    GetConceptRsp, GetTradingDatesReq, GetTradingDatesRsp, GetPreviousTradingDateReq, GetPreviousTradingDateRsp,
    GetNextTradingDateRsp, GetNextTradingDateReq, GetDividendsReq, GetDividendsSnapshotReq, GetHistoryInstrumentsReq,
    GetContinuousContractsReq, GetFundamentalsNReq)
from gm.pb.data_pb2 import InstrumentInfos, Instruments, Constituents, Dividends, ContinuousContracts


# 调用时加上 with_call 则会返回 GetFundamentalsRsp, _Rendezvous 这样的元组
class FundamentalServiceStub:
    def __init__(self, channel:Channel):...
    def GetFundamentals(self, request: GetFundamentalsReq, timeout=None, metadata=None, credentials=None, with_call=False) -> Union[GetFundamentalsRsp, Tuple[GetFundamentalsRsp, _Rendezvous]] : ...
    def GetFundamentalsN(self, request: GetFundamentalsNReq, timeout=None, metadata=None, credentials=None, with_call=False) -> Union[GetFundamentalsRsp, Tuple[GetFundamentalsRsp, _Rendezvous]] : ...
    def GetInstrumentInfos(self, request: GetInstrumentInfosReq, timeout=None, metadata=None, credentials=None, with_call=False) -> Union[InstrumentInfos, Tuple[InstrumentInfos, _Rendezvous]]: ...
    def GetInstruments(self, request:GetInstrumentsReq, timeout=None, metadata=None, credentials=None, with_call=False) -> Union[Instruments, Tuple[Instruments, _Rendezvous]]: ...
    def GetHistoryInstruments(self, request:GetHistoryInstrumentsReq, timeout=None, metadata=None, credentials=None, with_call=False)-> Union[Instruments, Tuple[Instruments, _Rendezvous]]: ...
    def GetConstituents(self, request:GetConstituentsReq, timeout=None, metadata=None, credentials=None, with_call=False) -> Union[Constituents, Tuple[Constituents, _Rendezvous]]: ...
    def GetSector(self, request:GetSectorReq, timeout=None, metadata=None, credentials=None, with_call=False) -> Union[GetSectorRsp, Tuple[GetSectorRsp, _Rendezvous]]:...
    def GetIndustry(self, request:GetIndustryReq, timeout=None, metadata=None, credentials=None, with_call=False) -> Union[GetIndustryRsp, Tuple[GetIndustryRsp, _Rendezvous]]:...
    def GetConcept(self, request:GetConceptReq, timeout=None, metadata=None, credentials=None, with_call=False) -> Union[GetConceptRsp, Tuple[GetConceptRsp, _Rendezvous]]:...
    def GetTradingDates(self, request:GetTradingDatesReq, timeout=None, metadata=None, credentials=None, with_call=False) -> Union[GetTradingDatesRsp, Tuple[GetTradingDatesRsp, _Rendezvous]]:...
    def GetPreviousTradingDate(self, request:GetPreviousTradingDateReq, timeout=None, metadata=None, credentials=None, with_call=False) -> Union[GetPreviousTradingDateRsp, Tuple[GetPreviousTradingDateRsp, _Rendezvous]]:...
    def GetNextTradingDate(self, request:GetNextTradingDateReq, timeout=None, metadata=None, credentials=None, with_call=False) -> Union[GetNextTradingDateRsp, Tuple[GetNextTradingDateRsp, _Rendezvous]]:...
    def GetDividends(self, request:GetDividendsReq, timeout=None, metadata=None, credentials=None, with_call=False) -> Union[Dividends, Tuple[Dividends, _Rendezvous]]:...
    def GetDividendsSnapshot(self, request:GetDividendsSnapshotReq, timeout=None, metadata=None, credentials=None, with_call=False) -> Union[Dividends, Tuple[Dividends, _Rendezvous]]:...
    def GetContinuousContracts(self, request:GetContinuousContractsReq, timeout=None, metadata=None, credentials=None, with_call=False) -> Union[ContinuousContracts, Tuple[ContinuousContracts, _Rendezvous]]:...


class FundamentalServiceServicer:
    def GetFundamentals(self, request:GetFundamentalsReq, context:ServicerContext) -> GetFundamentalsRsp:...
    def GetFundamentalsN(self, request:GetFundamentalsNReq, context:ServicerContext) -> GetFundamentalsRsp:...
    def GetInstrumentInfos(self, request:GetInstrumentInfosReq, context:ServicerContext) -> InstrumentInfos:...
    def GetInstruments(self, request:GetInstrumentsReq, context:ServicerContext) -> Instruments: ...
    def GetHistoryInstruments(self, request:GetHistoryInstrumentsReq, context:ServicerContext) -> Instruments: ...
    def GetConstituents(self, request:GetConstituentsReq, context:ServicerContext) -> Constituents: ...
    def GetSector(self, request:GetSectorReq, context:ServicerContext) -> GetSectorRsp:...
    def GetIndustry(self, request:GetIndustryReq, context:ServicerContext) -> GetIndustryRsp:...
    def GetConcept(self, request:GetConceptReq, context:ServicerContext) -> GetConceptRsp:...
    def GetTradingDates(self, request:GetTradingDatesReq, context:ServicerContext) -> GetTradingDatesRsp:...
    def GetPreviousTradingDate(self, request:GetPreviousTradingDateReq, context:ServicerContext) -> GetPreviousTradingDateRsp:...
    def GetNextTradingDate(self, request:GetNextTradingDateReq, context:ServicerContext) -> GetNextTradingDateRsp:...
    def GetDividends(self, request:GetDividendsReq, context:ServicerContext) -> Dividends:...
    def GetDividendsSnapshot(self, request:GetDividendsSnapshotReq, context:ServicerContext) -> Dividends:...
    def GetContinuousContracts(self, request:GetContinuousContractsReq, context:ServicerContext) -> ContinuousContracts:...


def add_FundamentalServiceServicer_to_server(servicer:FundamentalServiceServicer, server:Server):...
