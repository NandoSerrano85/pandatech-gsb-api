import os, shopify, multiprocessing
from dotenv import load_dotenv
from typing import Union
from pprint import pprint

from fastapi import FastAPI
from models.api_model import (
    MissingDataTable
)

from constants import (
    TABLE_DATA,
    STD_DPI,
    MK_DPI,
    All_TYPES,
    ROOT_FOLDER,
    MISSING_TABLE_DATA,
)

from util import (
    get_order_data,
)

from gang_sheet_builder import create_gang_sheet, create_gang_sheet_kwargs
from image_cleanup import image_cleanup


load_dotenv()

app = FastAPI()


# session = shopify.Session(os.getenv('SHOPIFY_URL'), os.getenv('API_VERSION'), os.getenv('API_ACCESS_TOKEN'))
# shopify.ShopifyResource.activate_session(session)

# query = open(os.path.join("graphql","connection_query.graphql")).read()
# query = os.path.
# shopify.GraphQL().execute('{ shop { name id } }')
# shopify.ShopifyResource.clear_session()
# shopify.Session.setup(api_key=os.getenv('API_KEY'), secret=os.getenv('API_SECRET'))
# with shopify.Session.temp("https://{}/admin".format('21458d'), os.getenv('API_VERSION'), os.getenv('API_ACCESS_TOKEN')):
#     print(shopify.ShopifyResource.get_site() + "/graphql.json")
#     pprint(shopify.GraphQL().execute('{ shop { name id } }'))
# shop_url = "https://%s:%s@%s/admin" % (os.getenv('API_KEY'), os.getenv('API_ACCESS_TOKEN'), os.getenv('SHOP_URL'))
# shopify.ShopifyResource.set_site(shop_url)


# product = shopify.Product.find(9285254185261)
# collection = shopify.GraphQL.execute(
#     query=query,
#     variables={"first": 10},
#     operation_name="GetFirstNCollections",
# )
# orders = shopify.Order().find()
# for order in orders:
#     order_dict = order.to_dict()
#     pprint(order_dict)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/create_gangsheets")
def read_create_gangasheets() -> MissingDataTable:
    # Create a shopify session
    session = shopify.Session(os.getenv('SHOPIFY_URL'), os.getenv('API_VERSION'), os.getenv('API_ACCESS_TOKEN'))
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

    return {'title': missing_data_dict['Title'], 'type': missing_data_dict['Type'], 'size': missing_data_dict['Size'], 'total': missing_data_dict['Total']}


@app.get("/cleanup/{image_type}")
def read_item(image_type: str):
    if image_type in All_TYPES or image_type == 'all':
        if image_type == 'all':
            for t in All_TYPES:
                image_cleanup(t)
        else:
            image_cleanup(image_type)

        return {'Success': "all images in clean up folders have been cropped and resized."}
    else:
        return {'Error': "did not pass in the correct variable"}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}