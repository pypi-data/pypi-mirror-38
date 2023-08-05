# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gm/pb/strategy_service.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from gm.pb import common_pb2 as gm_dot_pb_dot_common__pb2
from gm.pb import strategy_pb2 as gm_dot_pb_dot_strategy__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='gm/pb/strategy_service.proto',
  package='strategy.api',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x1cgm/pb/strategy_service.proto\x12\x0cstrategy.api\x1a\x12gm/pb/common.proto\x1a\x14gm/pb/strategy.proto\x1a\x1cgoogle/api/annotations.proto\x1a\x1bgoogle/protobuf/empty.proto\"I\n\x0eSetAccountsReq\x12\x13\n\x0bstrategy_id\x18\x01 \x01(\t\x12\r\n\x05stage\x18\x02 \x01(\x05\x12\x13\n\x0b\x61\x63\x63ount_ids\x18\x03 \x03(\t\"4\n\x0eGetAccountsReq\x12\x13\n\x0bstrategy_id\x18\x01 \x01(\t\x12\r\n\x05stage\x18\x02 \x01(\x05\"%\n\x0eGetAccountsRsp\x12\x13\n\x0b\x61\x63\x63ount_ids\x18\x02 \x03(\t\"/\n\x19GetStrategiesToAccountReq\x12\x12\n\naccount_id\x18\x01 \x01(\t\"J\n\x10GetStrategiesReq\x12 \n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x10.core.api.Filter\x12\x14\n\x0cstrategy_ids\x18\x02 \x03(\t\"K\n\x17GetStrategiesOfStageReq\x12 \n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x10.core.api.Filter\x12\x0e\n\x06stages\x18\x02 \x03(\x05\"(\n\x10\x44\x65lStrategiesReq\x12\x14\n\x0cstrategy_ids\x18\x01 \x03(\t\"M\n\x13GetStartCommandsReq\x12 \n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x10.core.api.Filter\x12\x14\n\x0cstrategy_ids\x18\x02 \x03(\t\"P\n\x16GetStrategyStatusesReq\x12 \n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x10.core.api.Filter\x12\x14\n\x0cstrategy_ids\x18\x02 \x03(\t\"K\n\x12GetStrategyLogsReq\x12 \n\x06\x66ilter\x18\x01 \x01(\x0b\x32\x10.core.api.Filter\x12\x13\n\x0bstrategy_id\x18\x02 \x01(\t2\xa6\r\n\x0fStrategyService\x12X\n\x0b\x41\x64\x64Strategy\x12\x16.strategy.api.Strategy\x1a\x16.strategy.api.Strategy\"\x19\x82\xd3\xe4\x93\x02\x13\"\x0e/v3/strategies:\x01*\x12\x61\n\rGetStrategies\x12\x1e.strategy.api.GetStrategiesReq\x1a\x18.strategy.api.Strategies\"\x16\x82\xd3\xe4\x93\x02\x10\x12\x0e/v3/strategies\x12x\n\x14GetStrategiesOfStage\x12%.strategy.api.GetStrategiesOfStageReq\x1a\x18.strategy.api.Strategies\"\x1f\x82\xd3\xe4\x93\x02\x19\x12\x17/v3/strategies-of-stage\x12\x66\n\x0bSetStrategy\x12\x16.strategy.api.Strategy\x1a\x16.google.protobuf.Empty\"\'\x82\xd3\xe4\x93\x02!\x1a\x1c/v3/strategies/{strategy_id}:\x01*\x12_\n\rDelStrategies\x12\x1e.strategy.api.DelStrategiesReq\x1a\x16.google.protobuf.Empty\"\x16\x82\xd3\xe4\x93\x02\x10*\x0e/v3/strategies\x12u\n\x0bSetAccounts\x12\x1c.strategy.api.SetAccountsReq\x1a\x16.google.protobuf.Empty\"0\x82\xd3\xe4\x93\x02*\x1a%/v3/strategies/{strategy_id}/accounts:\x01*\x12x\n\x0bGetAccounts\x12\x1c.strategy.api.GetAccountsReq\x1a\x1c.strategy.api.GetAccountsRsp\"-\x82\xd3\xe4\x93\x02\'\x12%/v3/strategies/{strategy_id}/accounts\x12\x8b\x01\n\x16GetStrategiesToAccount\x12\'.strategy.api.GetStrategiesToAccountReq\x1a\x18.strategy.api.Strategies\".\x82\xd3\xe4\x93\x02(\x12&/v3/strategies-to-account/{account_id}\x12z\n\x13GetStrategyStatuses\x12$.strategy.api.GetStrategyStatusesReq\x1a\x1e.strategy.api.StrategyStatuses\"\x1d\x82\xd3\xe4\x93\x02\x17\x12\x15/v3/strategy-statuses\x12o\n\x13SetStrategyStatuses\x12\x1e.strategy.api.StrategyStatuses\x1a\x16.google.protobuf.Empty\" \x82\xd3\xe4\x93\x02\x1a\"\x15/v3/strategy-statuses:\x01*\x12v\n\x0cStopStrategy\x12\x19.strategy.api.StopCommand\x1a\x16.google.protobuf.Empty\"3\x82\xd3\xe4\x93\x02-\"(/v3/strategy-commands/{strategy_id}/stop:\x01*\x12q\n\x10GetStartCommands\x12!.strategy.api.GetStartCommandsReq\x1a\x1b.strategy.api.StartCommands\"\x1d\x82\xd3\xe4\x93\x02\x17\x12\x15/v3/strategy-commands\x12u\n\x0fSetStartCommand\x12\x1a.strategy.api.StartCommand\x1a\x16.google.protobuf.Empty\".\x82\xd3\xe4\x93\x02(\x1a#/v3/strategy-commands/{strategy_id}:\x01*\x12W\n\x0f\x41\x64\x64StrategyLogs\x12\x0e.core.api.Logs\x1a\x16.google.protobuf.Empty\"\x1c\x82\xd3\xe4\x93\x02\x16\"\x11/v3/strategy-logs:\x01*\x12l\n\x0fGetStrategyLogs\x12 .strategy.api.GetStrategyLogsReq\x1a\x0e.core.api.Logs\"\'\x82\xd3\xe4\x93\x02!\x12\x1f/v3/strategy-logs/{strategy_id}b\x06proto3')
  ,
  dependencies=[gm_dot_pb_dot_common__pb2.DESCRIPTOR,gm_dot_pb_dot_strategy__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,])




_SETACCOUNTSREQ = _descriptor.Descriptor(
  name='SetAccountsReq',
  full_name='strategy.api.SetAccountsReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='strategy_id', full_name='strategy.api.SetAccountsReq.strategy_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stage', full_name='strategy.api.SetAccountsReq.stage', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account_ids', full_name='strategy.api.SetAccountsReq.account_ids', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=147,
  serialized_end=220,
)


_GETACCOUNTSREQ = _descriptor.Descriptor(
  name='GetAccountsReq',
  full_name='strategy.api.GetAccountsReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='strategy_id', full_name='strategy.api.GetAccountsReq.strategy_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stage', full_name='strategy.api.GetAccountsReq.stage', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=222,
  serialized_end=274,
)


_GETACCOUNTSRSP = _descriptor.Descriptor(
  name='GetAccountsRsp',
  full_name='strategy.api.GetAccountsRsp',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_ids', full_name='strategy.api.GetAccountsRsp.account_ids', index=0,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=276,
  serialized_end=313,
)


_GETSTRATEGIESTOACCOUNTREQ = _descriptor.Descriptor(
  name='GetStrategiesToAccountReq',
  full_name='strategy.api.GetStrategiesToAccountReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='account_id', full_name='strategy.api.GetStrategiesToAccountReq.account_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=315,
  serialized_end=362,
)


_GETSTRATEGIESREQ = _descriptor.Descriptor(
  name='GetStrategiesReq',
  full_name='strategy.api.GetStrategiesReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='strategy.api.GetStrategiesReq.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='strategy_ids', full_name='strategy.api.GetStrategiesReq.strategy_ids', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=364,
  serialized_end=438,
)


_GETSTRATEGIESOFSTAGEREQ = _descriptor.Descriptor(
  name='GetStrategiesOfStageReq',
  full_name='strategy.api.GetStrategiesOfStageReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='strategy.api.GetStrategiesOfStageReq.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='stages', full_name='strategy.api.GetStrategiesOfStageReq.stages', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=440,
  serialized_end=515,
)


_DELSTRATEGIESREQ = _descriptor.Descriptor(
  name='DelStrategiesReq',
  full_name='strategy.api.DelStrategiesReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='strategy_ids', full_name='strategy.api.DelStrategiesReq.strategy_ids', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=517,
  serialized_end=557,
)


_GETSTARTCOMMANDSREQ = _descriptor.Descriptor(
  name='GetStartCommandsReq',
  full_name='strategy.api.GetStartCommandsReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='strategy.api.GetStartCommandsReq.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='strategy_ids', full_name='strategy.api.GetStartCommandsReq.strategy_ids', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=559,
  serialized_end=636,
)


_GETSTRATEGYSTATUSESREQ = _descriptor.Descriptor(
  name='GetStrategyStatusesReq',
  full_name='strategy.api.GetStrategyStatusesReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='strategy.api.GetStrategyStatusesReq.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='strategy_ids', full_name='strategy.api.GetStrategyStatusesReq.strategy_ids', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=638,
  serialized_end=718,
)


_GETSTRATEGYLOGSREQ = _descriptor.Descriptor(
  name='GetStrategyLogsReq',
  full_name='strategy.api.GetStrategyLogsReq',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='filter', full_name='strategy.api.GetStrategyLogsReq.filter', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='strategy_id', full_name='strategy.api.GetStrategyLogsReq.strategy_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=720,
  serialized_end=795,
)

_GETSTRATEGIESREQ.fields_by_name['filter'].message_type = gm_dot_pb_dot_common__pb2._FILTER
_GETSTRATEGIESOFSTAGEREQ.fields_by_name['filter'].message_type = gm_dot_pb_dot_common__pb2._FILTER
_GETSTARTCOMMANDSREQ.fields_by_name['filter'].message_type = gm_dot_pb_dot_common__pb2._FILTER
_GETSTRATEGYSTATUSESREQ.fields_by_name['filter'].message_type = gm_dot_pb_dot_common__pb2._FILTER
_GETSTRATEGYLOGSREQ.fields_by_name['filter'].message_type = gm_dot_pb_dot_common__pb2._FILTER
DESCRIPTOR.message_types_by_name['SetAccountsReq'] = _SETACCOUNTSREQ
DESCRIPTOR.message_types_by_name['GetAccountsReq'] = _GETACCOUNTSREQ
DESCRIPTOR.message_types_by_name['GetAccountsRsp'] = _GETACCOUNTSRSP
DESCRIPTOR.message_types_by_name['GetStrategiesToAccountReq'] = _GETSTRATEGIESTOACCOUNTREQ
DESCRIPTOR.message_types_by_name['GetStrategiesReq'] = _GETSTRATEGIESREQ
DESCRIPTOR.message_types_by_name['GetStrategiesOfStageReq'] = _GETSTRATEGIESOFSTAGEREQ
DESCRIPTOR.message_types_by_name['DelStrategiesReq'] = _DELSTRATEGIESREQ
DESCRIPTOR.message_types_by_name['GetStartCommandsReq'] = _GETSTARTCOMMANDSREQ
DESCRIPTOR.message_types_by_name['GetStrategyStatusesReq'] = _GETSTRATEGYSTATUSESREQ
DESCRIPTOR.message_types_by_name['GetStrategyLogsReq'] = _GETSTRATEGYLOGSREQ
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

SetAccountsReq = _reflection.GeneratedProtocolMessageType('SetAccountsReq', (_message.Message,), dict(
  DESCRIPTOR = _SETACCOUNTSREQ,
  __module__ = 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.SetAccountsReq)
  ))
_sym_db.RegisterMessage(SetAccountsReq)

GetAccountsReq = _reflection.GeneratedProtocolMessageType('GetAccountsReq', (_message.Message,), dict(
  DESCRIPTOR = _GETACCOUNTSREQ,
  __module__ = 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.GetAccountsReq)
  ))
_sym_db.RegisterMessage(GetAccountsReq)

GetAccountsRsp = _reflection.GeneratedProtocolMessageType('GetAccountsRsp', (_message.Message,), dict(
  DESCRIPTOR = _GETACCOUNTSRSP,
  __module__ = 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.GetAccountsRsp)
  ))
_sym_db.RegisterMessage(GetAccountsRsp)

GetStrategiesToAccountReq = _reflection.GeneratedProtocolMessageType('GetStrategiesToAccountReq', (_message.Message,), dict(
  DESCRIPTOR = _GETSTRATEGIESTOACCOUNTREQ,
  __module__ = 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.GetStrategiesToAccountReq)
  ))
_sym_db.RegisterMessage(GetStrategiesToAccountReq)

GetStrategiesReq = _reflection.GeneratedProtocolMessageType('GetStrategiesReq', (_message.Message,), dict(
  DESCRIPTOR = _GETSTRATEGIESREQ,
  __module__ = 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.GetStrategiesReq)
  ))
_sym_db.RegisterMessage(GetStrategiesReq)

GetStrategiesOfStageReq = _reflection.GeneratedProtocolMessageType('GetStrategiesOfStageReq', (_message.Message,), dict(
  DESCRIPTOR = _GETSTRATEGIESOFSTAGEREQ,
  __module__ = 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.GetStrategiesOfStageReq)
  ))
_sym_db.RegisterMessage(GetStrategiesOfStageReq)

DelStrategiesReq = _reflection.GeneratedProtocolMessageType('DelStrategiesReq', (_message.Message,), dict(
  DESCRIPTOR = _DELSTRATEGIESREQ,
  __module__ = 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.DelStrategiesReq)
  ))
_sym_db.RegisterMessage(DelStrategiesReq)

GetStartCommandsReq = _reflection.GeneratedProtocolMessageType('GetStartCommandsReq', (_message.Message,), dict(
  DESCRIPTOR = _GETSTARTCOMMANDSREQ,
  __module__ = 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.GetStartCommandsReq)
  ))
_sym_db.RegisterMessage(GetStartCommandsReq)

GetStrategyStatusesReq = _reflection.GeneratedProtocolMessageType('GetStrategyStatusesReq', (_message.Message,), dict(
  DESCRIPTOR = _GETSTRATEGYSTATUSESREQ,
  __module__ = 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.GetStrategyStatusesReq)
  ))
_sym_db.RegisterMessage(GetStrategyStatusesReq)

GetStrategyLogsReq = _reflection.GeneratedProtocolMessageType('GetStrategyLogsReq', (_message.Message,), dict(
  DESCRIPTOR = _GETSTRATEGYLOGSREQ,
  __module__ = 'gm.pb.strategy_service_pb2'
  # @@protoc_insertion_point(class_scope:strategy.api.GetStrategyLogsReq)
  ))
_sym_db.RegisterMessage(GetStrategyLogsReq)



_STRATEGYSERVICE = _descriptor.ServiceDescriptor(
  name='StrategyService',
  full_name='strategy.api.StrategyService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=798,
  serialized_end=2500,
  methods=[
  _descriptor.MethodDescriptor(
    name='AddStrategy',
    full_name='strategy.api.StrategyService.AddStrategy',
    index=0,
    containing_service=None,
    input_type=gm_dot_pb_dot_strategy__pb2._STRATEGY,
    output_type=gm_dot_pb_dot_strategy__pb2._STRATEGY,
    serialized_options=_b('\202\323\344\223\002\023\"\016/v3/strategies:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='GetStrategies',
    full_name='strategy.api.StrategyService.GetStrategies',
    index=1,
    containing_service=None,
    input_type=_GETSTRATEGIESREQ,
    output_type=gm_dot_pb_dot_strategy__pb2._STRATEGIES,
    serialized_options=_b('\202\323\344\223\002\020\022\016/v3/strategies'),
  ),
  _descriptor.MethodDescriptor(
    name='GetStrategiesOfStage',
    full_name='strategy.api.StrategyService.GetStrategiesOfStage',
    index=2,
    containing_service=None,
    input_type=_GETSTRATEGIESOFSTAGEREQ,
    output_type=gm_dot_pb_dot_strategy__pb2._STRATEGIES,
    serialized_options=_b('\202\323\344\223\002\031\022\027/v3/strategies-of-stage'),
  ),
  _descriptor.MethodDescriptor(
    name='SetStrategy',
    full_name='strategy.api.StrategyService.SetStrategy',
    index=3,
    containing_service=None,
    input_type=gm_dot_pb_dot_strategy__pb2._STRATEGY,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=_b('\202\323\344\223\002!\032\034/v3/strategies/{strategy_id}:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='DelStrategies',
    full_name='strategy.api.StrategyService.DelStrategies',
    index=4,
    containing_service=None,
    input_type=_DELSTRATEGIESREQ,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=_b('\202\323\344\223\002\020*\016/v3/strategies'),
  ),
  _descriptor.MethodDescriptor(
    name='SetAccounts',
    full_name='strategy.api.StrategyService.SetAccounts',
    index=5,
    containing_service=None,
    input_type=_SETACCOUNTSREQ,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=_b('\202\323\344\223\002*\032%/v3/strategies/{strategy_id}/accounts:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='GetAccounts',
    full_name='strategy.api.StrategyService.GetAccounts',
    index=6,
    containing_service=None,
    input_type=_GETACCOUNTSREQ,
    output_type=_GETACCOUNTSRSP,
    serialized_options=_b('\202\323\344\223\002\'\022%/v3/strategies/{strategy_id}/accounts'),
  ),
  _descriptor.MethodDescriptor(
    name='GetStrategiesToAccount',
    full_name='strategy.api.StrategyService.GetStrategiesToAccount',
    index=7,
    containing_service=None,
    input_type=_GETSTRATEGIESTOACCOUNTREQ,
    output_type=gm_dot_pb_dot_strategy__pb2._STRATEGIES,
    serialized_options=_b('\202\323\344\223\002(\022&/v3/strategies-to-account/{account_id}'),
  ),
  _descriptor.MethodDescriptor(
    name='GetStrategyStatuses',
    full_name='strategy.api.StrategyService.GetStrategyStatuses',
    index=8,
    containing_service=None,
    input_type=_GETSTRATEGYSTATUSESREQ,
    output_type=gm_dot_pb_dot_strategy__pb2._STRATEGYSTATUSES,
    serialized_options=_b('\202\323\344\223\002\027\022\025/v3/strategy-statuses'),
  ),
  _descriptor.MethodDescriptor(
    name='SetStrategyStatuses',
    full_name='strategy.api.StrategyService.SetStrategyStatuses',
    index=9,
    containing_service=None,
    input_type=gm_dot_pb_dot_strategy__pb2._STRATEGYSTATUSES,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=_b('\202\323\344\223\002\032\"\025/v3/strategy-statuses:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='StopStrategy',
    full_name='strategy.api.StrategyService.StopStrategy',
    index=10,
    containing_service=None,
    input_type=gm_dot_pb_dot_strategy__pb2._STOPCOMMAND,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=_b('\202\323\344\223\002-\"(/v3/strategy-commands/{strategy_id}/stop:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='GetStartCommands',
    full_name='strategy.api.StrategyService.GetStartCommands',
    index=11,
    containing_service=None,
    input_type=_GETSTARTCOMMANDSREQ,
    output_type=gm_dot_pb_dot_strategy__pb2._STARTCOMMANDS,
    serialized_options=_b('\202\323\344\223\002\027\022\025/v3/strategy-commands'),
  ),
  _descriptor.MethodDescriptor(
    name='SetStartCommand',
    full_name='strategy.api.StrategyService.SetStartCommand',
    index=12,
    containing_service=None,
    input_type=gm_dot_pb_dot_strategy__pb2._STARTCOMMAND,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=_b('\202\323\344\223\002(\032#/v3/strategy-commands/{strategy_id}:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='AddStrategyLogs',
    full_name='strategy.api.StrategyService.AddStrategyLogs',
    index=13,
    containing_service=None,
    input_type=gm_dot_pb_dot_common__pb2._LOGS,
    output_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    serialized_options=_b('\202\323\344\223\002\026\"\021/v3/strategy-logs:\001*'),
  ),
  _descriptor.MethodDescriptor(
    name='GetStrategyLogs',
    full_name='strategy.api.StrategyService.GetStrategyLogs',
    index=14,
    containing_service=None,
    input_type=_GETSTRATEGYLOGSREQ,
    output_type=gm_dot_pb_dot_common__pb2._LOGS,
    serialized_options=_b('\202\323\344\223\002!\022\037/v3/strategy-logs/{strategy_id}'),
  ),
])
_sym_db.RegisterServiceDescriptor(_STRATEGYSERVICE)

DESCRIPTOR.services_by_name['StrategyService'] = _STRATEGYSERVICE

# @@protoc_insertion_point(module_scope)
