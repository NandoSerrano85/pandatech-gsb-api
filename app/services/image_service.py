# image_service.py
import uuid, os, grpc
from pythonProtos.images_pb2 import (
    Image,
    ListImagesResponse,
)
from pythonProtos.images_pb2_grpc import ImageServiceServicer

from app.core.constants import (
    DIR_LIST,
)
from app.core.util import (
    allowed_file,
)
from app.models.images import (
    ImageModel,
)
from database.db import get_db


class ImageServicer(ImageServiceServicer):
    def UploadImage(self, request, context):
        file_data = request.file_data
        original_filename = request.filename
        description = request.description
        image_type = request.image_type

        if not allowed_file(original_filename):
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details('Invalid file type')
            return Image()

        # Generate a unique filename
        filename = str(uuid.uuid4()) + os.path.splitext(original_filename)[1]
        file_path = os.path.join(DIR_LIST[image_type]['destination'], filename)

        # Save the file
        with open(file_path, 'wb') as f:
            f.write(file_data)

        # Save to database
        session = get_db()
        new_image = ImageModel(path=file_path, description=description)
        session.add(new_image)
        session.commit()

        response = Image(
            id=new_image.id,
            path=new_image.path,
            description=new_image.description,
            created_at=int(new_image.created_at.timestamp())
        )
        session.close()
        return response

    def CreateImage(self, request, context):
        session = get_db()
        new_image = ImageModel(path=request.path, description=request.description)
        session.add(new_image)
        session.commit()
        
        response = Image(
            id=new_image.id,
            path=new_image.path,
            description=new_image.description,
            created_at=int(new_image.created_at.timestamp())
        )
        session.close()
        return response

    def GetImage(self, request, context):
        session = get_db()
        image = session.query(ImageModel).filter(ImageModel.id == request.id).first()
        if not image:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Image not found')
            return Image()
        
        response = Image(
            id=image.id,
            path=image.path,
            description=image.description,
            created_at=int(image.created_at.timestamp())
        )
        session.close()
        return response

    def ListImages(self, request, context):
        session = get_db()
        offset = (request.page - 1) * request.page_size
        images = session.query(ImageModel).offset(offset).limit(request.page_size).all()
        total_count = session.query(ImageModel).count()
        
        response = ListImagesResponse(
            images=[
                Image(
                    id=image.id,
                    path=image.path,
                    description=image.description,
                    created_at=int(image.created_at.timestamp())
                ) for image in images
            ],
            total_count=total_count
        )
        session.close()
        return response