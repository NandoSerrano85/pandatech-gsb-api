import os
from google.protobuf.json_format import MessageToDict
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy_protobuf import ProtobufMixin
from sqlalchemy_protobuf.sqlalchemy_protobuf import ProtobufSerializer
from datetime import datetime
from database.db import Base

# Import the generated protobuf classes
from pythonProtos.user_pb2 import (User, RegisterRequest, RegisterResponse, AuthResponse)
from pythonProtos.images_pb2 import (Image, MissingImage)

# Helper function to convert proto fields to SQLAlchemy columns
def proto_to_sqlalchemy_column(proto_field):
    if proto_field.type == proto_field.TYPE_INT32:
        return Column(Integer)
    elif proto_field.type == proto_field.TYPE_INT64:
        return Column(Integer)
    elif proto_field.type == proto_field.TYPE_STRING:
        return Column(String)
    else:
        raise ValueError(f"Unsupported proto field type: {proto_field.type}")

# Generate SQLAlchemy models from proto definitions
def generate_model(proto_message, base_class):
    class_name = proto_message.DESCRIPTOR.name
    class_dict = {
        '__tablename__': class_name.lower() + 's',
        '__protobuf_meta__': ProtobufSerializer(proto_message)
    }

    for field in proto_message.DESCRIPTOR.fields:
        if field.name == 'id':
            class_dict[field.name] = Column(Integer, primary_key=True)
        elif field.name.endswith('_id'):
            referenced_table = field.name[:-3] + 's'
            class_dict[field.name] = Column(Integer, ForeignKey(f'{referenced_table}.id'))
        elif field.name == 'created_at':
            class_dict[field.name] = Column(DateTime, default=datetime.utcnow)
        else:
            class_dict[field.name] = proto_to_sqlalchemy_column(field)

    return type(class_name, (base_class, ProtobufMixin), class_dict)

# Generate models
def UserModel():
    return generate_model(User, Base)
def RegisterRequest():
    return generate_model(RegisterRequest, Base)
def RegisterResponse():
    return generate_model(RegisterResponse, Base)
def AuthResponse():
    return generate_model(AuthResponse, Base)
def ImageModel():
    return generate_model(Image, Base)
def MissingImageModel():
    return generate_model(MissingImage, Base)

# Add relationships
# User.images = relationship("Image", back_populates="user")
# Image.user = relationship("User", back_populates="images")

