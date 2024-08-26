from app.core.gang_sheet_builder import create_gang_sheet
from app.core.util import (
    find_png_files,
    read_local_csv,
    select_csv_data_by_type,
    )
from app.core.constants import (
    ROOT_FOLDER,
    All_TYPES,
    MK_DPI,
    STD_DPI,
)

def main():
    order_range = "Rush 4714"
    type_packs = ['5 Pack', 'Singles']
    tp = type_packs[1]
    order_csv = "Sublimation 08262024 - Sheet2.csv"
    csvFilePath = "/Users/fserrano/Desktop/{}".format(order_csv)
    orderDict = read_local_csv(csvFilePath)
    All_TYPES = ['UVDTF 16oz', 'UVDTF Decal']

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
