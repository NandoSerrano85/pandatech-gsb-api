import random
from ImageApp.app.core.gang_sheet_builder import create_gang_sheet
from ImageApp.app.core.util import (
    find_png_files,
    )
from ImageApp.app.core.constants import (
    ROOT_FOLDER,
    All_TYPES,
    MK_DPI,
    STD_DPI,
    DIR_LIST
)


def main():
    order_range = "PO ParisBerry 08252024"
    All_TYPES = ['UVDTF 16oz']
    type_packs = ['5 Pack', 'Singles']
    selected_amount = 300

    size = []

    for t in All_TYPES:
        current_amount = 0
        selectedFilePath = []
        target_dpi = STD_DPI if t != 'MK' else MK_DPI

        pngFilePath, pngFileName = find_png_files('{}ParisBerry'.format(ROOT_FOLDER))
        while current_amount < selected_amount:
            i = random.randint(0,len(pngFilePath)-1)
            selectedFilePath.append(pngFilePath[i])
            current_amount += 1
        if t == 'DTF':
            for n in range(len(pngFilePath)):
                size.append('Adult')
            create_gang_sheet(input_images=selectedFilePath, image_type=t, gang_sheet_type='DTF', output_path=ROOT_FOLDER, order_range=order_range, image_size=size,  dpi=target_dpi)
        else:
            create_gang_sheet(input_images=selectedFilePath, image_type=t, gang_sheet_type='UVDTF', output_path=ROOT_FOLDER, order_range=order_range, dpi=target_dpi, text="{} ".format(type_packs[1]))

    print("All Done!")
main()
