import cv2
import numpy as np


class EdgeDetection:

    """
    This class is used to perform edge detection on an image, it will use canny edge detection,
    dilation and adaptive thresholding to find the clearest/sure edges of an image
    Once it has found the edges, it will identify the contour which represents the game contour
    and draw this contour onto the original frame
    """
    '''
    applies canny edge detection to the frame passed, min is set to 30 and max is set to 200
    returns the canny edge image
    '''
    def canny_edge(self, frame):
        canny = cv2.Canny(frame, 30, 200)
        return self.dilate(canny)

    '''
    dilates the image using a 3x3 matrix, performs 1 iterations
    '''
    @staticmethod
    def dilate(canny):
        # Dilate image to improve visible contours
        krnl = np.ones((5, 5), np.uint8)
        dilated_image = cv2.dilate(canny, krnl, iterations=1)
        return dilated_image

    '''
    This method will find all the contours of an image
    '''
    @staticmethod
    def find_contours(dilated_frame):
        _, cnts, _ = cv2.findContours(dilated_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return cnts

    '''
    This method will find the contour of the game from the list of contours it has found
    '''
    @staticmethod
    def find_game_cnt(cnts):
        game_cnts = None
        arc_length = 0
        # loop over our contours
        for contour in cnts:
            # approximate the contour
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
            # if our approximated contour has four points and has the greatest perimter (biggest rectangle in focus),
            # then:
            # we can assume that we have found our box
            if perimeter > arc_length and len(approx) == 4:
                game_cnts = approx
                arc_length = perimeter

        return game_cnts

    '''
    This method will draw the contour of the game into the frame that has been passed to it
    '''
    @staticmethod
    def draw_cnts(game_cnts, frame):
        frame = cv2.drawContours(frame, [game_cnts], -1, (0, 255, 0), 2)
        return frame
