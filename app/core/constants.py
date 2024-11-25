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
UVDTF_ORNAMENT_DIR_CLEANUP = '{}UVDTF Ornament Cleanup/'.format(ROOT_FOLDER)
UVDTF_ORNAMENT_DIR = '{}UVDTF Ornament/'.format(ROOT_FOLDER)
UVDTF_LOGO_CUP_CARE_DIR_CLEANUP = '{}UVDTF Logo Cup Care Decal Cleanup/'.format(ROOT_FOLDER)
UVDTF_LOGO_CUP_CARE_DIR = '{}UVDTF Logo Cup Care Decal/'.format(ROOT_FOLDER)
UVDTF_LOGO_BOTTOM_SHOT_DIR_CLEANUP = '{}UVDTF Logo Bottom Shot Decal Cleanup/'.format(ROOT_FOLDER)
UVDTF_LOGO_BOTTOM_SHOT_DIR = '{}UVDTF Logo Bottom Shot Decal/'.format(ROOT_FOLDER)
UVDTF_25OZ_DIR_CLEANUP = '{}UVDTF 25oz Cleanup/'.format(ROOT_FOLDER)
UVDTF_25OZ_DIR = '{}UVDTF 25oz/'.format(ROOT_FOLDER)


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
    },
    'UVDTF Ornament': {
        'source': UVDTF_ORNAMENT_DIR_CLEANUP,
        'destination': UVDTF_ORNAMENT_DIR,
    },
    'UVDTF Logo Cup Care Decal': {
        'source': UVDTF_LOGO_CUP_CARE_DIR_CLEANUP,
        'destination': UVDTF_LOGO_CUP_CARE_DIR,
    },
    'UVDTF Logo Bottom Shot Decal': {
        'source': UVDTF_LOGO_BOTTOM_SHOT_DIR_CLEANUP,
        'destination': UVDTF_LOGO_BOTTOM_SHOT_DIR,
    },
    'UVDTF 25oz': {
        'source': UVDTF_25OZ_DIR_CLEANUP,
        'destination': UVDTF_25OZ_DIR,
    },
}
MK_DPI = 950
STD_DPI = 400
TEXT_AREA_HEIGHT = 0.015
SHEET_HEIGHT = 120

All_TYPES = ['DTF', 'UVDTF 16oz', 'UVDTF Decal', 'MK', 'UVDTF 40oz Top', 'UVDTF 40oz Bottom', 'UVDTF Bookmark', 'UVDTF Lid', 'UVDTF Milk Carton', 'MK Tapered', 'UVDTF Ornament', 'Sublimation', 'UVDTF Logo Cup Care Decal', 'UVDTF Logo Bottom Shot Decal', 'UVDTF 25oz']

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
    'UVDTF Ornament Decal': 'UVDTF Ornament',
    'Logo Cup Care Instructions - UVDTF Decal': 'UVDTF Logo Cup Care Decal',
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
    'Sublimation': {
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
    'UVDTF Ornament': {'width': 2.5, 'height': 2.5 },
    'UVDTF Logo Cup Care Decal': {'width': 2.25, 'height': 2.25 },
    'UVDTF Logo Bottom Shot Decal': {'width': 0.50, 'height': 0.50 },
    'UVDTF 25oz': { 'width': 9.3, 'height': 8.0 },
}

CANVAS = {
    'UVDTF Decal': { 'height': 4.0, 'width': 4.0 },
    'UVDTF Ornament': {'width': 2.5, 'height': 2.5 },
    'MK': { 'width': 1.5, 'height': 2.3 },
    'MK Rectangle': {'width': 1.5, 'height': 2.3},
    'MK Tapered': { 'width': 1.75, 'height': 2.6 },
    'UVDTF 40oz Bottom': {'width': 10.3, 'height': 3.58, 'arch': 3},
    'UVDTF Lid': {'width': 2.75, 'height': 2.75 },
    'UVDTF Bookmark': {'width': 5.5, 'height': 1.8 },
    'UVDTF Milk Carton': {'width': 2.2, 'height': 6.1 },
    'Custom 2x2': {'width': 2, 'height': 2 },
    'UVDTF Logo Cup Care Decal': {'width': 2.25, 'height': 2.25 },
    'UVDTF Logo Bottom Shot Decal': {'width': 0.50, 'height': 0.50 },
    'UVDTF 25oz': { 'width': 9.3, 'height': 8.0 },
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
UVDTF_GANG_SHEET_SPACING_MK_TAPERED = {'width': 0.3, 'height': 0.2}
UVDTF_GANG_SHEET_SPACING_ORNAMENT = {'width': 0.3, 'height': 0.3}
UVDTF_GANG_SHEET_SPACING_LOGO_CUP_CARE = {'width': 0.3, 'height': 0.3 }
UVDTF_GANG_SHEET_SPACING_LOGO_BOTTOM_SHOT = {'width': 0.50, 'height': 0.50 }
UVDTF_GANG_SHEET_SPACING_25OZ = {'width': 0.40, 'height': 0.40 }
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
    'MK Tapered': UVDTF_GANG_SHEET_SPACING_MK_TAPERED,
    'UVDTF Ornament': UVDTF_GANG_SHEET_SPACING_ORNAMENT,
    'UVDTF Logo Cup Care Decal': UVDTF_GANG_SHEET_SPACING_LOGO_CUP_CARE,
    'UVDTF Logo Bottom Shot Decal': UVDTF_GANG_SHEET_SPACING_LOGO_BOTTOM_SHOT,
    'UVDTF 25oz': UVDTF_GANG_SHEET_SPACING_25OZ,
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
UVDTF_GANG_SHEET_MAX_HEIGHT_ORNAMENT = 2.5
UVDTF_GANG_SHEET_MAX_HEIGHT_LOGO_CUP_CARE = 2.25
UVDTF_GANG_SHEET_MAX_HEIGHT_LOGO_BOTTOM_SHOT = 0.50
UVDTF_GANG_SHEET_MAX_HEIGHT_25OZ = 8.0
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
    'MK Tapered': UVDTF_GANG_SHEET_MAX_HEIGHT_MK,
    'UVDTF Ornament': UVDTF_GANG_SHEET_MAX_HEIGHT_ORNAMENT,
    'UVDTF Logo Cup Care Decal': UVDTF_GANG_SHEET_MAX_HEIGHT_LOGO_CUP_CARE,
    'UVDTF Logo Bottom Shot Decal': UVDTF_GANG_SHEET_MAX_HEIGHT_LOGO_BOTTOM_SHOT,
    'UVDTF 25oz': UVDTF_GANG_SHEET_MAX_HEIGHT_25OZ,
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

