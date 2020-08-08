
# Imports
import cv2
import numpy as np
import wx
import get_color

have_block_color = False
compare_background = False
lower_block = np.array([0, 0, 0])
upper_block = np.array([255, 255, 255])

def overlay_images(foreground, background):
    # Create a mask that filters out the selected color spectrum
    mask = cv2.inRange(img, lower_block, upper_block)
    # Remove (set to 0 intensity, aka black) the pixels that are in the mask
    img[mask != 0] = [0, 0, 0]
    # Remove the pixels that are not in the mask
    background[mask == 0] = [0, 0, 0]
    # Combine the images
    final_img = background + img
    return final_img

# Capture video from webcam. 
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
# Capture background image from file
background = cv2.imread('opencv_background_frame.png')

while True:
    # Read the frame
    _, img = cap.read()
    # Flip horizontally
    img = cv2.flip(img, 1)
    # Do the stuff
    if (compare_background and have_block_color):
        final_img = overlay_images(img, background.copy())
    elif have_block_color:
        k = cv2.waitKey(1)
        if k%256 == 32:
            # SPACE pressed
            img_name = 'opencv_background_frame.png'
            cv2.imwrite(img_name, img)
            print("{} written!".format(img_name))
            compare_background = True
            # Capture background image from file
            background = cv2.imread('opencv_background_frame.png')
        final_img = img
    else:
        k = cv2.waitKey(1)
        if k%256 == ord('c'):
            # 'c' pressed
            img_name = 'opencv_color_frame.png'
            cv2.imwrite(img_name, img)
            have_block_color = True
            print("{} written!".format(img_name))
            # Show frame to pick color
            app = wx.App()
            frame = get_color.mainFrame(img)
            frame.Show()
            app.MainLoop()
            lower_block = frame.lower_bound
            upper_block = frame.upper_bound
        final_img = img
            
    
    # Display
    cv2.imshow('img', final_img)
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
# Release the VideoCapture object
cap.release()
