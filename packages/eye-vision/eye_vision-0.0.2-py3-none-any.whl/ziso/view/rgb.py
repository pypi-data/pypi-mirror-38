import cv2
import matplotlib.pyplot as plt
#%matplotlib inline

"""
function to print RGB images
"""
def view(image_or_frame):
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
        raise TypeError ("Error... please check file name or reading the file first") from errors