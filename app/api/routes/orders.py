from fastapi import APIRouter
import shopify
from dotenv import load_dotenv
from app.core.util import (
    get_order_data,
)
from app.models.model_protos import (
    Order
)
from app.core.constants import (
    TABLE_DATA,
    MISSING_TABLE_DATA,
    All_TYPES,
    STD_DPI,
    MK_DPI,
    ROOT_FOLDER,
)
from app.core.gang_sheet_builder_v2 import (
    create_gang_sheets,
)
from app.core.config import Settings

settings = Settings()
router = APIRouter()

load_dotenv()

# @router.get("/get_unfulfilled_orders", response_model=GetOrdersResponse)
@router.get("/get_unfulfilled_orders")
def get_unfulfilled_orders():
    session = shopify.Session(settings.SHOPIFY_URL, settings.API_VERSION, settings.API_ACCESS_TOKEN)
    shopify.ShopifyResource.activate_session(session)

    # query for getting orders
    orders = shopify.Order().find()

    for order in orders:
        print(order.to_dict())

    