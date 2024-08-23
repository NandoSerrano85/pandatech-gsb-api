import cv2
import numpy as np

def mockup_image_creator(background, foreground, x_offset=0, y_offset=0):
    # Convert images to float32 for calculations
    bg = background.astype(float)
    fg = foreground.astype(float)

    # Get the overlapping region
    h, w = fg.shape[:2]
    overlap = bg[y_offset:y_offset+h, x_offset:x_offset+w]

    # If foreground has an alpha channel, use it for blending
    if fg.shape[2] == 4:
        alpha = fg[:, :, 3] / 255.0
        alpha = np.expand_dims(alpha, axis=-1)
        
        # Blend the images
        blended = alpha * fg[:, :, :3] + (1 - alpha) * overlap
        
        # Put the blended region back into the background
        bg[y_offset:y_offset+h, x_offset:x_offset+w] = blended
    else:
        # If no alpha channel, just overlay the foreground
        bg[y_offset:y_offset+h, x_offset:x_offset+w] = fg

    return bg.astype(np.uint8)

# Load images
background = cv2.imread('background.png')
foreground = cv2.imread('foreground.png', cv2.IMREAD_UNCHANGED)  # Keep alpha channel if present

# Layer the images
result = mockup_image_creator(background, foreground, x_offset=100, y_offset=50)

# Save or display the result
cv2.imwrite('layered_image.png', result)
cv2.imshow('Layered Image', result)
cv2.waitKey(0)
cv2.destroyAllWindows()