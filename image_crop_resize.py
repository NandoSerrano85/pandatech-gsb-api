import re
from croppping import crop_transparent
from resizing import resize_image_by_inches
from util import (
    create_folder,
    find_png_files,
    save_single_image,
    print_progress_bar,
    )
from constants import (
    ROOT_FOLDER,
    All_TYPES,
    MK_DPI,
    STD_DPI,
)


def main():
    allTypes = All_TYPES
    # allTypes = ['MK']
    is_new_mk = False

    for t in allTypes:
        dirName = "{}".format(t)
        # dirName = "{}/Top Cleanup".format(t)
        dirName = "{} Cleanup".format(t)
        target_dpi = STD_DPI if t != 'MK' else MK_DPI
        folderImagePath = "{}{}".format(ROOT_FOLDER, dirName)
        destinationImagePath = "{}{}".format(ROOT_FOLDER,t)
        # destinationImagePath = folderImagePath
        created_dir = False
        imageSize = None
        images = []
        resized_images = []
        if t == 'DTF':
            imageSize = 'Adult+'

        pngFilePath, pngFileName = find_png_files(folderImagePath)


        print("Start {}\nFile Path: {}\n".format(t, folderImagePath))
        #Cropping all images
        print_progress_bar(0, len(pngFilePath), prefix = 'Cropping:', suffix = 'Complete', length = 50)
        for n in range(0, len(pngFilePath)):
            images.append(crop_transparent(pngFilePath[n]))
            print_progress_bar(n+1, len(pngFilePath), prefix = 'Cropping:', suffix = 'Complete', length = 50)


        
        print_progress_bar(0, len(pngFilePath), prefix = 'Resizing:', suffix = 'Complete', length = 50)
        for n in range(0, len(pngFilePath)):
            if t == 'UVDTF 40oz' and re.search(r'/(Bottom Cleanup)/', pngFilePath[n]):
                imageSize = 'Bottom'
            elif t == 'UVDTF 40oz' and re.search(r'/(Top Cleanup)/', pngFilePath[n]):
                imageSize = 'Top'
            
            if len(images) > 0:
                resized_images.append(resize_image_by_inches(pngFilePath[n], t, imageSize, images[n], is_new_mk=is_new_mk, target_dpi=target_dpi))
            else:
                resized_images.append(resize_image_by_inches(pngFilePath[n], t, imageSize, is_new_mk=is_new_mk, target_dpi=target_dpi))
            print_progress_bar(n+1, len(pngFilePath), prefix = 'Resizing:', suffix = 'Complete', length = 50)

        # # #Creating destination folder
        create_folder(destinationImagePath)

        print_progress_bar(0, len(pngFilePath), prefix = 'Saving:', suffix = 'Complete', length = 50)
        # #Saving all images to designated folder
        for n in range(0, len(pngFilePath)):
            if t == 'UVDTF 40oz' and re.search(r'/(Bottom Cleanup)/', pngFilePath[n]):
                destinationImagePath = "{}{}/Bottom/".format(ROOT_FOLDER,t)
            elif t == 'UVDTF 40oz' and re.search(r'/(Top Cleanup)/', pngFilePath[n]):
                destinationImagePath = "{}{}/Top/".format(ROOT_FOLDER,t)
            if t == 'UVDTF 40oz' and not created_dir:
                created_dir = True
                create_folder(destinationImagePath)
            save_single_image(resized_images[n], destinationImagePath, pngFileName[n], target_dpi=(target_dpi, target_dpi))
            print_progress_bar(n+1, len(pngFilePath), prefix = 'Saving:', suffix = 'Complete', length = 50)

        print("\n{} Total Images: {}\n".format(t, len(pngFilePath)))

    print("Finished All Cropping and Resizing!")
main()
