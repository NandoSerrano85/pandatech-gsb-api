from pydantic import BaseModel
from typing import Union

class MissingDataResponse(BaseModel):
    title: Union[list, None] = None
    type: Union[list, None] = None
    size: Union[list, None] = None
    total: Union[list, None] = None

