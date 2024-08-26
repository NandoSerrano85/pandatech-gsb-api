import numpy as np
import cv2, csv, os, statistics, svgwrite
from math import ceil
from app.core.util import(
    inches_to_pixels,
    rotate_image_90,
    print_progress_bar,
    save_single_image
)
from app.core.constants import (
    GANG_SHEET_MAX_WIDTH,
    GANG_SHEET_SPACING,
    GANG_SHEET_MAX_ROW,
    GANG_SHEET_MAX_ROW_HEIGHT,
    GANG_SHEET_MAX_HEIGHT,
    STD_DPI,
    SIZING,
    TEXT_AREA_HEIGHT,
    MISSING_TABLE_DATA,
)
from app.core.resizing import resize_image_by_inches
from base64 import b64encode
from pprint import pprint

os.environ["OPENCV_LOG_LEVEL"] = "ERROR"

def create_gang_sheet_kwargs(kwargs):
    return create_gang_sheet(**kwargs)

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

def create_gang_sheet(input_images, image_type, gang_sheet_type, output_path, order_range, image_size=None, dpi=300, text='Single '):
    if gang_sheet_type == 'UVDTF':
        total_rows = ceil(len(input_images) / GANG_SHEET_MAX_ROW[gang_sheet_type][image_type])
        total_height = (GANG_SHEET_MAX_ROW_HEIGHT[gang_sheet_type][image_type] + GANG_SHEET_SPACING[gang_sheet_type][image_type]['height']) * total_rows + GANG_SHEET_SPACING[gang_sheet_type][image_type]['height']
        total_height_px = inches_to_pixels(total_height, dpi)
        height_px = inches_to_pixels(GANG_SHEET_MAX_HEIGHT, dpi)
    else:
        average_row = statistics.median([ GANG_SHEET_MAX_ROW[gang_sheet_type][size] for size in image_size ])
        average_row_height = statistics.median([ GANG_SHEET_MAX_ROW_HEIGHT[gang_sheet_type][size] for size in image_size ])
        total_rows = ceil(len(input_images) / average_row)
        total_height = (average_row_height + GANG_SHEET_SPACING[gang_sheet_type]['Adult+']['height']) * total_rows + GANG_SHEET_SPACING[gang_sheet_type]['Adult+']['height']
        total_height_px = inches_to_pixels(total_height, dpi)
        height_px = inches_to_pixels(GANG_SHEET_MAX_HEIGHT, dpi)
    # Calculate dimensions in pixels
    width_px = inches_to_pixels(GANG_SHEET_MAX_WIDTH[gang_sheet_type], dpi)

    num_sheets = ceil(total_height_px / height_px)
    
    # Load and process images
    images = []
    images_not_found = dict()
    has_missing = False
    i = 0
    progress = 0
    while i < len(input_images):
        img_path = input_images[i]
        if os.path.exists(img_path):
            img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
            if img.shape[2] == 3:  # If image is BGR, convert to BGRA
                img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
            if image_type == 'UVDTF 16oz':
                img = rotate_image_90(img, 1)
            if image_type == 'UVDTF 40oz Top':
                img = rotate_image_90(img, 1)
            if image_type == 'DTF':
                img = resize_image_by_inches(img_path, image=img, image_type=image_type, image_size=image_size[i], target_dpi=dpi)
            images.append(img)
            i += 1
        else:
            has_missing = True
            image_name = img_path.split('/')[-1].split('.')[0]
            if image_name not in images_not_found:
                if image_size != None:
                    images_not_found[image_name] = {'Total': 1, 'Size':image_size[i] }
                else:
                    images_not_found[image_name] = {'Total': 1, 'Size':None }
            else:
                images_not_found[image_name]['Total'] += 1
            input_images.pop(i)
            if image_size:
                image_size.pop(i)
        progress += 1
    
    if not images:
        print("Error: No valid images provided")
        return False
    
    # Place images on the gang sheet   
    gang_sheets_png = []
    gang_sheets_svg = []
    image_index = 0

    for sheet in range(num_sheets):
        # Create a blank gang sheet np.zeros((height_px, width_px, 4), dtype=np.uint8)
        svg_output_file = "{}{} {} {}part{}.svg".format(output_path, order_range, image_type, text, sheet+1)
        dwg = svgwrite.Drawing(svg_output_file)
        gang_sheet = np.zeros((height_px, width_px, 4), dtype=np.uint8)
        gang_sheet[:, :, 3] = 0 
        current_x, current_y = 0, 0
        row_height = 0
        gang_sheet, current_y = add_text_to_gang_sheet(gang_sheet, "{} {} {}- part{}".format(order_range, image_type, text, sheet+1), width_px, height_px, dpi)
        for n in range(image_index, len(images)):
            if image_size != None:
                spacing_width_px = inches_to_pixels(GANG_SHEET_SPACING[gang_sheet_type][image_size[n]]['width'], dpi)
                spacing_height_px = inches_to_pixels(GANG_SHEET_SPACING[gang_sheet_type][image_size[n]]['height'], dpi)
            else:
                spacing_width_px = inches_to_pixels(GANG_SHEET_SPACING[gang_sheet_type][image_type]['width'], dpi)
                spacing_height_px = inches_to_pixels(GANG_SHEET_SPACING[gang_sheet_type][image_type]['height'], dpi)

            img = images[n]
            img_height, img_width = img.shape[:2]

            
            # Check if image fits in the current row
            if current_x + img_width > width_px:
                # Move to the next row
                current_x = 0
                current_y += row_height + spacing_width_px
                row_height = 0
            
            # Check if image fits in the sheet vertically
            if current_y + img_height + spacing_height_px > height_px:
                image_index = n
                break
            
            # Place the image
            gang_sheet[current_y:current_y+img_height, current_x:current_x+img_width] = img

            # Place the image onto SVG
            # _, buffer = cv2.imencode('.png', img)
            # img_base64 = b64encode(buffer).decode('utf-8')

            # dwg.add(dwg.image(f"data:image/png;base64,{img_base64}",
            #                   insert=(current_x, current_y),
            #                   size=(img_width+spacing_width_px, img_height+spacing_height_px)))
            
            # Update position and row height
            current_x += img_width + spacing_width_px
            row_height = max(row_height, img_height)

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
            gang_sheets_png.append(resized_gang_sheet)

            # Clean up for SVG
            # dwg['viewBox'] = f"0 0 {new_width} {new_height}"
            # width_inches = new_width / dpi
            # height_inches = new_height / dpi
            # dwg['width'] = f"{width_inches}in"
            # dwg['height'] = f"{height_inches}in"
            gang_sheets_svg.append(dwg)
        else:
            print(f"Warning: Sheet {sheet + 1} is empty (all transparent). Skipping.")

    # Save the gang sheet
    for n in range(len(gang_sheets_png)):
        save_single_image(gang_sheets_png[n], output_path, "{} {} {} part{}.png".format(order_range, image_type, text, n+1))
        # Create SVG
        # gang_sheets_svg[n].save()

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
