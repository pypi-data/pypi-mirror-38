# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorboard/plugins/audio/plugin_data.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='tensorboard/plugins/audio/plugin_data.proto',
  package='tensorboard',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n+tensorboard/plugins/audio/plugin_data.proto\x12\x0btensorboard\"}\n\x0f\x41udioPluginData\x12\x0f\n\x07version\x18\x01 \x01(\x05\x12\x37\n\x08\x65ncoding\x18\x02 \x01(\x0e\x32%.tensorboard.AudioPluginData.Encoding\" \n\x08\x45ncoding\x12\x0b\n\x07UNKNOWN\x10\x00\x12\x07\n\x03WAV\x10\x0b\x62\x06proto3')
)



_AUDIOPLUGINDATA_ENCODING = _descriptor.EnumDescriptor(
  name='Encoding',
  full_name='tensorboard.AudioPluginData.Encoding',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNKNOWN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WAV', index=1, number=11,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=153,
  serialized_end=185,
)
_sym_db.RegisterEnumDescriptor(_AUDIOPLUGINDATA_ENCODING)


_AUDIOPLUGINDATA = _descriptor.Descriptor(
  name='AudioPluginData',
  full_name='tensorboard.AudioPluginData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='tensorboard.AudioPluginData.version', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='encoding', full_name='tensorboard.AudioPluginData.encoding', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _AUDIOPLUGINDATA_ENCODING,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=60,
  serialized_end=185,
)

_AUDIOPLUGINDATA.fields_by_name['encoding'].enum_type = _AUDIOPLUGINDATA_ENCODING
_AUDIOPLUGINDATA_ENCODING.containing_type = _AUDIOPLUGINDATA
DESCRIPTOR.message_types_by_name['AudioPluginData'] = _AUDIOPLUGINDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

AudioPluginData = _reflection.GeneratedProtocolMessageType('AudioPluginData', (_message.Message,), dict(
  DESCRIPTOR = _AUDIOPLUGINDATA,
  __module__ = 'tensorboard.plugins.audio.plugin_data_pb2'
  # @@protoc_insertion_point(class_scope:tensorboard.AudioPluginData)
  ))
_sym_db.RegisterMessage(AudioPluginData)


# @@protoc_insertion_point(module_scope)
