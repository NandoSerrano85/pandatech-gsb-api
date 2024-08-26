from fastapi import APIRouter, Depends, HTTPException
from ImageApp.app.core.image_cleanup import (
    image_cleanup,
)
from ImageApp.app.core.constants import (
    All_TYPES,
)

router = APIRouter()

@router.get("/cleanup/images/{image_type}")
def cleanup_images_by_type(image_type: str):
    if image_type in All_TYPES or image_type == 'all':
        if image_type == 'all':
            for t in All_TYPES:
                image_cleanup(t)
        else:
            image_cleanup(image_type)

        return HTTPException(status_code=200, detail={'Success': "all images in clean up folders have been cropped and resized."})
    else:
        return HTTPException(status_code=400, detail={'Error': "did not pass in the correct variable"})