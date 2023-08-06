import cv2
import matplotlib.pyplot as plt

"""
function to view non grayscale images
"""
def im(image_or_frame):
    """
    The try block below will 'try' to read an image/frame
    it uses OpenCV which takes in image data at a default of BGR
    we convert it to RGB to be compatible with modern libraries
    """
    try:
        # so as not to have the axis that show the scale of the image(s)
        plt.axis("off")       
        # this is for displaying the image
        plt.imshow(image_or_frame) 
        plt.show()
    except Exception as errors:
        raise TypeError ("Error... please check file name or read the file first") from errors
        pass

    """
    function to view grayscale images
    """
def gray(image_or_frame):
    """
    The try block below will 'try' to read an image/frame
    it uses OpenCV which takes in image data at a default of BGR
    we convert it to RGB to be compatible with modern libraries
    """
    try:
        image_or_frame = cv2.cvtColor(image_or_frame, cv2.COLOR_BGR2GRAY)
        # so as not to have the axis that show the scale of the image(s)
        plt.axis("off")       
        # this is for displaying the image
        plt.imshow(image_or_frame, cmap="gray") 
        plt.show()
    except Exception as errors:
        raise TypeError ("Error... please check file name or read the file first") from errors
        pass