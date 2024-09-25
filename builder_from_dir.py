import random
from app.core.gang_sheet_builder import create_gang_sheet
from app.core.gang_sheet_builder_v2 import create_gang_sheets, process_gang_sheets_concurrently
from app.core.util import (
    find_png_files,
    )
from app.core.constants import (
    ROOT_FOLDER_LOCAL,
    All_TYPES,
    MK_DPI,
    STD_DPI,
    DIR_LIST
)

def parris_berry():
    order_range = "PO ParisBerry 09152024"
    All_TYPES = ['UVDTF 16oz']
    type_packs = ['5 Pack', 'Singles']
    order_range = "Custom Gangsheet"
    All_TYPES = ['UVDTF 16oz']
    selected_amount = 11

    size = []

    for t in All_TYPES:
        current_amount = 0
        selectedFilePath = list()
        target_dpi = STD_DPI if t != 'MK' else MK_DPI

        pngFilePath, pngFileName = find_png_files('{}Custom Cup Wraps'.format(ROOT_FOLDER_LOCAL))
    
        while current_amount < selected_amount:
            # i = random.randint(0,len(pngFilePath)-1)
            selectedFilePath.append(pngFilePath.pop(0))
            current_amount += 1
        if t == 'DTF':
            for n in range(len(pngFilePath)):
                size.append('Adult')
            create_gang_sheet(input_images=selectedFilePath, image_type=t, gang_sheet_type='DTF', output_path=ROOT_FOLDER_LOCAL, order_range=order_range, image_size=size,  dpi=target_dpi)
        else:
            create_gang_sheet(input_images=selectedFilePath, image_type=t, gang_sheet_type='UVDTF', output_path=ROOT_FOLDER_LOCAL, order_range=order_range, dpi=target_dpi, text="{} ".format(type_packs[1]))

    print("All Done!")

def customs():
    order_range = "Custom Gangsheet"
    All_TYPES = ['UVDTF 16oz']
    selected_amount = 200

    size = []

    for t in All_TYPES:
        target_dpi = STD_DPI if t != 'MK' else MK_DPI

        pngFilePath, pngFileName = find_png_files('{}Custom Cup Wraps'.format(ROOT_FOLDER_LOCAL))

        orders = {t: 
                  {
                      'Title': [],
                      'Size': [],
                      'Total': [],
                   },
                   'Type Total':len(pngFilePath),
                }
        for png in pngFilePath:
            orders[t]['Title'].append(png)
            orders[t]['Size'].append('')
            orders[t]['Total'].append(1)

        if t == 'DTF':
            gs_type = 'DTF'
            for n in range(len(pngFilePath)):
                size.append('Adult')
        elif t == 'Custom 2x2':
            gs_type = 'Custom 2x2'
        else:
            gs_type = 'UVDTF'
        
        create_gang_sheets(image_data=orders[t], image_type=t, gang_sheet_type=gs_type, output_path=ROOT_FOLDER_LOCAL, order_range=order_range, total_images=orders['Type Total'],  dpi=target_dpi)

    print("All Done!")

def main():
    customs()
main()
