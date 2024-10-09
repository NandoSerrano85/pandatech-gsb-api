import cv2, os
import numpy as np
from PIL import Image
from app.core.util import (
    inches_to_pixels, 
    rotate_image_90,
    check_image_array,
)
from app.core.constants import (
    SIZING,
    CANVAS,
    STD_DPI,
)

Image.MAX_IMAGE_PIXELS = 933120000
os.environ["OPENCV_LOG_LEVEL"] = "ERROR"

"""
    This function uses PIL to get the DPI information from the orginal image.
"""
def get_dpi_from_pil(image_path):
    with Image.open(image_path) as img:
        dpi = img.info.get('dpi')
        if dpi:
            return dpi[0], dpi[1]  # Return x and y DPI
    return None, None 

"""
    This function creates a canvas and centers the image into the canvas
"""
def fit_image_to_center_canvas(resized_img, new_width_px, new_height_px, target_dpi, image_type, image_size=None):
    canvas_width_px = inches_to_pixels(CANVAS[image_type]['width'], target_dpi)
    canvas_height_px = inches_to_pixels(CANVAS[image_type]['height'], target_dpi)

    background = np.zeros((canvas_height_px, canvas_width_px, 4), dtype=np.uint8)

    # Calculate the position to place the resized image in the center
    x_offset = (canvas_width_px - new_width_px) // 2
    y_offset = (canvas_height_px - new_height_px) // 2
    
    # Copy the resized image onto the transparent background
    background[y_offset:y_offset+new_height_px, x_offset:x_offset+new_width_px] = resized_img

    return background

def get_width_and_height(image, image_path, target_dpi=None):
    # Get current image size in pixels
    height_px, width_px = image.shape[:2]
    
    if target_dpi:
        dpi_x = dpi_y = target_dpi
    else:
        # Try to get DPI information using PIL
        dpi_x, dpi_y = get_dpi_from_pil(image_path)
        
        if dpi_x is None or dpi_y is None:
            dpi_x = dpi_y = 400  # Default to 300 DPI if not found
    
    # Calculate and return current size in inches
    return width_px / dpi_x, height_px / dpi_y

def arch_image(image, image_type, image_size, target_dpi, arch_amount=60):
    # Get image dimensions
    height, width, channels = image.shape
    
    # Calculate new dimensions to accommodate the arch
    new_height = height + arch_amount
    new_width = width
    
    # Create meshgrid for the new dimensions
    x, y = np.meshgrid(np.arange(new_width), np.arange(new_height))
    
    # Calculate the arch
    center_x = new_width / 2
    arch_factor = arch_amount / (center_x ** 2)
    y_offset = arch_factor * (x - center_x) ** 2
    
    # Apply the transformation
    x_mapped = x
    y_mapped = y - y_offset
    
    # Normalize coordinates
    x_mapped = x_mapped / (new_width - 1)
    y_mapped = y_mapped / (height - 1)
    
    # Ensure coordinates are within bounds
    x_mapped = np.clip(x_mapped, 0, 1)
    y_mapped = np.clip(y_mapped, 0, 1)
    
    # Remap the image
    mapped_x = (x_mapped * (width - 1)).astype(np.float32)
    mapped_y = (y_mapped * (height - 1)).astype(np.float32)
    
    # Create a new image with the arched dimensions
    result = cv2.remap(image, mapped_x, mapped_y, cv2.INTER_LINEAR, None, cv2.BORDER_CONSTANT, (0, 0, 0, 0))
    
    return fit_image_to_center_canvas(result, new_width, new_height, target_dpi, image_type, image_size=image_size)

"""
    This function resizes an image based on inches
"""
def resize_image_by_inches(image_path, image_type, image_size=None, image=None, target_dpi=STD_DPI, is_new_mk=False):
    # Read the image
    if check_image_array(image):
        img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    else:
        img = image

    if img.shape[2] == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    current_width_inches, current_height_inches = get_width_and_height(img, image_path, target_dpi)

    if current_width_inches >= current_height_inches:
        current_largest_side_inches = current_width_inches
    else:
        current_largest_side_inches = current_height_inches

    if image_type == 'DTF':
        if image_size in SIZING[image_type]:
            target_largest_side_inches = SIZING[image_type][image_size]['height']
        else:
            raise Exception("Missing Size Value. Please add an image_size value of 'Adult+', 'Adult', 'Youth', 'Toddler' or 'Pocket'.")
    elif image_type == 'UVDTF 40oz Top' or image_type == 'UVDTF 40oz Bottom':
        target_largest_side_inches = SIZING[image_type]['width']
    else:
        if SIZING[image_type]['width'] >= SIZING[image_type]['height']:
            target_largest_side_inches = SIZING[image_type]['width']
        else:
            target_largest_side_inches = SIZING[image_type]['height']

     # Calculate scale factor
    scale_factor = target_largest_side_inches / current_largest_side_inches
    
    if image_type == 'DTF' or image_type == 'UVDTF Decal' or image_type == 'UVDTF Lid' or image_type == 'Custom 2x2':
        # Calculate new dimensions
        new_width_inches = (current_width_inches * scale_factor)
        new_height_inches = (current_height_inches * scale_factor)

         # Calculate new size in pixels based on new dementions inches and DPI
        new_width_px = inches_to_pixels(new_width_inches, target_dpi)
        new_height_px = inches_to_pixels(new_height_inches, target_dpi)
    elif image_type == 'MK' or image_type == 'UVDTF Bookmark' or image_type == 'MK Tapered':
        if current_width_inches < 1:
            image_type = 'MK Rectangle'
        current_width = inches_to_pixels(current_width_inches, target_dpi)
        current_height = inches_to_pixels(current_height_inches, target_dpi)

        target_width = inches_to_pixels(SIZING[image_type]['width'], target_dpi)
        target_height = inches_to_pixels(SIZING[image_type]['height'], target_dpi)

        # Calculate scaling factor
        scale_width = target_width / current_width
        scale_height = target_height / current_height
        scale_factor = min(scale_width, scale_height)

        new_width_px = int(current_width * scale_factor)
        new_height_px = int(current_height * scale_factor)
    else:
        # Calculate new size in pixels based on target inches and DPI
        new_width_px = inches_to_pixels(SIZING[image_type]['width'], target_dpi)
        new_height_px = inches_to_pixels(SIZING[image_type]['height'], target_dpi)

    interpolation = cv2.INTER_CUBIC if scale_factor > 1 else cv2.INTER_AREA 
    
    # Resize the image
    resized_img = cv2.resize(img, (new_width_px, new_height_px), interpolation=interpolation)

    # Fit the resized images into a canvas
    if image_type == 'UVDTF Decal' or image_type == 'UVDTF Bookmark' or image_type == 'UVDTF Lid' or image_type == 'Custom 2x2':
        return fit_image_to_center_canvas(resized_img, new_width_px, new_height_px, target_dpi, image_type)
    elif image_type == 'MK' or image_type == 'MK Tapered' or image_type == 'MK Rectangle':
        if (new_width_px > new_height_px) and is_new_mk:
            rotated_img = rotate_image_90(resized_img)
            return fit_image_to_center_canvas(rotated_img, rotated_img.shape[1], rotated_img.shape[0], target_dpi, image_type)
        else:
            return fit_image_to_center_canvas(resized_img, new_width_px, new_height_px, target_dpi, image_type)
    
    # Check in utils for code on arching still can't get to work properly
    # Arch bottom part of a 40oz cup wrap
    # if image_type == "UVDTF 40oz Bottom":
    #     # pass
    #     resized_img = arch_image(resized_img, image_type, image_size, target_dpi)
        
    return resized_img