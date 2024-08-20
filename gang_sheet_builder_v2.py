import cv2, os, math, svgwrite
import numpy as np
from base64 import b64encode
from itertools import combinations, product
from constants import (
    GANG_SHEET_MAX_WIDTH,
    GANG_SHEET_SPACING,
    GANG_SHEET_MAX_ROW,
    GANG_SHEET_MAX_ROW_HEIGHT,
    GANG_SHEET_MAX_HEIGHT,
    STD_DPI
)
from util import (
    inches_to_pixels,
)

def optimize_row(images, max_width, spacing):
    best_row = []
    best_width = 0
    best_height = 0

    # Generate all possible rotation combinations
    rotation_options = list(product([False, True], repeat=len(images)))

    for rotations in rotation_options:
        print("rotation optimiazation")
        rotated_images = [
            (img, height, width) if rotate else (img, width, height)
            for (img, width, height), rotate in zip(images, rotations)
        ]

        for i in range(1, len(rotated_images) + 1):
            for combo in combinations(rotated_images, i):
                width = sum(img[1] for img in combo) + 10 * (len(combo) - 1)
                if width <= max_width:
                    height = max(img[2] for img in combo)
                    if width > best_width or (width == best_width and height < best_height):
                        best_row = list(combo)
                        best_width = width
                        best_height = height

    return best_row, best_width, best_height

def pack_images(images, max_width, max_height, spacing):
    packed = []
    y = 0
    v = 0

    while images and y < max_height:
        row, row_width, row_height = optimize_row(images, max_width, spacing)
        
        if not row:
            break
        h = 0
        x = 0
        print("test in pack images")
        for img, width, height in row:
            packed.append((img, width, height, x, y))
            x += width + 10
            # Remove the original image from the list
            original = next(i for i in images if i[0] is img)
            images.remove(original)
            h += 1
        y += row_height + 10
        v+=1

    return packed, y - 10

def create_image_gang_sheets(input_images, output_prefix, gang_sheet_type, image_type, max_height_inches=GANG_SHEET_MAX_HEIGHT, image_size=None, dpi=STD_DPI):
    max_width_inches = GANG_SHEET_MAX_WIDTH[gang_sheet_type]
    images = []
    spacing = []

    for n in range(len(input_images)):
        png_file = input_images[n]
        print(png_file)
        img = cv2.imread(png_file, cv2.IMREAD_UNCHANGED)
        height, width = img.shape[:2]
        # if image_size != None:
        #     spacing_width_px = inches_to_pixels(GANG_SHEET_SPACING[gang_sheet_type][image_size[n]]['width'], dpi)
        #     spacing_height_px = inches_to_pixels(GANG_SHEET_SPACING[gang_sheet_type][image_size[n]]['height'], dpi)
        # else:
        #     spacing_width_px = inches_to_pixels(GANG_SHEET_SPACING[gang_sheet_type][image_type]['width'], dpi)
        #     spacing_height_px = inches_to_pixels(GANG_SHEET_SPACING[gang_sheet_type][image_type]['height'], dpi)
        images.append((img, width, height))
        # spacing.append((spacing_width_px, spacing_height_px))

    max_width_pixels = int(max_width_inches * dpi)
    max_height_pixels = int(max_height_inches * dpi)

    sheet_num = 0
    while images:
        sheet_num += 1
        packed_images, sheet_height = pack_images(images, max_width_pixels, max_height_pixels, spacing)

        if not packed_images:
            print(f"Warning: Image too large to fit on sheet: {images[0][1]}x{images[0][2]}")
            images.pop(0)
            # spacing.pop(0)
            continue

        # Create SVG
        svg_output_file = f"{output_prefix}_{sheet_num}.svg"
        dwg = svgwrite.Drawing(svg_output_file, profile='tiny')

        # Create PNG
        png_image = np.zeros((sheet_height, max_width_pixels, 4), dtype=np.uint8)

        for img, width, height, x, y in packed_images:
            # Check if the image needs to be rotated
            if img.shape[1] != width or img.shape[0] != height:
                img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)

            # Process for SVG
            if img.shape[2] == 4:
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
            else:
                rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            _, buffer = cv2.imencode('.png', rgb_img)
            img_base64 = b64encode(buffer).decode('utf-8')

            dwg.add(dwg.image(f"data:image/png;base64,{img_base64}",
                              insert=(x, y),
                              size=(width, height)))

            # Process for PNG
            if img.shape[2] == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
            png_image[y:y+height, x:x+width] = img

        # Finalize and save SVG
        dwg['viewBox'] = f"0 0 {max_width_pixels} {sheet_height}"
        width_inches = max_width_pixels / dpi
        height_inches = sheet_height / dpi
        dwg['width'] = f"{width_inches}in"
        dwg['height'] = f"{height_inches}in"
        dwg.save()

        # Save PNG
        png_output_file = f"{output_prefix}_{sheet_num}.png"
        cv2.imwrite(png_output_file, png_image)

        print(f"Created {svg_output_file} and {png_output_file}")
