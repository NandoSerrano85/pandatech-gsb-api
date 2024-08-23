import cv2, os, struct, zlib, csv
import numpy as np

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from constants import (
    STD_DPI,
    All_TYPES_DICT,
    ROOT_FOLDER,
    PACK_LISTS,
    SIZE_LIST,
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

def select_csv_data_by_type(csv_data, local_path, type=''):
    index_data = []
    selected_data={'Product title':[], 'Type':[], 'Size':[]}

    if type == '':
        for n in range(len(csv_data['Type'])):
            for _ in range(int(csv_data['Total'][n])):
                if csv_data['Type'][n] == "UVDTF 40oz":
                    selected_data['Product title'].append("{}/Top/{}.png".format(local_path, csv_data['Product title'][n]))
                    selected_data['Product title'].append("{}/Bottom/{}.png".format(local_path, csv_data['Product title'][n]))
                else:
                    selected_data['Product title'].append("{}/{}.png".format(local_path, csv_data['Product title'][n]))
                selected_data['Type'].append(csv_data['Type'][n])
                selected_data['Size'].append(csv_data['Size'][n])

        return selected_data
    
    for n in range(len(csv_data['Type'])):
        if csv_data['Type'][n] == type:
            index_data.append(n)
    
    for n in index_data:
        for _ in range(int(csv_data['Total'][n])):
            selected_data['Product title'].append("{}/{}.png".format(local_path, csv_data['Product title'][n]))
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

def get_order_data(orders):
    titles = []
    types = []
    sizes = []
    quantity = []
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
                    if 'Custom' in item['title']:
                        titles.append("{} - {}".format(item['title'], order_dict['order_number']))
                        types.append('Custom')
                        sizes.append(item['variant_title'])
                        quantity.append(item['quantity'])
                        continue
                    item_type = All_TYPES_DICT[item['title'].split('- ')[1].strip()]
                    item_title = "{}{}/{}.png".format(ROOT_FOLDER, item_type, item['title'])
                    if item['variant_title'] in SIZE_LIST:
                        item_size = SIZE_LIST[item['variant_title']]
                        item_quantity = item['quantity']
                    else:
                        item_size = ''
                        item_quantity = item['quantity']*PACK_LISTS[item['variant_title']]
                    for _ in range(item_quantity):
                        if item_type == 'UVDTF 40oz':
                            titles.append("{}{}/Top/{}.png".format(ROOT_FOLDER, item_type, item['title']))
                            types.append('UVDTF 40oz Top')
                            sizes.append('Top')
                            quantity.append(item_quantity)
                            titles.append("{}{}/Bottom/{} (Bottom).png".format(ROOT_FOLDER, item_type, item['title']))
                            types.append('UVDTF 40oz Bottom')
                            sizes.append('Bottom')
                            quantity.append(item_quantity)
                        else:
                            titles.append(item_title)
                            types.append(item_type)
                            sizes.append(item_size)
                            quantity.append(item_quantity)

    return titles, types, sizes, quantity, first_order, last_order