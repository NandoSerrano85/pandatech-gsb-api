ROOT_FOLDER_LOCAL = '/Users/fserrano/Desktop/'
ROOT_FOLDER_LOCAL_OUTPUT = '/Users/fserrano/Desktop/Printfiles/'
ROOT_FOLDER_LOCAL_CSV = '/Users/fserrano/Desktop/'
ROOT_FOLDER = '/app/data/'
DTF_DIR_CLEANUP = '{}DTF Cleanup/'.format(ROOT_FOLDER)
DTF_DIR = '{}DTF/'.format(ROOT_FOLDER)
UVDTF_16OZ_DIR_CLEANUP = '{}UVDTF 16oz Cleanup/'.format(ROOT_FOLDER)
UVDTF_16OZ_DIR = '{}UVDTF 16oz/'.format(ROOT_FOLDER)
UVDTF_DECAL_DIR_CLEANUP = '{}UVDTF Decal Cleanup/'.format(ROOT_FOLDER)
UVDTF_DECAL_DIR = '{}UVDTF Decal/'.format(ROOT_FOLDER)
UVDTF_MK_DIR_CLEANUP = '{}MK Cleanup/'.format(ROOT_FOLDER)
UVDTF_MK_DIR = '{}MK/'.format(ROOT_FOLDER)
UVDTF_BOOKMARK_DIR_CLEANUP = '{}UVDTF Bookmark Cleanup/'.format(ROOT_FOLDER)
UVDTF_BOOKMAK_DIR = '{}UVDTF Bookmark/'.format(ROOT_FOLDER)
UVDTF_LID_DIR_CLEANUP = '{}UVDTF Lid Cleanup/'.format(ROOT_FOLDER)
UVDTF_LID_DIR = '{}UVDTF Lid/'.format(ROOT_FOLDER)
UVDTF_40OZ_TOP_DIR_CLEANUP = '{}UVDTF 40oz/Top Cleanup/'.format(ROOT_FOLDER)
UVDTF_40OZ_TOP_DIR = '{}UVDTF 40oz/Top/'.format(ROOT_FOLDER)
UVDTF_40OZ_BOTTOM_DIR_CLEANUP = '{}UVDTF 40oz/Bottom Cleanup/'.format(ROOT_FOLDER)
UVDTF_40OZ_BOTTOM_DIR = '{}UVDTF 40oz/Bottom/'.format(ROOT_FOLDER)
UVDTF_MILK_CARTON_DIR_CLEANUP = '{}UVDTF Milk Carton Cleanup/'.format(ROOT_FOLDER)
UVDTF_MILK_CARTON_DIR = '{}UVDTF Milk Carton/'.format(ROOT_FOLDER)

DIR_LIST = {
    'DTF':{
        'source': DTF_DIR_CLEANUP,
        'destination': DTF_DIR,
    }, 
    'UVDTF 16oz':{
        'source': UVDTF_16OZ_DIR_CLEANUP,
        'destination': UVDTF_16OZ_DIR,
    },
    'UVDTF Decal':{
        'source': UVDTF_DECAL_DIR_CLEANUP,
        'destination': UVDTF_DECAL_DIR,
    },
    'MK':{
        'source': UVDTF_MK_DIR_CLEANUP,
        'destination': UVDTF_MK_DIR,
    },
    'UVDTF 40oz Top':{
        'source': UVDTF_40OZ_TOP_DIR_CLEANUP,
        'destination': UVDTF_40OZ_TOP_DIR,
    },
    'UVDTF 40oz Bottom':{
        'source': UVDTF_40OZ_BOTTOM_DIR_CLEANUP,
        'destination': UVDTF_40OZ_BOTTOM_DIR,
    },
    'UVDTF Bookmark':{
        'source': UVDTF_BOOKMARK_DIR_CLEANUP,
        'destination': UVDTF_BOOKMAK_DIR,
    },
    'UVDTF Lid':{
        'source': UVDTF_LID_DIR_CLEANUP,
        'destination': UVDTF_LID_DIR,
    },
    'UVDTF Milk Carton' : {
        'source': UVDTF_MILK_CARTON_DIR_CLEANUP,
        'destination': UVDTF_MILK_CARTON_DIR,
    }
}
MK_DPI = 950
STD_DPI = 400
TEXT_AREA_HEIGHT = 0.015
SHEET_HEIGHT = 120

All_TYPES = ['DTF', 'UVDTF 16oz', 'UVDTF Decal', 'MK', 'UVDTF 40oz Top', 'UVDTF 40oz Bottom', 'UVDTF Bookmark', 'UVDTF Lid', 'UVDTF Milk Carton']

All_TYPES_DICT = {
    'DTF Transfer': 'DTF',
    '16oz UVDTF Cup Wrap': 'UVDTF 16oz',
    '16oz UVDTF Cup Wrap (EXCLUSIVE)': 'UVDTF 16oz',
    'UVDTF Decal': 'UVDTF Decal',
    'Motel Keychain': 'MK',
    '40oz UVDTF Tumbler Wrap': 'UVDTF 40oz',
    'UVDTF Bookmark Decal': 'UVDTF Bookmark',
    'UVDTF Lid Decal': 'UVDTF Lid',
    'UVDTF Milk Carton': 'UVDTF Milk Carton',
}

PACK_LISTS = {
    'Single': 1,
    'Default title': 1,
    '5 Pack': 5,
    '10 Pack': 10,
    '15 Pack': 15
}

SIZE_LIST = {
    'Adult+ 13"': 'Adult+',
    'Adult 11"': 'Adult',
    'Youth 8"': 'Youth',
    'Toddler 6"': 'Toddler',
    'Pocket 4"': 'Pocket',
    'Adult Plus': 'Adult+',
}

TABLE_DATA = {
    'Title':[], 
    'Type':[], 
    'Size':[],
    'Total':[],
}

MISSING_TABLE_DATA = {
    'Title':[], 
    'Type':[], 
    'Size':[],
    'Total': [],
}

SIZING = {
    'DTF': {
        'Adult+': { 'height': 13.0 },
        'Adult': { 'height': 11.0 },
        'Youth': { 'height': 8.0 },
        'Toddler': { 'height': 6.0 },
        'Pocket': { 'height': 4.0 },
    },
    'UVDTF 16oz': { 'width': 9.4, 'height': 4.33 },
    'UVDTF Decal': { 'height': 4.0, 'width': 4.0 },
    'MK': { 'width': 1.3, 'height': 1.75 },
    'MK Rectangle': {'width': 0.9, 'height': 2},
    'MK Tapered': {'width': 1.65, 'height': 2.4},
    'UVDTF Bookmark': { 'width': 5.5, 'height': 1.8 },
    'UVDTF 40oz Top': {'width': 11.3, 'height': 5 },
    'UVDTF 40oz Bottom': {'width': 10.3, 'height': 3.58 },
    # 'UVDTF 40oz Bottom': {'width': 10, 'height': 3.2 },
    'UVDTF Bookmark': {'width': 5.5, 'height': 1.8 },
    'UVDTF Lid': {'width': 2.75, 'height': 2.75 },
    'UVDTF Milk Carton': {'width': 2.2, 'height': 6.1 },
    'Custom 2x2': {'width': 2, 'height': 2 },
}

CANVAS = {
    'UVDTF Decal': { 'height': 4.0, 'width': 4.0 },
    'MK': { 'width': 1.5, 'height': 2.3 },
    'MK Rectangle': {'width': 1.5, 'height': 2.3},
    'MK Tapered': { 'width': 1.75, 'height': 2.6 },
    'UVDTF 40oz Bottom': {'width': 10.3, 'height': 3.58, 'arch': 3},
    'UVDTF Lid': {'width': 2.75, 'height': 2.75 },
    'UVDTF Bookmark': {'width': 5.5, 'height': 1.8 },
    'UVDTF Milk Carton': {'width': 2.2, 'height': 6.1 },
    'Custom 2x2': {'width': 2, 'height': 2 },
}

DTF_MAX_SIZE = 'Adult+'

UVDTF_GANG_SHEET_MAX_WIDTH = 22.7

UVDTF_GANG_SHEET_MAX_ROW_16OZ = 5
UVDTF_GANG_SHEET_MAX_ROW_DECAL = 5
UVDTF_GANG_SHEET_MAX_ROW_MK = 15
UVDTF_GANG_SHEET_MAX_ROW_40OZ_TOP = 4
UVDTF_GANG_SHEET_MAX_ROW_40OZ_BOTTOM = 2
UVDTF_GANG_SHEET_MAX_ROW_LID = 7
UVDTF_GANG_SHEET_MAX_ROW_BOOKMARK = 10
UVDTF_GANG_SHEET_MAX_ROW_CUSTOM_2X2 = 10
UVDTF_GANG_SHEET_MAX_ROW = {
    'UVDTF 16oz': UVDTF_GANG_SHEET_MAX_ROW_16OZ,
    'UVDTF Decal': UVDTF_GANG_SHEET_MAX_ROW_DECAL,
    'MK': UVDTF_GANG_SHEET_MAX_ROW_MK,
    'UVDTF 40oz Top': UVDTF_GANG_SHEET_MAX_ROW_40OZ_TOP,
    'UVDTF 40oz Bottom': UVDTF_GANG_SHEET_MAX_ROW_40OZ_BOTTOM,
    'UVDTF Bookmark': UVDTF_GANG_SHEET_MAX_ROW_BOOKMARK,
    'UVDTF Lid': UVDTF_GANG_SHEET_MAX_ROW_LID,
    'Custom 2x2': UVDTF_GANG_SHEET_MAX_ROW_CUSTOM_2X2,
}

UVDTF_GANG_SHEET_SPACING_16OZ = {'width': 0.26, 'height': 0.5}
UVDTF_GANG_SHEET_SPACING_DECAL = {'width': 0.6, 'height': 0.3}
UVDTF_GANG_SHEET_SPACING_MK = {'width': 0.0, 'height': 0.0}
UVDTF_GANG_SHEET_SPACING_40OZ_TOP = {'width': 0.4, 'height': 0.3}
UVDTF_GANG_SHEET_SPACING_40OZ_BOTTOM  = {'width': 0.4, 'height': 0.3}
UVDTF_GANG_SHEET_SPACING_BOOKMARK = {'width': 0.3, 'height': 0.3}
UVDTF_GANG_SHEET_SPACING_LID = {'width': 0.3, 'height': 0.3}
UVDTF_GANG_SHEET_SPACING_CUSTOM_2X2 = {'width': 0.3, 'height': 0.3}
UVDTF_GANG_SHEET_SPACING_MILK_CARTON = {'width': 0.3, 'height': 0.3}
UVDTF_GANG_SHEET_SPACING = {
    'UVDTF 16oz': UVDTF_GANG_SHEET_SPACING_16OZ,
    'UVDTF Decal': UVDTF_GANG_SHEET_SPACING_DECAL,
    'MK': UVDTF_GANG_SHEET_SPACING_MK,
    'UVDTF 40oz Top': UVDTF_GANG_SHEET_SPACING_40OZ_TOP,
    'UVDTF 40oz Bottom': UVDTF_GANG_SHEET_SPACING_40OZ_BOTTOM,
    'UVDTF Bookmark': UVDTF_GANG_SHEET_SPACING_BOOKMARK,
    'UVDTF Lid': UVDTF_GANG_SHEET_SPACING_LID,
    'Custom 2x2': UVDTF_GANG_SHEET_SPACING_CUSTOM_2X2,
    'UVDTF Milk Carton': UVDTF_GANG_SHEET_SPACING_MILK_CARTON,
}
UVDTF_GANG_SHEET_MAX_HEIGHT_16OZ = 9.4
UVDTF_GANG_SHEET_MAX_HEIGHT_DECAL = 4.0
UVDTF_GANG_SHEET_MAX_HEIGHT_MK = 2.3
UVDTF_GANG_SHEET_MAX_HEIGHT_40OZ_TOP = 11.3
UVDTF_GANG_SHEET_MAX_HEIGHT_40OZ_BOTTOM = 3.58
UVDTF_GANG_SHEET_MAX_HEIGHT_BOOKMARK = 5.5
UVDTF_GANG_SHEET_MAX_HEIGHT_LID = 2.75
UVDTF_GANG_SHEET_MAX_HEIGHT_CUSTOM_2X2 = 2
UVDTF_GANG_SHEET_MAX_HEIGHT_MILK_CARTON = 6.1
UVDTF_GANG_SHEET_MAX_HEIGHT = {
    'UVDTF 16oz': UVDTF_GANG_SHEET_MAX_HEIGHT_16OZ,
    'UVDTF Decal': UVDTF_GANG_SHEET_MAX_HEIGHT_DECAL,
    'MK': UVDTF_GANG_SHEET_MAX_HEIGHT_MK,
    'UVDTF 40oz Top':UVDTF_GANG_SHEET_MAX_HEIGHT_40OZ_TOP,
    'UVDTF 40oz Bottom': UVDTF_GANG_SHEET_MAX_HEIGHT_40OZ_BOTTOM,
    'UVDTF Bookmark': UVDTF_GANG_SHEET_MAX_HEIGHT_BOOKMARK,
    'UVDTF Lid': UVDTF_GANG_SHEET_MAX_HEIGHT_LID,
    'Custom 2x2': UVDTF_GANG_SHEET_MAX_HEIGHT_CUSTOM_2X2,
    'UVDTF Milk Carton': UVDTF_GANG_SHEET_MAX_HEIGHT_MILK_CARTON,
}

DTF_GANG_SHEET_MAX_WIDTH = 22

DTF_GANG_SHEET_SPACING_ADULT_PLUS = {'width': 0.5, 'height': 0.5}
DTF_GANG_SHEET_SPACING = { 
    'Adult+': DTF_GANG_SHEET_SPACING_ADULT_PLUS,
    'Adult': DTF_GANG_SHEET_SPACING_ADULT_PLUS,
    'Youth': DTF_GANG_SHEET_SPACING_ADULT_PLUS,
    'Toddler': DTF_GANG_SHEET_SPACING_ADULT_PLUS,
    'Pocket': DTF_GANG_SHEET_SPACING_ADULT_PLUS,
}

DTF_GANG_SHEET_MAX_HEIGHT_ADULT_PLUS = 13.0
DTF_GANG_SHEET_MAX_HEIGHT_ADULT = 11.0
DTF_GANG_SHEET_MAX_HEIGHT_YOUTH = 8.0
DTF_GANG_SHEET_MAX_HEIGHT_TODDLER = 6.0
DTF_GANG_SHEET_MAX_HEIGHT_POCKET = 4.0
DTF_GANG_SHEET_MAX_HEIGHT = {
    'Adult+': DTF_GANG_SHEET_MAX_HEIGHT_ADULT_PLUS,
    'Adult': DTF_GANG_SHEET_MAX_HEIGHT_ADULT,
    'Youth': DTF_GANG_SHEET_MAX_HEIGHT_YOUTH,
    'Toddler': DTF_GANG_SHEET_MAX_HEIGHT_TODDLER,
    'Pocket': DTF_GANG_SHEET_MAX_HEIGHT_POCKET,
}

DTF_GANG_SHEET_MAX_ROW_ADULT_PLUS = 1
DTF_GANG_SHEET_MAX_ROW_ADULT = 2
DTF_GANG_SHEET_MAX_ROW_YOUTH = 3
DTF_GANG_SHEET_MAX_ROW_TODDLER = 4
DTF_GANG_SHEET_MAX_ROW_POCKET = 5
DTF_GANG_SHEET_MAX_ROW = {
    'Adult+': DTF_GANG_SHEET_MAX_ROW_ADULT_PLUS,
    'Adult': DTF_GANG_SHEET_MAX_ROW_ADULT,
    'Youth': DTF_GANG_SHEET_MAX_ROW_YOUTH,
    'Toddler': DTF_GANG_SHEET_MAX_ROW_TODDLER,
    'Pocket': DTF_GANG_SHEET_MAX_ROW_POCKET,
}

GANG_SHEET_MAX_WIDTH = {
    'UVDTF': UVDTF_GANG_SHEET_MAX_WIDTH,
    'DTF': DTF_GANG_SHEET_MAX_WIDTH,
    'Custom 2x2': 22,
}

GANG_SHEET_SPACING = {
    'UVDTF' : UVDTF_GANG_SHEET_SPACING,
    'DTF': DTF_GANG_SHEET_SPACING
}
GANG_SHEET_MAX_ROW = {
    'UVDTF': UVDTF_GANG_SHEET_MAX_ROW,
    'DTF': DTF_GANG_SHEET_MAX_ROW,
}

GANG_SHEET_MAX_ROW_HEIGHT = {
    'UVDTF': UVDTF_GANG_SHEET_MAX_HEIGHT,
    'DTF': DTF_GANG_SHEET_MAX_HEIGHT,
}

GANG_SHEET_MAX_HEIGHT = {
    'UVDTF': SHEET_HEIGHT + (TEXT_AREA_HEIGHT * SHEET_HEIGHT),
    'DTF': SHEET_HEIGHT + (TEXT_AREA_HEIGHT * SHEET_HEIGHT),
    'Custom 2x2': 36
}
ALLOWED_EXTENSIONS = {'png', 'svg', 'tiff'}

