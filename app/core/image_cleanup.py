import re
from app.core.croppping import crop_transparent
from app.core.resizing import resize_image_by_inches
from app.core.util import (
    create_folder,
    find_png_files,
    save_single_image,
    print_progress_bar,
    )
from app.core.constants import (
    STD_DPI,
    MK_DPI,
    All_TYPES,
    DTF_MAX_SIZE,
    DIR_LIST,
)

def image_cleanup(image_type = All_TYPES):
    images = []
    resized_images = []
    imageSize = None

    target_dpi = STD_DPI if image_type != 'MK' else MK_DPI
    pngFilePath, pngFileName = find_png_files(DIR_LIST[image_type]['source'])

    if image_type == 'UVDTF 40oz Bottom' and re.search(r'/(Bottom Cleanup)/', pngFilePath[n]):
        imageSize = 'Bottom'
    elif image_type == 'UVDTF 40oz Top' and re.search(r'/(Top Cleanup)/', pngFilePath[n]):
        imageSize = 'Top'
    elif image_type == 'DTF':
        imageSize = DTF_MAX_SIZE

    for n in range(0, len(pngFilePath)):
        images.append(crop_transparent(pngFilePath[n]))

    for n in range(0, len(pngFilePath)):
        if len(images) > 0:
            resized_images.append(resize_image_by_inches(pngFilePath[n], image_type, imageSize, images[n], is_new_mk=False, target_dpi=target_dpi))
        else:
            resized_images.append(resize_image_by_inches(pngFilePath[n], image_type, imageSize, is_new_mk=False, target_dpi=target_dpi))

    create_folder(DIR_LIST[image_type]['destination'])
    for n in range(0, len(pngFilePath)):
        save_single_image(resized_images[n], DIR_LIST[image_type]['destination'], pngFileName[n], target_dpi=(target_dpi, target_dpi))