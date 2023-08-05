# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: gm/pb/common.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from github.com.gogo.protobuf.gogoproto import gogo_pb2 as github_dot_com_dot_gogo_dot_protobuf_dot_gogoproto_dot_gogo__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='gm/pb/common.proto',
  package='core.api',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x12gm/pb/common.proto\x12\x08\x63ore.api\x1a\x1fgoogle/protobuf/timestamp.proto\x1a-github.com/gogo/protobuf/gogoproto/gogo.proto\"R\n\x08Property\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x0b\n\x03val\x18\x02 \x01(\t\x12\x0c\n\x04name\x18\x03 \x01(\t\x12\r\n\x05index\x18\x04 \x01(\x05\x12\x0f\n\x07visible\x18\x05 \x01(\x08\"\x87\x01\n\x06\x46ilter\x12\x0e\n\x06\x66ields\x18\x01 \x01(\t\x12\x0e\n\x06\x66ilter\x18\x02 \x01(\t\x12\x0c\n\x04sort\x18\x03 \x01(\t\x12\r\n\x05limit\x18\x04 \x01(\x05\x12\x0c\n\x04page\x18\x05 \x01(\x05\x12\x10\n\x08pagesize\x18\x06 \x01(\x05\x12\x10\n\x08\x66romdate\x18\x07 \x01(\t\x12\x0e\n\x06todate\x18\x08 \x01(\t\"1\n\x05\x45rror\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0c\n\x04type\x18\x02 \x01(\t\x12\x0c\n\x04info\x18\x03 \x01(\t\"\x8d\x01\n\x11\x43onnectionAddress\x12\r\n\x05title\x18\x01 \x01(\t\x12\x39\n\x07\x61\x64\x64ress\x18\x02 \x03(\x0b\x32(.core.api.ConnectionAddress.AddressEntry\x1a.\n\x0c\x41\x64\x64ressEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\xdf\x01\n\x10\x43onnectionStatus\x12\r\n\x05state\x18\x01 \x01(\x05\x12\x1e\n\x05\x65rror\x18\x02 \x01(\x0b\x32\x0f.core.api.Error\"\x9b\x01\n\x05State\x12\x11\n\rState_UNKNOWN\x10\x00\x12\x14\n\x10State_CONNECTING\x10\x01\x12\x13\n\x0fState_CONNECTED\x10\x02\x12\x12\n\x0eState_LOGGEDIN\x10\x03\x12\x17\n\x13State_DISCONNECTING\x10\x04\x12\x16\n\x12State_DISCONNECTED\x10\x05\x12\x0f\n\x0bState_ERROR\x10\x06\"\x8b\x01\n\x03Log\x12\x0e\n\x06source\x18\x01 \x01(\t\x12\r\n\x05level\x18\x02 \x01(\t\x12\x0b\n\x03msg\x18\x03 \x01(\t\x12\x10\n\x08owner_id\x18\x04 \x01(\t\x12\x46\n\ncreated_at\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x16\x90\xdf\x1f\x01\xf2\xde\x1f\x0exorm:\"created\"\"#\n\x04Logs\x12\x1b\n\x04\x64\x61ta\x18\x01 \x03(\x0b\x32\r.core.api.Log\"A\n\tHeartbeat\x12\x34\n\ncreated_at\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x04\x90\xdf\x1f\x01\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,github_dot_com_dot_gogo_dot_protobuf_dot_gogoproto_dot_gogo__pb2.DESCRIPTOR,])



_CONNECTIONSTATUS_STATE = _descriptor.EnumDescriptor(
  name='State',
  full_name='core.api.ConnectionStatus.State',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='State_UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='State_CONNECTING', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='State_CONNECTED', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='State_LOGGEDIN', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='State_DISCONNECTING', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='State_DISCONNECTED', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='State_ERROR', index=6, number=6,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=598,
  serialized_end=753,
)
_sym_db.RegisterEnumDescriptor(_CONNECTIONSTATUS_STATE)


_PROPERTY = _descriptor.Descriptor(
  name='Property',
  full_name='core.api.Property',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='core.api.Property.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='val', full_name='core.api.Property.val', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='core.api.Property.name', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='index', full_name='core.api.Property.index', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='visible', full_name='core.api.Property.visible', index=4,
      number=5, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
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
  serialized_start=112,
  serialized_end=194,
)


_FILTER = _descriptor.Descriptor(
  name='Filter',
  full_name='core.api.Filter',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='fields', full_name='core.api.Filter.fields', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='filter', full_name='core.api.Filter.filter', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='sort', full_name='core.api.Filter.sort', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='limit', full_name='core.api.Filter.limit', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='page', full_name='core.api.Filter.page', index=4,
      number=5, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pagesize', full_name='core.api.Filter.pagesize', index=5,
      number=6, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='fromdate', full_name='core.api.Filter.fromdate', index=6,
      number=7, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='todate', full_name='core.api.Filter.todate', index=7,
      number=8, type=9, cpp_type=9, label=1,
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
  serialized_start=197,
  serialized_end=332,
)


_ERROR = _descriptor.Descriptor(
  name='Error',
  full_name='core.api.Error',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='code', full_name='core.api.Error.code', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='core.api.Error.type', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='info', full_name='core.api.Error.info', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  serialized_start=334,
  serialized_end=383,
)


_CONNECTIONADDRESS_ADDRESSENTRY = _descriptor.Descriptor(
  name='AddressEntry',
  full_name='core.api.ConnectionAddress.AddressEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='core.api.ConnectionAddress.AddressEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='core.api.ConnectionAddress.AddressEntry.value', index=1,
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
  serialized_options=_b('8\001'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=481,
  serialized_end=527,
)

_CONNECTIONADDRESS = _descriptor.Descriptor(
  name='ConnectionAddress',
  full_name='core.api.ConnectionAddress',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='title', full_name='core.api.ConnectionAddress.title', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='address', full_name='core.api.ConnectionAddress.address', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_CONNECTIONADDRESS_ADDRESSENTRY, ],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=386,
  serialized_end=527,
)


_CONNECTIONSTATUS = _descriptor.Descriptor(
  name='ConnectionStatus',
  full_name='core.api.ConnectionStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='state', full_name='core.api.ConnectionStatus.state', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='error', full_name='core.api.ConnectionStatus.error', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CONNECTIONSTATUS_STATE,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=530,
  serialized_end=753,
)


_LOG = _descriptor.Descriptor(
  name='Log',
  full_name='core.api.Log',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='source', full_name='core.api.Log.source', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='level', full_name='core.api.Log.level', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='msg', full_name='core.api.Log.msg', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='owner_id', full_name='core.api.Log.owner_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='created_at', full_name='core.api.Log.created_at', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\220\337\037\001\362\336\037\016xorm:\"created\"'), file=DESCRIPTOR),
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
  serialized_start=756,
  serialized_end=895,
)


_LOGS = _descriptor.Descriptor(
  name='Logs',
  full_name='core.api.Logs',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='data', full_name='core.api.Logs.data', index=0,
      number=1, type=11, cpp_type=10, label=3,
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
  serialized_start=897,
  serialized_end=932,
)


_HEARTBEAT = _descriptor.Descriptor(
  name='Heartbeat',
  full_name='core.api.Heartbeat',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='created_at', full_name='core.api.Heartbeat.created_at', index=0,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\220\337\037\001'), file=DESCRIPTOR),
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
  serialized_start=934,
  serialized_end=999,
)

_CONNECTIONADDRESS_ADDRESSENTRY.containing_type = _CONNECTIONADDRESS
_CONNECTIONADDRESS.fields_by_name['address'].message_type = _CONNECTIONADDRESS_ADDRESSENTRY
_CONNECTIONSTATUS.fields_by_name['error'].message_type = _ERROR
_CONNECTIONSTATUS_STATE.containing_type = _CONNECTIONSTATUS
_LOG.fields_by_name['created_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_LOGS.fields_by_name['data'].message_type = _LOG
_HEARTBEAT.fields_by_name['created_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['Property'] = _PROPERTY
DESCRIPTOR.message_types_by_name['Filter'] = _FILTER
DESCRIPTOR.message_types_by_name['Error'] = _ERROR
DESCRIPTOR.message_types_by_name['ConnectionAddress'] = _CONNECTIONADDRESS
DESCRIPTOR.message_types_by_name['ConnectionStatus'] = _CONNECTIONSTATUS
DESCRIPTOR.message_types_by_name['Log'] = _LOG
DESCRIPTOR.message_types_by_name['Logs'] = _LOGS
DESCRIPTOR.message_types_by_name['Heartbeat'] = _HEARTBEAT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Property = _reflection.GeneratedProtocolMessageType('Property', (_message.Message,), dict(
  DESCRIPTOR = _PROPERTY,
  __module__ = 'gm.pb.common_pb2'
  # @@protoc_insertion_point(class_scope:core.api.Property)
  ))
_sym_db.RegisterMessage(Property)

Filter = _reflection.GeneratedProtocolMessageType('Filter', (_message.Message,), dict(
  DESCRIPTOR = _FILTER,
  __module__ = 'gm.pb.common_pb2'
  # @@protoc_insertion_point(class_scope:core.api.Filter)
  ))
_sym_db.RegisterMessage(Filter)

Error = _reflection.GeneratedProtocolMessageType('Error', (_message.Message,), dict(
  DESCRIPTOR = _ERROR,
  __module__ = 'gm.pb.common_pb2'
  # @@protoc_insertion_point(class_scope:core.api.Error)
  ))
_sym_db.RegisterMessage(Error)

ConnectionAddress = _reflection.GeneratedProtocolMessageType('ConnectionAddress', (_message.Message,), dict(

  AddressEntry = _reflection.GeneratedProtocolMessageType('AddressEntry', (_message.Message,), dict(
    DESCRIPTOR = _CONNECTIONADDRESS_ADDRESSENTRY,
    __module__ = 'gm.pb.common_pb2'
    # @@protoc_insertion_point(class_scope:core.api.ConnectionAddress.AddressEntry)
    ))
  ,
  DESCRIPTOR = _CONNECTIONADDRESS,
  __module__ = 'gm.pb.common_pb2'
  # @@protoc_insertion_point(class_scope:core.api.ConnectionAddress)
  ))
_sym_db.RegisterMessage(ConnectionAddress)
_sym_db.RegisterMessage(ConnectionAddress.AddressEntry)

ConnectionStatus = _reflection.GeneratedProtocolMessageType('ConnectionStatus', (_message.Message,), dict(
  DESCRIPTOR = _CONNECTIONSTATUS,
  __module__ = 'gm.pb.common_pb2'
  # @@protoc_insertion_point(class_scope:core.api.ConnectionStatus)
  ))
_sym_db.RegisterMessage(ConnectionStatus)

Log = _reflection.GeneratedProtocolMessageType('Log', (_message.Message,), dict(
  DESCRIPTOR = _LOG,
  __module__ = 'gm.pb.common_pb2'
  # @@protoc_insertion_point(class_scope:core.api.Log)
  ))
_sym_db.RegisterMessage(Log)

Logs = _reflection.GeneratedProtocolMessageType('Logs', (_message.Message,), dict(
  DESCRIPTOR = _LOGS,
  __module__ = 'gm.pb.common_pb2'
  # @@protoc_insertion_point(class_scope:core.api.Logs)
  ))
_sym_db.RegisterMessage(Logs)

Heartbeat = _reflection.GeneratedProtocolMessageType('Heartbeat', (_message.Message,), dict(
  DESCRIPTOR = _HEARTBEAT,
  __module__ = 'gm.pb.common_pb2'
  # @@protoc_insertion_point(class_scope:core.api.Heartbeat)
  ))
_sym_db.RegisterMessage(Heartbeat)


_CONNECTIONADDRESS_ADDRESSENTRY._options = None
_LOG.fields_by_name['created_at']._options = None
_HEARTBEAT.fields_by_name['created_at']._options = None
# @@protoc_insertion_point(module_scope)
