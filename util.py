import cv2, os, struct, zlib, csv
import numpy as np
from PIL import Image
# from libtiff import TIFF

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from constants import (
    STD_DPI,
)
# from googleapiclient.discovery import build
# from oauth2client.service_account import ServiceAccountCredentials
# from google.oauth2.service_account import Credentials
# from googleapiclient.discovery import build

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

    # for n in range(len(csv_data['Total'])):
    #     print(isinstance(csv_data['Total'][n], str))
    #     try:
    #         csv_data['Total'][n] = int(csv_data['Total'][n])
    #     except ValueError:
    #         csv_data['Total'][n] = 0

    #     # print(isinstance(csv_data['Total'][n], int))
    
    # # csv_data = dict(sorted(csv_data.items(), key=lambda item: item[1]['Total']))
    
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

# Not Test!!!!!!!
# def embed_png_in_svg(png_path, svg_path, width, height):
#     # Read the PNG file
#     with open(png_path, "rb") as png_file:
#         png_data = png_file.read()
    
#     # Encode the PNG data to base64
#     png_base64 = base64.b64encode(png_data).decode('utf-8')
    
#     # Create an SVG drawing
#     dwg = svgwrite.Drawing(svg_path, size=(width, height))
    
#     # Add the PNG as an image to the SVG
#     dwg.add(dwg.image(f"data:image/png;base64,{png_base64}",
#                       insert=(0, 0),
#                       size=(width, height)))
    
#     # Save the SVG file
#     dwg.save()

# # Usage
# embed_png_in_svg('input_image.png', 'output_image.svg', 300, 200)


# MISSING TO CREATE A SERVICE ACCOUNT WITH CREDENTIALS
# def read_google_sheet(sheet_id, range_name):
#     # Set up credentials
#     creds = Credentials.from_service_account_file('path/to/your/service_account_key.json', 
#                                                   scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    
#     # Build the Sheets API service
#     service = build('sheets', 'v4', credentials=creds)
    
#     # Call the Sheets API to get the data
#     sheet = service.spreadsheets()
#     result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    
#     # Get the data from the result
#     data = result.get('values', [])
    
#     # Convert to dictionary
#     if not data:
#         return {}
    
#     headers = data[0]
#     result_dict = {}
    
#     for row in data[1:]:
#         for i, value in enumerate(row):
#             if i < len(headers):
#                 if headers[i] not in result_dict:
#                     result_dict[headers[i]] = []
#                 result_dict[headers[i]].append(value)
    
#     return result_dict


# Arch bottom part of a 40oz cup wrap
# def arch_image():

#         # # Ensure the image has an alpha channel
#         # if img.shape[2] == 3:
#         #     img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)

#         height, width = resized_img.shape[:2]
    
#         # Create mappings for x and y coordinates
#         map_x = np.zeros((height, width), dtype=np.float32)
#         map_y = np.zeros((height, width), dtype=np.float32)

#         # Calculate the radius of the arc
#         bend_radians = np.radians(canvas[image_type][image_size]['arch'] * 1.8)  # Convert percentage to radians
#         radius = height / bend_radians if bend_radians > 0 else float('inf')
        
#         # Calculate center of the arc
#         center_y = height + radius
        
#         for y in range(height):
#             for x in range(width):
#                 # Normalize coordinates
#                 norm_y = y / height
#                 norm_x = x / width - 0.5
                
#                 # Calculate angle for this point
#                 angle = norm_y * bend_radians
                
#                 # Calculate new positions
#                 new_y = np.sin(angle) * radius
#                 new_x = norm_x * (radius - new_y)
                
#                 # Convert back to pixel coordinates
#                 map_y[y, x] = center_y - radius + new_y
#                 map_x[y, x] = (new_x / radius + 0.5) * width
        
#         # for y in range(height):
#         #     for x in range(width):
#         #         # Calculate new x position (slight curve to maintain image width)
#         #         normalized_x = x / (width - 1) - 0.5
#         #         new_x = x + canvas[image_type][image_size]['arch'] * height * 0.1 * normalized_x
#         #         map_x[y, x] = new_x
                
#         #         # Calculate new y position
#         #         normalized_y = y / (height - 1)
                
#         #         # Apply sine curve for smooth arch effect
#         #         offset = np.sin(np.pi * normalized_x) * canvas[image_type][image_size]['arch'] * height
                
#         #         new_y = y - offset * (1 - normalized_y)
#         #         map_y[y, x] = new_y
    

#                 # # Calculate new x position (no change for x in this case)
#                 # map_x[y, x] = x
                
#                 # # Calculate new y position
#                 # normalized_x = x / (width - 1) - 0.5
#                 # normalized_y = y / (height - 1)
                
#                 # # Apply quadratic curve for arch effect
#                 # offset = canvas[image_type][image_size]['arch'] * (normalized_x ** 2)
                
#                 # new_y = (normalized_y + offset) * height
#                 # map_y[y, x] = new_y
        
#         # Apply the mapping to create the arch effect
#         img_arched = cv2.remap(resized_img, map_x, map_y, cv2.INTER_LINEAR, borderMode=cv2.BORDER_TRANSPARENT, borderValue=(0, 0, 0, 0))

#         # # Create a mask for the valid (non-transparent) pixels
#         # mask = img_arched[:,:,3] > 0

#         # # Create a fully transparent image
#         # result = np.zeros((height, width, 4), dtype=np.uint8)
        
#         # # Copy only the valid pixels to the result
#         # result[mask] = img_arched[mask]
        
#         return img_arched
#         # return fit_image_to_center_canvas(img_arched, img_arched.shape[1], img_arched.shape[0], target_dpi, image_type, image_size)

# def connection_gcp():
#     scope = ['https://www.googleapis.com/auth/drive.readonly']

#     credentials = ServiceAccountCredentials.from_json_keyfile_name('service_account_key.json', scope)

#     # https://developers.google.com/drive/api/v3/quickstart/python
#     service = build('drive', 'v3', credentials=credentials)

#     # Call the Drive v3 API
#     results = service.files().list(
#         fields="*",corpora = 'drive',supportsAllDrives = True, driveId = "YOUR_DRIVE_ID", includeItemsFromAllDrives = True).execute()
#     items = results.get('files', [])

#     if not items:
#         print('No files found.')
#     else:
#         print('Files:')
#         for item in items:
#             print(u'{0} ({1})'.format(item['name'], item['id']))


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