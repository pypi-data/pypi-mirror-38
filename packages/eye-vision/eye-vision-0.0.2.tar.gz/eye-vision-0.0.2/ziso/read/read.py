import cv2
"""
module to read images
"""

'''
Reading images in RGB format
'''
def rgb(image_or_frame):
    # reading an image in the default BGR format for opencv
    try:
        image_or_frame = cv2.cvtColor(cv2.imread(image_or_frame),cv2.COLOR_BGR2RGB)
    except:
        print ("Please check the file path, there seems to be an error")
    """
    error checking
    """
    # in the event of an invalid file path this will be executed
    try:
        assert (image_or_frame) == None
        print ("Please check the file path, there seems to be an error")
    except Exception as errors:
        #raise AssertionError ("file found") from errors
        pass
    # returning the variable for re-use
    return image_or_frame

'''
Reading images in BGR format
'''
def bgr(image_or_frame):
    # reading an image in the default BGR format for opencv
    image_or_frame = cv2.imread(image_or_frame)
    """
    error checking
    """
    # in the event of an invalid file path this will be executed
    try:
        assert (image_or_frame) == None
        print ("Please check the file path, there seems to be an error")
    except Exception as errors:
        #raise AssertionError ("file found") from errors
        pass
    # returning the variable for re-use
    return image_or_frame

'''
Reading images in grayscale format
'''
def gray(image_or_frame):
    # reading an image in the default BGR format for opencv
    image_or_frame = cv2.imread(image_or_frame, 0)
    """
    error checking
    """
    # in the event of an invalid file path this will be executed
    try:
        assert (image_or_frame) == None
        print ("Please check the file path, there seems to be an error")
    except Exception as errors:
        #raise AssertionError ("file found") from errors
        pass
    # returning the variable for re-use
    return image_or_frame
            