from fastapi import APIRouter, Depends, HTTPException
import os, shopify, multiprocessing
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
from app.core.gang_sheet_builder import (
    create_gang_sheet,
    create_gang_sheet_kwargs,
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
    data = dict()

    # if more than 50 open orders logic for pagination else no need for pagination
    if len(orders) > 50:
        while orders.has_next_page():
            # gets all order data and format title according to need for gangsheet builder
            temp = get_order_data(orders)

            order_data['Title'].append(temp[0])
            order_data['Type'].append(temp[1])
            order_data['Size'].append(temp[2])
            order_data['Total'].append(temp[3])
            order_start = min(order_start, temp[4])
            order_end = max(order_end, temp[5])
            next_url = orders.next_page_url
            orders = shopify.Order().find(from_=next_url)
    else:
        order_data['Title'], order_data['Type'], order_data['Size'], order_data['Total'],  order_start, order_end = get_order_data(orders)

    # clean up
    for n in range(len(order_data['Type'])):
        if order_data['Type'][n] not in data:
            data[order_data['Type'][n]] = {'Title': [], 'Size': [], 'Total': []}

        data[order_data['Type'][n]]['Title'].append(order_data['Title'][n])
        data[order_data['Type'][n]]['Size'].append(order_data['Size'][n])
        data[order_data['Type'][n]]['Total'].append(order_data['Total'][n])

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
            missing_data = create_gang_sheet(input_images=data[t]['Title'], image_type=t, gang_sheet_type='DTF', output_path=ROOT_FOLDER, order_range=order_range, image_size=data[t]['Size'],  dpi=target_dpi)
        else:
            missing_data = create_gang_sheet(input_images=data[t]['Title'], image_type=t, gang_sheet_type='UVDTF', output_path=ROOT_FOLDER, order_range=order_range, dpi=target_dpi, text='Singles')

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

    #     pool = multiprocessing.Pool(processes=4)
    #     if t == 'DTF':
    #         missing_data = pool.map(create_gang_sheet_kwargs, [{'input_images':data[t]['Title'], 'image_type':t, 'gang_sheet_type':'DTF', 'output_path':ROOT_FOLDER, 'order_range':order_range, 'image_size':data[t]['Size'], 'dpi':target_dpi}])
    #     else:
    #         missing_data = pool.map(create_gang_sheet_kwargs, [{'input_images':data[t]['Title'], 'image_type':t, 'gang_sheet_type':'UVDTF', 'output_path':ROOT_FOLDER, 'order_range':order_range, 'dpi':target_dpi, 'text':'Singles'}])

    #     if missing_data:
    #         for msd in missing_data:
    #             if not msd:
    #                 continue
    #             if len(missing_data_dict['Title']) == 0:
    #                 missing_data_dict['Title'] = msd['Title']
    #                 missing_data_dict['Type'] = msd['Type']
    #                 missing_data_dict['Total'] = msd['Total']
    #                 missing_data_dict['Size'] = msd['Size']
    #             else:
    #                 missing_data_dict['Title'].append(msd['Title'])
    #                 missing_data_dict['Type'].append(msd['Type'])
    #                 missing_data_dict['Total'].append(msd['Total'])
    #                 missing_data_dict['Size'].append(msd['Size'])

    # pool.close()
    # print("Pool is closed. No new tasks will be accepted.")
    # pool.join()
    # print("Pool has been joined. All processes have exited.")
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

