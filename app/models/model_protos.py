import inspect
from sqlalchemy import Column, Integer, String, Float, Boolean
from database.db import Base
from google.protobuf.descriptor import FieldDescriptor

from protos.generated.user_pb2 import (User, RegisterRequest, RegisterResponse, AuthResponse)
from protos.generated.images_pb2 import (Image, MissingImage)

# Protobuf to SQLAlchemy type mapping
TYPE_MAP = {
    FieldDescriptor.TYPE_DOUBLE: Float,
    FieldDescriptor.TYPE_FLOAT: Float,
    FieldDescriptor.TYPE_INT64: Integer,
    FieldDescriptor.TYPE_UINT64: Integer,
    FieldDescriptor.TYPE_INT32: Integer,
    FieldDescriptor.TYPE_FIXED64: Integer,
    FieldDescriptor.TYPE_FIXED32: Integer,
    FieldDescriptor.TYPE_BOOL: Boolean,
    FieldDescriptor.TYPE_STRING: String,
    FieldDescriptor.TYPE_BYTES: String,
    FieldDescriptor.TYPE_UINT32: Integer,
    FieldDescriptor.TYPE_SFIXED32: Integer,
    FieldDescriptor.TYPE_SFIXED64: Integer,
    FieldDescriptor.TYPE_SINT32: Integer,
    FieldDescriptor.TYPE_SINT64: Integer,
}

def get_protobuf_messages(module):
    messages = []
    for name, obj in inspect.getmembers(module):
        if inspect.isclass(obj) and hasattr(obj, 'DESCRIPTOR') and hasattr(obj.DESCRIPTOR, 'fields'):
            messages.append(obj)
    return messages

def generate_sqlalchemy_model(proto_class):
    fields = []
    descriptor = proto_class.DESCRIPTOR
    
    for field in descriptor.fields:
        field_type = TYPE_MAP.get(field.type, String)  # Default to String if type not mapped
        column = Column(field.name.lower(), field_type)
        fields.append(column)
    
    model_class_name = descriptor.name
    attrs = {'__tablename__': model_class_name.lower(), '__table_args__': {'extend_existing': True}}
    for field in fields:
        attrs[field.name] = field
    
    model_class = type(model_class_name, (Base,), attrs)
    return model_class

# Generate models
def UserModel():
    proto_class = get_protobuf_messages(User)
    return generate_sqlalchemy_model(proto_class)

def RegisterRequest():
    proto_class = get_protobuf_messages(RegisterRequest)
    return generate_sqlalchemy_model(proto_class)

def RegisterResponse():
    proto_class = get_protobuf_messages(RegisterResponse)
    return generate_sqlalchemy_model(proto_class)

def AuthResponse():
    proto_class = get_protobuf_messages(AuthResponse)
    return generate_sqlalchemy_model(proto_class)

def ImageModel():
    proto_class = get_protobuf_messages(Image)
    return generate_sqlalchemy_model(proto_class)

def MissingImageModel():
    proto_class = get_protobuf_messages(MissingImage)
    return generate_sqlalchemy_model(proto_class)

