from fastapi import APIRouter
import shopify
from dotenv import load_dotenv
from app.core.util import (
    get_order_data,
)
from app.models.model_protos import (
    MissingImageModel
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

load_dotenv()

router = APIRouter()

@router.get("/create_gangsheets", response_model=MissingImageModel)
def create_gangsheets_from_shopify_orders():
    # Create a shopify session
    session = shopify.Session(settings.SHOPIFY_URL, settings.API_VERSION, settings.API_ACCESS_TOKEN)
    shopify.ShopifyResource.activate_session(session)

    # query for getting orders
    orders = shopify.Order().find()

    # variables for work
    order_data = TABLE_DATA
    missing_data_dict = MISSING_TABLE_DATA
    order_start, order_end = 999999999, 0
    order_range = ''
    data = {
        'DTF': {'Title':[], 'Size':[], 'Total':[], 'Type Total': 0},
        'UVDTF 16oz': {'Title':[], 'Size':[], 'Total':[], 'Type Total': 0},
        'UVDTF Decal':{'Title':[], 'Size':[], 'Total':[], 'Type Total': 0},
        'MK':{'Title':[], 'Size':[], 'Total':[], 'Type Total': 0},
        'UVDTF 40oz Top':{'Title':[], 'Size':[], 'Total':[], 'Type Total': 0},
        'UVDTF 40oz Bottom':{'Title':[], 'Size':[], 'Total':[], 'Type Total': 0},
        'Custom': {'Title':[], 'Size':[], 'Total':[], 'Type Total': 0},
        'UVDTF Bookmark': {'Title':[], 'Size':[], 'Total':[], 'Type Total': 0},
        'UVDTF Lid': {'Title':[], 'Size':[], 'Total':[], 'Type Total': 0},
        }

    # if more than 50 open orders logic for pagination else no need for pagination
    if len(orders) > 50:
        while orders.has_next_page():
            # gets all order data and format title according to need for gangsheet builder
            temp = get_order_data(orders, data)

            order_start = min(order_start, temp[0])
            order_end = max(order_end, temp[1])
            next_url = orders.next_page_url
            orders = shopify.Order().find(from_=next_url)
    else:
        order_start, order_end = get_order_data(orders, data)

    order_range = '{} - {}'.format(order_end, order_start)

    for k, v in data.items():
        if k not in All_TYPES:
            if len(missing_data_dict['Title']) == 0:
                missing_data_dict['Title'] = v['Title']
                missing_data_dict['Type'] = [k]
                missing_data_dict['Total'] = v['Total']
                missing_data_dict['Size'] = v['Size']
            else:
                missing_data_dict['Title'].append(v['Title'])
                missing_data_dict['Type'].append(k)
                missing_data_dict['Total'].append(v['Total'])
                missing_data_dict['Size'].append(v['Size'])

    for t in All_TYPES:
        target_dpi = STD_DPI if t != 'MK' else MK_DPI

        if t not in data:
            continue
        if t == 'DTF':
            gs_type = 'DTF'
        else:
            gs_type = 'UVDTF'
        missing_data = create_gang_sheets(image_data=data[t], image_type=t, gang_sheet_type=gs_type, output_path=ROOT_FOLDER, order_range=order_range, total_images=orders[t]['Type Total'],  dpi=target_dpi)
        if missing_data:
            if len(missing_data_dict['Title']) == 0:
                missing_data_dict['Title'] = missing_data['Title']
                missing_data_dict['Type'] = missing_data['Type']
                missing_data_dict['Total'] = missing_data['Total']
                missing_data_dict['Size'] = missing_data['Size']
            else:
                missing_data_dict['Title'].append(missing_data['Title'])
                missing_data_dict['Type'].append(missing_data['Type'])
                missing_data_dict['Total'].append(missing_data['Total'])
                missing_data_dict['Size'].append(missing_data['Size'])

    shopify.ShopifyResource.clear_session()

    return MissingImageModel({'title': missing_data_dict['Title'], 'type': missing_data_dict['Type'], 'size': missing_data_dict['Size'], 'total': missing_data_dict['Total']})


@router.get("/create_gangsheet/{order_number}")
def create_gangsheets_from_given_shopify_order(order_number: str):
    session = shopify.Session(settings.SHOPIFY_URL, settings.API_VERSION, settings.API_ACCESS_TOKEN)
    shopify.ShopifyResource.activate_session(session)

    # query for getting order
    order = shopify.Order().find(order_number=order_number)

    print(order)
    return order

