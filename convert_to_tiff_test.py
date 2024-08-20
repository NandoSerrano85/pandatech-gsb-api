from util import (
    png_to_cmyk_tiff
)
from constants import (
    ROOT_FOLDER,
    All_TYPES,
    MK_DPI,
    STD_DPI,
)

def main():
    png_to_cmyk_tiff("{}/DTF Test/Tired Deprived Moms Club - DTF Transfer.png".format(ROOT_FOLDER), "{}/DTF Test/Tired Deprived Moms Club - DTF Transfer.tiff".format(ROOT_FOLDER))

main()