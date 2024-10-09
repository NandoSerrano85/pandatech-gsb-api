import numpy as np
import cv2
import csv
import os
import statistics
import concurrent.futures
from functools import partial
import multiprocessing
from math import ceil
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
from app.core.util import inches_to_pixels, rotate_image_90, save_single_image
from app.core.constants import (
    GANG_SHEET_MAX_WIDTH, GANG_SHEET_SPACING, GANG_SHEET_MAX_ROW,
    GANG_SHEET_MAX_ROW_HEIGHT, GANG_SHEET_MAX_HEIGHT, STD_DPI, TEXT_AREA_HEIGHT
)
from app.core.resizing import resize_image_by_inches

os.environ["OPENCV_LOG_LEVEL"] = "ERROR"

@lru_cache(maxsize=None)
def cached_inches_to_pixels(inches, dpi):
    return inches_to_pixels(inches, dpi)

def add_text_to_gang_sheet(gang_sheet, text, width_pixels, max_height, dpi):
    text_height = int(max_height * TEXT_AREA_HEIGHT)
    font = cv2.FONT_HERSHEY_DUPLEX
    font_scale = 6.0 if dpi == STD_DPI else int(6.0 * 2.5)
    text_color = (0, 0, 0, 255)
    font_thickness = max(int(font_scale * 3), 2)
    
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_x = width_pixels // 2 - text_size[0] // 2
    text_y = text_height // 2 + text_size[1] // 2
    
    cv2.putText(gang_sheet, text, (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)
    return gang_sheet, text_height

def process_image(img_path, image_type, image_size, dpi):
    if os.path.exists(img_path):
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            return None
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
        if image_type in ['UVDTF 16oz', 'UVDTF 40oz Top', 'UVDTF Bookmark']:
            img = rotate_image_90(img, 1)
        if image_type == 'DTF':
            img = resize_image_by_inches(img_path, image=img, image_type=image_type, image_size=image_size, target_dpi=dpi)
        return img
    return None

def create_gang_sheets(image_data, image_type, gang_sheet_type, output_path, order_range, total_images, dpi=300, text='Single '):
    # Pre-calculate common values
    width_px = cached_inches_to_pixels(GANG_SHEET_MAX_WIDTH[gang_sheet_type], dpi)
    height_px = cached_inches_to_pixels(GANG_SHEET_MAX_HEIGHT[gang_sheet_type], dpi)

    image_index, part, current_index = 0, 1, 0
    images_not_found = {}
    has_missing = False
    current_image_amount_left = 0

    # Pre-process images in parallel
    with ThreadPoolExecutor() as executor:
        future_to_image = {executor.submit(process_image, image_data['Title'][i], image_type, image_data['Size'][i], dpi): i 
                           for i in range(len(image_data['Title']))}
        processed_images = {i: future.result() for future, i in future_to_image.items()}

    while current_index != len(image_data['Title'])-1:
        gang_sheet = np.zeros((height_px, width_px, 4), dtype=np.uint8)
        gang_sheet[:, :, 3] = 0 
        current_x, current_y = 0, 0
        row_height = 0
        gang_sheet, current_y = add_text_to_gang_sheet(gang_sheet, f"{order_range} {image_type} {text}- part{part}", width_px, height_px, dpi)

        for i in range(image_index, len(image_data['Title'])):
            img = processed_images[i]
            current_index = i
            if image_index != i:
                current_image_amount_left = 0
            if img is not None:
                image_size = image_data['Size'][i]
                spacing_key = image_size if image_type == 'DTF' else image_type
                spacing_width_px = cached_inches_to_pixels(GANG_SHEET_SPACING[gang_sheet_type][spacing_key]['width'], dpi)
                spacing_height_px = cached_inches_to_pixels(GANG_SHEET_SPACING[gang_sheet_type][spacing_key]['height'], dpi)

                img_height, img_width = img.shape[:2]
                for amount_index in range(current_image_amount_left, image_data['Total'][i]):
                    if current_x + img_width > width_px:
                        current_x, current_y = 0, current_y + row_height + spacing_width_px
                        row_height = 0
                    
                    if current_y + img_height + spacing_height_px > height_px:
                        image_index = i
                        current_image_amount_left = amount_index
                        break
                    
                    gang_sheet[current_y:current_y+img_height, current_x:current_x+img_width] = img
                    current_x += img_width + spacing_width_px
                    row_height = max(row_height, img_height)
                
                if current_y + img_height + spacing_height_px > height_px:
                    break
            else:
                has_missing = True
                image_name = os.path.splitext(os.path.basename(image_data['Title'][i]))[0]
                images_not_found[image_name] = {'Total': image_data['Total'][i], 'Size': image_data['Size'][i]}
                image_index = i + 1
                current_image_amount_left = 0
        # Save the gang sheet
        alpha_channel = gang_sheet[:,:,3]
        rows, cols = np.any(alpha_channel, axis=1), np.any(alpha_channel, axis=0)
        if np.any(rows) and np.any(cols):
            ymin, ymax = np.where(rows)[0][[0, -1]]
            xmin, xmax = np.where(cols)[0][[0, -1]]
            cropped_gang_sheet = gang_sheet[ymin:ymax+1, xmin:xmax+1]
            
            scale_factor = STD_DPI / dpi
            new_width, new_height = int((xmax - xmin + 1) * scale_factor), int((ymax - ymin + 1) * scale_factor)
            resized_gang_sheet = cv2.resize(cropped_gang_sheet, (new_width, new_height), interpolation=cv2.INTER_AREA)

            save_single_image(resized_gang_sheet, output_path, f"{order_range} {image_type} {text} part {part}.png")
            part += 1
        else:
            print(f"Warning: Sheet {part} is empty (all transparent). Skipping.")
       
        

    if has_missing:
        with open(f"{output_path}/{image_type}_missing.csv", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Title', 'Total', "Type", "Size"])
            for key, value in images_not_found.items():
                writer.writerow([key, value['Total'], image_type, value['Size']])
        return {'Title': list(images_not_found.keys()), 'Total': [v['Total'] for v in images_not_found.values()], 'Type': [image_type] * len(images_not_found), 'Size': [v['Size'] for v in images_not_found.values()]}
    return None

def create_gang_sheet_kwargs(kwargs):
    return create_gang_sheets(**kwargs)

def process_gang_sheets_concurrently(gang_sheet_params_list, max_workers=None):
    """
    Process multiple gang sheets concurrently using a thread pool.
    
    :param gang_sheet_params_list: A list of dictionaries, each containing parameters for create_gang_sheets
    :param max_workers: The maximum number of worker threads to use. If None, it will default to the number of CPUs.
    :return: A list of results from create_gang_sheets calls
    """
    if max_workers is None:
        max_workers = multiprocessing.cpu_count()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(create_gang_sheet_kwargs, params) for params in gang_sheet_params_list]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    return results