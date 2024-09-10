from app.core.gang_sheet_builder import create_gang_sheet
from app.core.gang_sheet_builder_v2 import create_gang_sheets
from app.core.util import (
    read_local_csv,
    select_csv_data_by_type,
    sort_csv_data_by_type_optimized,
    )
from app.core.constants import (
    ROOT_FOLDER_LOCAL,
    All_TYPES,
    MK_DPI,
    STD_DPI,
)

def csv_reader_v1():
    order_range = "4788 - 4811"
    type_packs = ['5 Pack', 'Singles']
    tp = type_packs[1]
    order_csv = "Product Pick List 4788 - 4811 - Original.csv"
    csvFilePath = "{}{}".format(ROOT_FOLDER_LOCAL, order_csv)
    orderDict = read_local_csv(csvFilePath)
    All_TYPES = ['UVDTF 40oz']

    for t in All_TYPES:
        target_dpi = STD_DPI if t != 'MK' else MK_DPI
        ordersByType = select_csv_data_by_type(orderDict, "{}{}".format(ROOT_FOLDER_LOCAL, t), t)
        
        if not ordersByType:
            continue
        if t == 'DTF':
            create_gang_sheet(input_images=ordersByType['Product title'], image_type=t, gang_sheet_type='DTF', output_path=ROOT_FOLDER_LOCAL, order_range=order_range, image_size=ordersByType['Size'],  dpi=target_dpi)
        else:
            if t == 'UVDTF 40oz':
                create_gang_sheet(input_images=ordersByType['Product title'], image_type='UVDTF 40oz Top', gang_sheet_type='UVDTF', output_path=ROOT_FOLDER_LOCAL, order_range=order_range, dpi=target_dpi, text="{} ".format(tp))
                create_gang_sheet(input_images=ordersByType['Product title'], image_type='UVDTF 40oz Bottom', gang_sheet_type='UVDTF', output_path=ROOT_FOLDER_LOCAL, order_range=order_range, dpi=target_dpi, text="{} ".format(tp))
            else:
                create_gang_sheet(input_images=ordersByType['Product title'], image_type=t, gang_sheet_type='UVDTF', output_path=ROOT_FOLDER_LOCAL, order_range=order_range, dpi=target_dpi, text="{} ".format(tp))

    print("All Done!")

def csv_reader_v2():
    order_range = "4788 - 4821"
    order_csv = "Product Pick List 4788 - 4821 - Original.csv"
    csvFilePath = "{}{}".format(ROOT_FOLDER_LOCAL, order_csv)
    orderDict = read_local_csv(csvFilePath)
    # All_TYPES=['UVDTF 40oz Top', 'UVDTF 40oz Bottom'] 

    for t in All_TYPES:
        gs_type = None
        target_dpi = STD_DPI if t != 'MK' else MK_DPI
        orders = sort_csv_data_by_type_optimized(orderDict, ROOT_FOLDER_LOCAL, t)

        if not orders:
            continue
        
        if t == 'DTF':
            gs_type = 'DTF'
        else:
            gs_type = 'UVDTF'
            
        create_gang_sheets(image_data=orders[t], image_type=t, gang_sheet_type=gs_type, output_path=ROOT_FOLDER_LOCAL, order_range=order_range, total_images=orders['Type Total'],  dpi=target_dpi)
    print('All Done!')

def main():
    csv_reader_v2()
main()