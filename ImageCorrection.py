import cv2


class ImageCorrection:

    """
    returns a grayscale image of the image passed in its argument
    @frame is the opencv image passed
    """
    def get_gray(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return self.apply_filter(gray)

    '''
    applies bilateral filter to the image and returns the filtered image
    '''
    def apply_filter(self, frame):
        bilateral = cv2.bilateralFilter(frame, 35, 50, 11)
        return self.adaptive_threshold(bilateral)

    '''
    Applies local thresholding to identify core foreground and background pixel values in an image
    '''
    @staticmethod
    def adaptive_threshold(frame):
        threshold_image = cv2.adaptiveThreshold(frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        return threshold_image
