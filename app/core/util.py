import cv2, os, struct, zlib, csv
import numpy as np
from pprint import pprint

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from app.core.constants import (
    STD_DPI,
    MK_DPI,
    All_TYPES_DICT,
    ROOT_FOLDER,
    PACK_LISTS,
    SIZE_LIST,
    All_TYPES,
    DTF_MAX_SIZE,
    ALLOWED_EXTENSIONS,
)

def inches_to_pixels(inches, dpi):
    return int(round(inches * dpi))

def rotate_image_90(image, rotations=1):
    """
    Rotate an image by 90 degrees clockwise.
    
    :param image: Input image
    :param rotations: Number of 90 degree rotations. Positive for clockwise, negative for counterclockwise.
    :return: Rotated image
    """
    # Ensure rotations is between -3 and 3
    rotations = rotations % 4
    
    if rotations == 0:
        return image
    elif rotations == 1:
        return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif rotations == 2:
        return cv2.rotate(image, cv2.ROTATE_180)
    else:  # rotations == 3 or -1
        return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
def create_folder(folder_path):
    try:
        os.makedirs(folder_path)
        print(f"Folder created successfully: {folder_path}")
    except FileExistsError:
        print(f"Folder already exists: {folder_path}")
    except PermissionError:
        print(f"Permission denied: Unable to create folder {folder_path}")
    except Exception as e:
        print(f"An error occurred while creating the folder: {e}")

def find_png_files(folder_path):
    # Ensure the path ends with a slash
    folder_path = os.path.join(folder_path, '')
    
    png_filepath = []
    png_filenames = []

    # Walks through dirtectory searchjing for PNG files and adds path to png_filepath
    for root, dirs, files in os.walk(folder_path):
        png_filepath.extend([os.path.join(root, file) for file in files if file.lower().endswith('.png')])
        png_filenames.extend([file for file in files if file.lower().endswith('.png')])
    
    return png_filepath, png_filenames

def save_single_image(image, folder_path, filename, target_dpi=(STD_DPI,STD_DPI)):

    output_path = os.path.join(folder_path, filename)

    cv2.imwrite(output_path, image)

    retval, buffer = cv2.imencode(".png", image)
    s = buffer.tostring()

    # Find start of IDAT chunk
    IDAToffset = s.find(b'IDAT') - 4

    pHYs = b'pHYs' + struct.pack('!IIc',int(target_dpi[0]/0.0254),int(target_dpi[1]/0.0254),b"\x01" ) 
    pHYs = struct.pack('!I',9) + pHYs + struct.pack('!I',zlib.crc32(pHYs))

    with open(output_path, "wb") as out:
        out.write(buffer[0:IDAToffset])
        out.write(pHYs)
        out.write(buffer[IDAToffset:])

def read_local_csv(file_path):
    result_dict = {}
    
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)  # Read the first row as headers
        
        for header in headers:
            result_dict[header] = []
        
        for row in reader:
            for i, value in enumerate(row):
                if i < len(headers):
                    result_dict[headers[i]].append(value)
    
    return result_dict
def find_index(lst, element):
    try:
        return lst.index(element)
    except ValueError:
        return -1 

def sort_csv_data_by_type_optimized(csv_data, path, type):
    index_data = []
    data = dict()
    total = 0
    local_type = None

    if type == "UVDTF 40oz Top" or type == "UVDTF 40oz Bottom":
        local_type = "UVDTF 40oz"
    else:
         local_type = type
    
    local_path = "{}{}".format(path, local_type)

    for n in range(len(csv_data['Type'])):
        if csv_data['Type'][n] == local_type:
            index_data.append(n)

    if local_type == "UVDTF 40oz":
        data["UVDTF 40oz Top"] = {'Title':[], 'Size':[], 'Total':[]}
        data["UVDTF 40oz Bottom"] = {'Title':[], 'Size':[], 'Total':[]}
    else:
        data[type] = {'Title':[], 'Size':[], 'Total':[]}

    for n in index_data:
        title_total = int(csv_data['Total'][n]) if type != 'UVDTF Milk Carton' else int(csv_data['Total'][n]) * 4
        if local_type == "UVDTF 40oz":
            title_top = "{}/Top/{}.png".format(local_path, csv_data['Product title'][n])
            title_bottom = "{}/Bottom/{} (Bottom).png".format(local_path, csv_data['Product title'][n])
            i_top = find_index(data["UVDTF 40oz Top"]['Title'], title_top)
            i_bottom = find_index(data["UVDTF 40oz Bottom"]['Title'], title_bottom)

            if i_top < 0 and i_bottom < 0:
                data["UVDTF 40oz Top"]['Title'].append(title_top)
                data["UVDTF 40oz Top"]['Size'].append('Top')
                data["UVDTF 40oz Top"]['Total'].append(title_total)
                data["UVDTF 40oz Bottom"]['Title'].append(title_bottom)
                data["UVDTF 40oz Bottom"]['Size'].append('Bottom')
                data["UVDTF 40oz Bottom"]['Total'].append(title_total)
            else:
                data["UVDTF 40oz Top"]['Total'][i_top] += title_total
                data["UVDTF 40oz Bottom"]['Total'][i_bottom] += title_total

        else:
            title = "{}/{}.png".format(local_path, csv_data['Product title'][n])
            i = find_index(data[type]['Title'], title)
            if i < 0:
                data[type]['Title'].append(title)
                data[type]['Size'].append(csv_data['Size'][n])
                data[type]['Total'].append(title_total)
            else:
                if csv_data['Size'][n] == data[type]['Size'][i]:
                    data[type]['Total'][i] += title_total
                else:
                    data[type]['Title'].append(title)
                    data[type]['Size'].append(csv_data['Size'][n])
                    data[type]['Total'].append(title_total)
        total += title_total

    data['Type Total'] = total
    return data

def select_csv_data_by_type(csv_data, local_path, type=''):
    index_data = []
    selected_data={'Title':[], 'Type':[], 'Size':[]}

    if type == '':
        for n in range(len(csv_data['Type'])):
            for _ in range(int(csv_data['Total'][n])):
                if csv_data['Type'][n] == "UVDTF 40oz":
                    selected_data['Title'].append("{}/Top/{}.png".format(local_path, csv_data['Product title'][n]))
                    selected_data['Type'].append('UVDTF 40oz Top')
                    selected_data['Size'].append('Top')
                    selected_data['Title'].append("{}/Bottom/{} (Bottom).png".format(local_path, csv_data['Product title'][n]))
                    selected_data['Type'].append('UVDTF 40oz Bottom')
                    selected_data['Size'].append('Bottom')
                else:
                    selected_data['Title'].append("{}/{}.png".format(local_path, csv_data['Product title'][n]))
                    selected_data['Type'].append(csv_data['Type'][n])
                    selected_data['Size'].append(csv_data['Size'][n])

        return selected_data
    
    for n in range(len(csv_data['Type'])):
        if csv_data['Type'][n] == type:
            index_data.append(n)
    
    for n in index_data:
        for _ in range(int(csv_data['Total'][n])):
            if csv_data['Type'][n] == "UVDTF 40oz":
                selected_data['Title'].append("{}/Top/{}.png".format(local_path, csv_data['Product title'][n]))
                selected_data['Type'].append('UVDTF 40oz Top')
                selected_data['Size'].append('Top')
                selected_data['Title'].append("{}/Bottom/{} (Bottom).png".format(local_path, csv_data['Product title'][n]))
                selected_data['Type'].append('UVDTF 40oz Bottom')
                selected_data['Size'].append('Bottom')
            else:
                selected_data['Title'].append("{}/{}.png".format(local_path, csv_data['Product title'][n]))
                selected_data['Type'].append(csv_data['Type'][n])
                selected_data['Size'].append(csv_data['Size'][n])
    return selected_data

def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def connection_gcp():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()

    drive = GoogleDrive(gauth)

    file_list = drive.ListFile({'q': "'root' in parents"}).GetList()
    for file1 in file_list:
        print('title: %s, id: %s' % (file1['title'], file1['id']))

def check_image_array(image_array):
    if image_array is None or len(image_array) == 0:
        return True
    
    for img in image_array:
        if img is None or not isinstance(img, np.ndarray):
            return True
    
    return False

def png_to_cmyk_tiff(input_path, output_path):
    # Read the PNG image with alpha channel
    image_bgra = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    
    # Separate the color channels and alpha
    b, g, r, a = cv2.split(image_bgra)
    
    # Merge BGR channels
    image_bgr = cv2.merge([b, g, r])
    
    # Normalize BGR values
    image_bgr_float = image_bgr.astype(np.float32) / 255.0
    
    # Calculate CMYK
    k = 1 - np.max(image_bgr_float, axis=2)
    c = (1 - image_bgr_float[:,:,2] - k) / (1 - k + 1e-8)
    m = (1 - image_bgr_float[:,:,1] - k) / (1 - k + 1e-8)
    y = (1 - image_bgr_float[:,:,0] - k) / (1 - k + 1e-8)
    
    # Scale to 0-255 range and convert to uint8
    c = (c * 255).astype(np.uint8)
    m = (m * 255).astype(np.uint8)
    y = (y * 255).astype(np.uint8)
    k = (k * 255).astype(np.uint8)
    
    # Create a 5-channel image (CMYK + Alpha)
    cmyk_alpha = np.dstack((c, m, y, k, a))
    
    tif = TIFF.open(output_path, mode='w')
    # Save as TIFF
    tif.write_image(cmyk_alpha)
    # success = cv2.imwrite(output_path, cmyk_alpha)
    
    # if success:
    #     print(f"CMYK TIFF with transparency saved to {output_path}")
    # else:
    #     print("Failed to save the image")

def get_order_data(orders, data):
    is_first = True
    first_order = None
    last_order = None

    for order in orders:
        order_dict = order.to_dict()
        last_order = order_dict['order_number']
        if is_first:
            is_first = False
            first_order = order_dict['order_number']
        if order_dict['fulfillment_status'] == None:
            line_items = order_dict['line_items']
            for item in line_items:
                if item['fulfillment_status'] == None and item['title'] != 'Shipping Protection by Route':
                    item_type = item['title'].split('- ')
                    if len(item_type) < 2:
                        item_type = item_type[0].strip()
                    else:
                        item_type = item_type[1].strip()
                    
                    if 'Custom' in item['title'] or item_type not in All_TYPES_DICT:
                        item_title = "{} - {}".format(item['title'], order_dict['order_number'])
                        data['Custom']['Title'].append(item_title)
                        data['Custom']['Total'].append(item['quantity'])
                        data['Custom']['Size'].append(item['variant_title'])
                        continue
                    item_type = All_TYPES_DICT[item_type]
                    item_title = "{}{}/{}.png".format(ROOT_FOLDER, item_type, item['title'])
                    if item['variant_title'] in SIZE_LIST:
                        item_size = SIZE_LIST[item['variant_title']]
                        item_quantity = item['quantity']
                    else:
                        item_size = ''
                        variant_title = item['variant_title'] if item['variant_title'] != None else 'Default title'
                        item_quantity = item['quantity']*PACK_LISTS[variant_title]

                    if item_type == 'UVDTF 40oz':
                        item_title_top = "{}{}/Top/{}.png".format(ROOT_FOLDER, item_type, item['title'])
                        item_title_bottom = "{}{}/Bottom/{} (Bottom).png".format(ROOT_FOLDER, item_type, item['title'])
                        i_top = find_index(data["UVDTF 40oz Top"]['Title'], item_title_top)
                        i_bottom = find_index(data["UVDTF 40oz Bottom"]['Title'], item_title_bottom)
                        if i_top < 0 and i_bottom < 0:
                            data['UVDTF 40oz Top']['Title'].append(item_title_top)
                            data['UVDTF 40oz Top']['Total'].append(item_quantity)
                            data['UVDTF 40oz Top']['Size'].append('Top')
                            data['UVDTF 40oz Bottom']['Title'].append(item_title_bottom)
                            data['UVDTF 40oz Bottom']['Total'].append(item_quantity)
                            data['UVDTF 40oz Bottom']['Size'].append('Bottom')
                        else:
                            data["UVDTF 40oz Top"]['Total'][i_top] += item_quantity
                            data["UVDTF 40oz Bottom"]['Total'][i_bottom] += item_quantity
                        data['UVDTF 40oz Top']['Type Total'] += item_quantity
                        data['UVDTF 40oz Bottom']['Type Total'] += item_quantity   
                    else:
                        i = find_index(data[type]['Title'], item_title)
                        if i < 0:
                            data[item_type]['Title'].append(item_title)
                            data[item_type]['Size'].append(item_size)
                            data[item_type]['Total'].append(item_quantity)
                        else:
                            if item_size == data[type]['Size'][i]:
                                data[item_type]['Total'][i] += item_quantity
                            else:
                                data[item_type]['Title'].append(item_title)
                                data[item_type]['Size'].append(item_size)
                                data[item_type]['Total'].append(item_quantity)
                        data[item_type]['Type Total'] += item_quantity

    return first_order, last_order

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS