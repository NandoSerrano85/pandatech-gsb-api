import numpy as np
import cv2, csv, os, statistics
from math import ceil
from app.core.util import(
    inches_to_pixels,
    rotate_image_90,
    save_single_image
)
from app.core.constants import (
    GANG_SHEET_MAX_WIDTH,
    GANG_SHEET_SPACING,
    GANG_SHEET_MAX_ROW,
    GANG_SHEET_MAX_ROW_HEIGHT,
    GANG_SHEET_MAX_HEIGHT,
    STD_DPI,
    TEXT_AREA_HEIGHT,
)
from app.core.resizing import resize_image_by_inches

os.environ["OPENCV_LOG_LEVEL"] = "ERROR"

def create_gang_sheet_kwargs(kwargs):
    return create_gang_sheets(**kwargs)

def add_text_to_gang_sheet(gang_sheet, text, width_pixels, max_height, dpi):
        # Calculate the space for text 
        text_height = int(max_height * TEXT_AREA_HEIGHT)
        
        # Set up text parameters
        font = cv2.FONT_HERSHEY_DUPLEX  # A sans-serif font
        font_scale = 6.0  if dpi == STD_DPI else int(6.0 * 2.5)# Approximate 18pt font size
        text_color = (0, 0, 0, 255)  # Black color with full opacity
        font_thickness = max(int(font_scale * 3), 2)  # Adjust thickness based on scale
        
        # Calculate text size
        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        
        # Calculate position to center the text horizontally and place it near the top
        text_x = width_pixels //2 - text_size[0] // 2
        text_y = text_height // 2 + text_size[1] // 2
        
        # Put the text on the image
        cv2.putText(gang_sheet, text, (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

        return gang_sheet, text_height

def create_gang_sheets(image_data, image_type, gang_sheet_type, output_path, order_range, total_images, dpi=300, text='Single '):
    if gang_sheet_type == 'UVDTF':
        total_rows = ceil(total_images / GANG_SHEET_MAX_ROW[gang_sheet_type][image_type])
        total_height = (GANG_SHEET_MAX_ROW_HEIGHT[gang_sheet_type][image_type] + GANG_SHEET_SPACING[gang_sheet_type][image_type]['height']) * total_rows + GANG_SHEET_SPACING[gang_sheet_type][image_type]['height']
        total_height_px = inches_to_pixels(total_height, dpi)
        height_px = inches_to_pixels(GANG_SHEET_MAX_HEIGHT, dpi)
    else:
        average_row = statistics.median([ GANG_SHEET_MAX_ROW[gang_sheet_type][size] for size in image_data['Size'] ])
        average_row_height = statistics.median([ GANG_SHEET_MAX_ROW_HEIGHT[gang_sheet_type][size] for size in image_data['Size'] ])
        total_rows = ceil(total_images / average_row)
        total_height = (average_row_height + GANG_SHEET_SPACING[gang_sheet_type]['Adult+']['height']) * total_rows + GANG_SHEET_SPACING[gang_sheet_type]['Adult+']['height']
        total_height_px = inches_to_pixels(total_height, dpi)
        height_px = inches_to_pixels(GANG_SHEET_MAX_HEIGHT, dpi)

    # Clearing variables
    average_row = None
    average_row_height = None
    total_rows = None
    total_height = None

    # Calculate dimensions in pixels
    width_px = inches_to_pixels(GANG_SHEET_MAX_WIDTH[gang_sheet_type], dpi)

    num_sheets = ceil(total_height_px / height_px)
    
    total_height_px = None
    # Load and process images
    image_index = 0
    image_amount = 0
    part = 1
    images_not_found = dict()
    has_missing = False
    for sheet in range(num_sheets):
        unfinished_image = False
        gang_sheet = np.zeros((height_px, width_px, 4), dtype=np.uint8)
        gang_sheet[:, :, 3] = 0 
        current_x, current_y = 0, 0
        row_height = 0
        gang_sheet, current_y = add_text_to_gang_sheet(gang_sheet, "{} {} {}- part{}".format(order_range, image_type, text, sheet+1), width_px, height_px, dpi)

        for i in range(image_index, len(image_data['Title'])):
            img_path = image_data['Title'][i]
            if os.path.exists(img_path):
                img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
                if img.shape[2] == 3:  # If image is BGR, convert to BGRA
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
                if image_type == 'UVDTF 16oz':
                    img = rotate_image_90(img, 1)
                if image_type == 'UVDTF 40oz Top':
                    img = rotate_image_90(img, 1)
                if image_type == 'DTF':
                    img = resize_image_by_inches(img_path, image=img, image_type=image_type, image_size=image_data['Size'][i], target_dpi=dpi)

                image_size = image_data['Size'][i]
                if image_type == 'DTF':
                    spacing_width_px = inches_to_pixels(GANG_SHEET_SPACING[gang_sheet_type][image_size]['width'], dpi)
                    spacing_height_px = inches_to_pixels(GANG_SHEET_SPACING[gang_sheet_type][image_size]['height'], dpi)
                else:
                    spacing_width_px = inches_to_pixels(GANG_SHEET_SPACING[gang_sheet_type][image_type]['width'], dpi)
                    spacing_height_px = inches_to_pixels(GANG_SHEET_SPACING[gang_sheet_type][image_type]['height'], dpi)

                img_height, img_width = img.shape[:2]
                for n in range(image_amount, image_data['Total'][i]):
                    # Check if image fits in the current row
                    if current_x + img_width > width_px:
                        # Move to the next row
                        current_x = 0
                        current_y += row_height + spacing_width_px
                        row_height = 0
                    
                    # Check if image fits in the sheet vertically
                    if current_y + img_height + spacing_height_px > height_px:
                        image_index = i
                        image_amount = n
                        unfinished_image = True
                        break
                    
                    # Place the image
                    gang_sheet[current_y:current_y+img_height, current_x:current_x+img_width] = img
                    
                    # Update position and row height
                    current_x += img_width + spacing_width_px
                    row_height = max(row_height, img_height)
                if unfinished_image:
                    break
                else:
                    image_amount = 0
            else:
                has_missing = True
                image_name = img_path.split('/')[-1].split('.')[0]
                images_not_found[image_name] = {'Total': image_data['Total'][i], 'Size':image_data['Size'][i] }
                image_index = i+1
                image_amount = 0
        alpha = gang_sheet[:, :, 3]
        coords = cv2.findNonZero(alpha)
        
        if coords is not None:
            # Crop empty space
            alpha_channel = gang_sheet[:,:,3]
            rows = np.any(alpha_channel, axis=1)
            cols = np.any(alpha_channel, axis=0)
            ymin, ymax = np.where(rows)[0][[0, -1]]
            xmin, xmax = np.where(cols)[0][[0, -1]]

            cropped_gang_sheet = gang_sheet[ymin:ymax+1, xmin:xmax+1]
            
            # Calculate new dimensions at target DPI
            scale_factor = STD_DPI / dpi
            new_width = int((xmax - xmin + 1) * scale_factor)
            new_height = int((ymax - ymin + 1) * scale_factor)

            resized_gang_sheet = cv2.resize(cropped_gang_sheet, (new_width, new_height), interpolation=cv2.INTER_AREA)

            # Save gangsheet
            save_single_image(resized_gang_sheet, output_path, "{} {} {} part {}.png".format(order_range, image_type, text, part))

            part += 1
            del cropped_gang_sheet
            del resized_gang_sheet

        else:
            print(f"Warning: Sheet {sheet + 1} is empty (all transparent). Skipping.")

    if has_missing:
        missing_dict = { 'Title':[],  'Type':[],  'Size':[], 'Total': []}
        with open("{}/{}_missing.csv".format(output_path, image_type), 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Title', 'Total', "Type", "Size"])  # Write header
            for key, value in images_not_found.items():
                missing_dict['Title'].append(key)
                missing_dict['Total'].append(value['Total'])
                missing_dict['Type'].append(image_type)
                missing_dict['Size'].append(value['Size'])
                writer.writerow([key, value['Total'], image_type, value['Size']])
        return missing_dict
    return None
