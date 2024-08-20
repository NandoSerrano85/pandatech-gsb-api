from gang_sheet_builder import create_gang_sheet
from util import (
    find_png_files,
    read_local_csv,
    select_csv_data_by_type,
    )
from constants import (
    ROOT_FOLDER,
    All_TYPES,
    MK_DPI,
    STD_DPI,
)
from gang_sheet_builder_v2 import create_image_gang_sheets


def main():
    order_range = "4634 - 4662"
    # order_range = "Order 4571"
    type_packs = ['5 Pack', 'Singles']
    tp = type_packs[1]
    order_csv = "Product Pick List {} - Original.csv".format(order_range)
    # order_csv = "Product Pick List {} - Order 4571.csv".format(order_range)
    # order_csv = "Product Pick List {} - MK {}.csv".format(order_range, tp)
    # order_csv = "Product Pick List {} - Rush 4654.csv".format(order_range)
    csvFilePath = "/Users/fserrano/Desktop/{}".format(order_csv)
    orderDict = read_local_csv(csvFilePath)
    # order_range = "Order 4571"
    All_TYPES = ['DTF', 'MK']

    for t in All_TYPES:
        target_dpi = STD_DPI if t != 'MK' else MK_DPI
        ordersByType = select_csv_data_by_type(orderDict, "{}{}".format(ROOT_FOLDER, t), t)
        
        if not ordersByType:
            continue
        if t == 'DTF':
            create_gang_sheet(input_images=ordersByType['Product title'], image_type=t, gang_sheet_type='DTF', output_path=ROOT_FOLDER, order_range=order_range, image_size=ordersByType['Size'],  dpi=target_dpi)
        else:
            create_gang_sheet(input_images=ordersByType['Product title'], image_type=t, gang_sheet_type='UVDTF', output_path=ROOT_FOLDER, order_range=order_range, dpi=target_dpi, text="{} ".format(tp))

    print("All Done!")
main()
