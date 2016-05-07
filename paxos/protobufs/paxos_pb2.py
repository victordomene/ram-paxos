# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: paxos.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='paxos.proto',
  package='paxos',
  syntax='proto3',
  serialized_pb=_b('\n\x0bpaxos.proto\x12\x05paxos\"R\n\x0ePrepareRequest\x12\x17\n\x0fproposal_number\x18\x01 \x01(\x04\x12\x15\n\rdecree_number\x18\x02 \x01(\x04\x12\x10\n\x08proposer\x18\x03 \x01(\t\"`\n\rAcceptRequest\x12\x17\n\x0fproposal_number\x18\x01 \x01(\x04\x12\x15\n\rdecree_number\x18\x02 \x01(\x04\x12\r\n\x05value\x18\x03 \x01(\x04\x12\x10\n\x08proposer\x18\x04 \x01(\t\"\x8a\x01\n\x0fPromiseResponse\x12\x10\n\x08promised\x18\x01 \x01(\x08\x12\x14\n\x0chad_previous\x18\x02 \x01(\x08\x12\x17\n\x0fproposal_number\x18\x03 \x01(\x04\x12\x15\n\rdecree_number\x18\x04 \x01(\x04\x12\r\n\x05value\x18\x05 \x01(\x04\x12\x10\n\x08\x61\x63\x63\x65ptor\x18\x06 \x01(\t\"_\n\x0cLearnRequest\x12\x17\n\x0fproposal_number\x18\x01 \x01(\x04\x12\x15\n\rdecree_number\x18\x02 \x01(\x04\x12\r\n\x05value\x18\x03 \x01(\x04\x12\x10\n\x08\x61\x63\x63\x65ptor\x18\x04 \x01(\t\"\x1e\n\nOKResponse\x12\x10\n\x08response\x18\x01 \x01(\x08\x32\xb7\x01\n\x02VM\x12?\n\x0ehandle_prepare\x12\x15.paxos.PrepareRequest\x1a\x16.paxos.PromiseResponse\x12\x38\n\rhandle_accept\x12\x14.paxos.AcceptRequest\x1a\x11.paxos.OKResponse\x12\x36\n\x0chandle_learn\x12\x13.paxos.LearnRequest\x1a\x11.paxos.OKResponseb\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_PREPAREREQUEST = _descriptor.Descriptor(
  name='PrepareRequest',
  full_name='paxos.PrepareRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='proposal_number', full_name='paxos.PrepareRequest.proposal_number', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='decree_number', full_name='paxos.PrepareRequest.decree_number', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='proposer', full_name='paxos.PrepareRequest.proposer', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=22,
  serialized_end=104,
)


_ACCEPTREQUEST = _descriptor.Descriptor(
  name='AcceptRequest',
  full_name='paxos.AcceptRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='proposal_number', full_name='paxos.AcceptRequest.proposal_number', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='decree_number', full_name='paxos.AcceptRequest.decree_number', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='paxos.AcceptRequest.value', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='proposer', full_name='paxos.AcceptRequest.proposer', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=106,
  serialized_end=202,
)


_PROMISERESPONSE = _descriptor.Descriptor(
  name='PromiseResponse',
  full_name='paxos.PromiseResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='promised', full_name='paxos.PromiseResponse.promised', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='had_previous', full_name='paxos.PromiseResponse.had_previous', index=1,
      number=2, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='proposal_number', full_name='paxos.PromiseResponse.proposal_number', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='decree_number', full_name='paxos.PromiseResponse.decree_number', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='paxos.PromiseResponse.value', index=4,
      number=5, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='acceptor', full_name='paxos.PromiseResponse.acceptor', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=205,
  serialized_end=343,
)


_LEARNREQUEST = _descriptor.Descriptor(
  name='LearnRequest',
  full_name='paxos.LearnRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='proposal_number', full_name='paxos.LearnRequest.proposal_number', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='decree_number', full_name='paxos.LearnRequest.decree_number', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='paxos.LearnRequest.value', index=2,
      number=3, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='acceptor', full_name='paxos.LearnRequest.acceptor', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=345,
  serialized_end=440,
)


_OKRESPONSE = _descriptor.Descriptor(
  name='OKResponse',
  full_name='paxos.OKResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='response', full_name='paxos.OKResponse.response', index=0,
      number=1, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=442,
  serialized_end=472,
)

DESCRIPTOR.message_types_by_name['PrepareRequest'] = _PREPAREREQUEST
DESCRIPTOR.message_types_by_name['AcceptRequest'] = _ACCEPTREQUEST
DESCRIPTOR.message_types_by_name['PromiseResponse'] = _PROMISERESPONSE
DESCRIPTOR.message_types_by_name['LearnRequest'] = _LEARNREQUEST
DESCRIPTOR.message_types_by_name['OKResponse'] = _OKRESPONSE

PrepareRequest = _reflection.GeneratedProtocolMessageType('PrepareRequest', (_message.Message,), dict(
  DESCRIPTOR = _PREPAREREQUEST,
  __module__ = 'paxos_pb2'
  # @@protoc_insertion_point(class_scope:paxos.PrepareRequest)
  ))
_sym_db.RegisterMessage(PrepareRequest)

AcceptRequest = _reflection.GeneratedProtocolMessageType('AcceptRequest', (_message.Message,), dict(
  DESCRIPTOR = _ACCEPTREQUEST,
  __module__ = 'paxos_pb2'
  # @@protoc_insertion_point(class_scope:paxos.AcceptRequest)
  ))
_sym_db.RegisterMessage(AcceptRequest)

PromiseResponse = _reflection.GeneratedProtocolMessageType('PromiseResponse', (_message.Message,), dict(
  DESCRIPTOR = _PROMISERESPONSE,
  __module__ = 'paxos_pb2'
  # @@protoc_insertion_point(class_scope:paxos.PromiseResponse)
  ))
_sym_db.RegisterMessage(PromiseResponse)

LearnRequest = _reflection.GeneratedProtocolMessageType('LearnRequest', (_message.Message,), dict(
  DESCRIPTOR = _LEARNREQUEST,
  __module__ = 'paxos_pb2'
  # @@protoc_insertion_point(class_scope:paxos.LearnRequest)
  ))
_sym_db.RegisterMessage(LearnRequest)

OKResponse = _reflection.GeneratedProtocolMessageType('OKResponse', (_message.Message,), dict(
  DESCRIPTOR = _OKRESPONSE,
  __module__ = 'paxos_pb2'
  # @@protoc_insertion_point(class_scope:paxos.OKResponse)
  ))
_sym_db.RegisterMessage(OKResponse)


import abc
import six
from grpc.beta import implementations as beta_implementations
from grpc.beta import interfaces as beta_interfaces
from grpc.framework.common import cardinality
from grpc.framework.interfaces.face import utilities as face_utilities

class BetaVMServicer(object):
  """Defines a VM service, which provides functionality for Proposer, Acceptor
  and Learner.
  """
  def handle_prepare(self, request, context):
    """Acceptors will receive these
    """
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
  def handle_accept(self, request, context):
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)
  def handle_learn(self, request, context):
    """Learners will receive these
    """
    context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)

class BetaVMStub(object):
  """Defines a VM service, which provides functionality for Proposer, Acceptor
  and Learner.
  """
  def handle_prepare(self, request, timeout):
    """Acceptors will receive these
    """
    raise NotImplementedError()
  handle_prepare.future = None
  def handle_accept(self, request, timeout):
    raise NotImplementedError()
  handle_accept.future = None
  def handle_learn(self, request, timeout):
    """Learners will receive these
    """
    raise NotImplementedError()
  handle_learn.future = None

def beta_create_VM_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
  import paxos_pb2
  import paxos_pb2
  import paxos_pb2
  import paxos_pb2
  import paxos_pb2
  import paxos_pb2
  request_deserializers = {
    ('paxos.VM', 'handle_accept'): paxos_pb2.AcceptRequest.FromString,
    ('paxos.VM', 'handle_learn'): paxos_pb2.LearnRequest.FromString,
    ('paxos.VM', 'handle_prepare'): paxos_pb2.PrepareRequest.FromString,
  }
  response_serializers = {
    ('paxos.VM', 'handle_accept'): paxos_pb2.OKResponse.SerializeToString,
    ('paxos.VM', 'handle_learn'): paxos_pb2.OKResponse.SerializeToString,
    ('paxos.VM', 'handle_prepare'): paxos_pb2.PromiseResponse.SerializeToString,
  }
  method_implementations = {
    ('paxos.VM', 'handle_accept'): face_utilities.unary_unary_inline(servicer.handle_accept),
    ('paxos.VM', 'handle_learn'): face_utilities.unary_unary_inline(servicer.handle_learn),
    ('paxos.VM', 'handle_prepare'): face_utilities.unary_unary_inline(servicer.handle_prepare),
  }
  server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
  return beta_implementations.server(method_implementations, options=server_options)

def beta_create_VM_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
  import paxos_pb2
  import paxos_pb2
  import paxos_pb2
  import paxos_pb2
  import paxos_pb2
  import paxos_pb2
  request_serializers = {
    ('paxos.VM', 'handle_accept'): paxos_pb2.AcceptRequest.SerializeToString,
    ('paxos.VM', 'handle_learn'): paxos_pb2.LearnRequest.SerializeToString,
    ('paxos.VM', 'handle_prepare'): paxos_pb2.PrepareRequest.SerializeToString,
  }
  response_deserializers = {
    ('paxos.VM', 'handle_accept'): paxos_pb2.OKResponse.FromString,
    ('paxos.VM', 'handle_learn'): paxos_pb2.OKResponse.FromString,
    ('paxos.VM', 'handle_prepare'): paxos_pb2.PromiseResponse.FromString,
  }
  cardinalities = {
    'handle_accept': cardinality.Cardinality.UNARY_UNARY,
    'handle_learn': cardinality.Cardinality.UNARY_UNARY,
    'handle_prepare': cardinality.Cardinality.UNARY_UNARY,
  }
  stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
  return beta_implementations.dynamic_stub(channel, 'paxos.VM', cardinalities, options=stub_options)
# @@protoc_insertion_point(module_scope)
