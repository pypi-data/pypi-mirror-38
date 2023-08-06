import cv2
import matplotlib.pyplot as plt

def gray(image_or_frame):
    # coverting from the opencv default BGR scheme to RGB color format
    RGB_image = cv2.imread(image_or_frame)
    RGB_image = cv2.cvtColor(RGB_image, cv2.COLOR_RGB2GRAY)
    # so as not to have the axis that show the scale of the image(s)
    plt.axis("off")       
    # this is for displaying the image
    plt.imshow(RGB_image) 