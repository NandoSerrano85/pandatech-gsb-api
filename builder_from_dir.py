from gang_sheet_builder import create_gang_sheet
from util import (
    find_png_files,
    )
from constants import (
    ROOT_FOLDER,
    All_TYPES,
    MK_DPI,
    STD_DPI,
)


def main():
    order_range = "Test Prints Gravitees"
    All_TYPES = ['DTF', 'UVDTF 16oz']
    type_packs = ['5 Pack', 'Singles']

    size =[]

    for t in All_TYPES:
        target_dpi = STD_DPI if t != 'MK' else MK_DPI
        folderImagePath = "{}PRINT THESE/{}/Gravitees".format(ROOT_FOLDER, t)

        pngFilePath, pngFileName = find_png_files(folderImagePath)
        
        # if not ordersByType:
        #     pass
        if t == 'DTF':
            for n in range(len(pngFilePath)):
                size.append('Adult')
            create_gang_sheet(input_images=pngFilePath, image_type=t, gang_sheet_type='DTF', output_path=ROOT_FOLDER, order_range=order_range, image_size=size,  dpi=target_dpi)
        else:
            create_gang_sheet(input_images=pngFilePath, image_type=t, gang_sheet_type='UVDTF', output_path=ROOT_FOLDER, order_range=order_range, dpi=target_dpi, text="{} ".format(type_packs[1]))

    print("All Done!")
main()
