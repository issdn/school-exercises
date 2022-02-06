from PIL import ImageGrab, Image, ImageSequence
from cv2 import cv2
import numpy as np
import pyautogui
import time

# Define variables.
# Spectrum of colour in which objects should be displayed. For max lvl 29 fish circles appear in white.
lower_range = np.array([143, 166, 197])
upper_range = np.array([255, 255, 255])

# Your resolution: width / height.
your_resolution = (1080, 1920)
width = your_resolution[0] * 0.9
height = your_resolution[1] * 0.5
# Window size, x1/beginning, y1/beginning, x2/width, y2/height.
window_size = (100, 200, width, height)

# Time needed for fishing. 21 + 3 for circle to disappear.
fish_time = 24

# Positions of fish.
fish_pos = []


def clear_popups():
    clear_popups.variable = 0

    screen = cv2.cvtColor(np.array(ImageGrab.grab(bbox=window_size)), cv2.COLOR_BGR2RGB)
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    template = cv2.imread("popout.jpg", 0)
    
    threshold = 0.9
    
    res = cv2.matchTemplate(screen_gray,template,cv2.TM_CCOEFF_NORMED)

    loc = np.where( res >= threshold)
    
    for pt in zip(*loc[::-1]):
        pyautogui.click(x = ( pt[0] + 130 ),
                        y = ( pt[1] + 203 ))
        print("Popup cleared")
        clear_popups.variable = 1

def set_positions():
    screen = cv2.cvtColor(np.array(ImageGrab.grab(bbox=window_size)), cv2.COLOR_BGR2RGB)
    # Show only objects with specified color, in this example white, other kinds of fish can be added later.
    mask = cv2.inRange(screen, lower_range, upper_range)
    
    # Thicken the pixels so it's easier to for HoughCircles to distinguish needed ones. And add blur so it doesn't catch random circles from left-over pixels.
    kernel = np.ones((4,4),np.uint8)
    mask = cv2.dilate(mask, kernel, iterations = 1)

    # Use HoughCircles to look for circles.
    circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1, 1, param1=30, param2=15,minRadius=0,maxRadius=28)
    if circles is not None:
        circles_round = np.uint16(np.around(circles))
        for i in circles_round[0, :]:

            center = (i[0], i[1])
            radius = i[2]

            mask = cv2.circle(mask, center, radius, (255, 0, 255), 1)
            
            # Append list of positions that will go to click_on_fish()
            fish_pos.append([(i[0]+100), (i[1]+200)])

    

def click_on_fish(positions):
        try:
            pyautogui.click(x=(positions[0][0]),
                            y=(positions[0][1]),
                            clicks=2)

            # Wait for potential popups and then clear them.
            time.sleep(2)
            clear_popups()

            # If there was a popup, no fish is being fished so don't need to wait for it.
            if clear_popups.variable != 1:
                time.sleep(fish_time)
        
        except:
            pass

            
# Bot loop
while True:
    fish_pos.clear()

    time.sleep(1)

    clear_popups()

    set_positions()

    click_on_fish(fish_pos)



