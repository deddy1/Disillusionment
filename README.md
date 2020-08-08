# Abstract:
This project uses OpenCV and Python to render a user invisible.

# Methodology:
There is a three step process to accomplishing the objective
1. **Choose a blocking color**. The program will read a live video stream from the computer's default webcam. Place the green screen in the picture and press 'c'. The program will capture an image and open it in another window. Click and drag a rectangle completely inside the color to block. The max and min color values will be sent to the main script.
2. **Choose a background**. Next, press space bar to capture the background image. For best results, place the computer/webcam somewhere secure, and take the background picture without you in it. The critical part is that you do not move the webcam after capturing the background image.
3. **Mask and combine images**. The color boundary determined in step 1 sets an upper and lower bound for which to block out colors. The background image will be shown everywhere that color is found.
