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
    ROOT_FOLDER_LOCAL,
    All_TYPES,
    MK_DPI,
    STD_DPI,
)


def main():
    allTypes = All_TYPES
    is_new_mk = False
    allTypes = ["DTF", "UVDTF 16oz", "UVDTF Decal", "MK", "Sublimation"]
    allTypes = ["MK"]

    for t in allTypes:
        # dirName = "ParisBerry"
        # dirName = "{}".format(t)
        if t == 'UVDTF 40oz Bottom':
            dirName = "UVDTF 40oz/Bottom Cleanup"
        elif t == 'UVDTF 40oz Top':
            dirName = "UVDTF 40oz/Top Cleanup"
        else:
            dirName = "{} Cleanup".format(t)
        # dirName = "Custom Cup Wraps"
        target_dpi = MK_DPI if (t == 'MK' or t == 'MK Tapered' or t == "UVDTF Logo Bottom Shot Decal" or t == 'UVDTF Logo Cup Care Decal') else STD_DPI
        print(target_dpi)
        print(t != 'MK' or t != 'MK Tapered')
        folderImagePath = "{}{}".format(ROOT_FOLDER_LOCAL, dirName)
        destinationImagePath = "{}{}".format(ROOT_FOLDER_LOCAL, t)
        # destinationImagePath = folderImagePath
        created_dir = False
        imageSize = None
        images = []
        resized_images = []
        if t == 'DTF' or t == 'Sublimation':
            imageSize = 'Adult+'

        pngFilePath, pngFileName = find_png_files(folderImagePath)

        print(t)
        if len(pngFilePath) < 1:
            continue

        if t != "UVDTF Lid":
            print("Start {}\nFile Path: {}\n".format(t, folderImagePath))
            #Cropping all images
            print_progress_bar(0, len(pngFilePath), prefix = 'Cropping:', suffix = 'Complete', length = 50)
            for n in range(0, len(pngFilePath)):
                images.append(crop_transparent(pngFilePath[n]))
                print_progress_bar(n+1, len(pngFilePath), prefix = 'Cropping:', suffix = 'Complete', length = 50)


        
        print_progress_bar(0, len(pngFilePath), prefix = 'Resizing:', suffix = 'Complete', length = 50)
        for n in range(0, len(pngFilePath)):
            if t == 'UVDTF 40oz Bottom':
                imageSize = 'Bottom'
            elif t == 'UVDTF 40oz Top':
                imageSize = 'Top'
            
            if len(images) > 0:
                resized_images.append(resize_image_by_inches(pngFilePath[n], t, imageSize, images[n], is_new_mk=is_new_mk, target_dpi=target_dpi))
            else:
                resized_images.append(resize_image_by_inches(pngFilePath[n], t, imageSize, is_new_mk=is_new_mk, target_dpi=target_dpi))
            print_progress_bar(n+1, len(pngFilePath), prefix = 'Resizing:', suffix = 'Complete', length = 50)

        # # #Creating destination folder
        # create_folder(destinationImagePath)

        print_progress_bar(0, len(pngFilePath), prefix = 'Saving:', suffix = 'Complete', length = 50)
        # #Saving all images to designated folder
        for n in range(0, len(pngFilePath)):
            if t == 'UVDTF 40oz Bottom' and re.search(r'/(Bottom Cleanup)/', pngFilePath[n]):
                destinationImagePath = "{}UVDTF 40oz/Bottom/".format(ROOT_FOLDER_LOCAL)
            elif t == 'UVDTF 40oz Top' and re.search(r'/(Top Cleanup)/', pngFilePath[n]):
                destinationImagePath = "{}UVDTF 40oz/Top/".format(ROOT_FOLDER_LOCAL)
            if (t == 'UVDTF 40oz Top' or t == 'UVDTF 40oz Bottom') and not created_dir:
                created_dir = True
                create_folder(destinationImagePath)
            save_single_image(resized_images[n], destinationImagePath, pngFileName[n], target_dpi=(target_dpi, target_dpi))
            print_progress_bar(n+1, len(pngFilePath), prefix = 'Saving:', suffix = 'Complete', length = 50)

        print("\n{} Total Images: {}\n".format(t, len(pngFilePath)))

    print("Finished All Cropping and Resizing!")
main()
