import cv2
import numpy as np

'''
code used from https://www.pyimagesearch.com/2014/05/05/building-pokedex-python-opencv-perspective-warping-step-5-6/
'''

class ImageWarper:

    @staticmethod
    def get_warped_image(game_cnts, shape_ratio, shape_orig):
        points = game_cnts.reshape(4, 2)
        rectangle = np.zeros((4, 2), dtype="float32")

        # top-left = smallest sum bottom-right = largest sum
        s = points.sum(axis=1)
        rectangle[0] = points[np.argmin(s)]
        rectangle[2] = points[np.argmax(s)]

        # compute difference between the points top-right will be smallest and bottom right will have largest difference
        difference = np.diff(points, axis=1)
        rectangle[1] = points[np.argmin(difference)]
        rectangle[3] = points[np.argmax(difference)]

        # scale rectangle to image
        rectangle *= shape_ratio
        # find width of warped image
        (top_left, top_right, bottom_right, bottom_left) = rectangle
        width_1 = np.sqrt(((bottom_right[0] - bottom_left[0]) ** 2) + ((bottom_right[1] - bottom_left[1]) ** 2))
        width_2 = np.sqrt(((top_right[0] - top_left[0]) ** 2) + ((top_right[1] - top_left[1]) ** 2))

        # find height of our transformed image
        height_1 = np.sqrt(((top_right[0] - bottom_right[0]) ** 2) + ((top_right[1] - bottom_right[1]) ** 2))
        height_2 = np.sqrt(((top_left[0] - bottom_left[0]) ** 2) + ((top_left[1] - bottom_left[1]) ** 2))

        # take the maximum of the width and height values to reach our final dimensions
        max_width = max(int(width_1), int(width_2))
        max_height = max(int(height_1), int(height_2))

        # construct destination pts which to create "birds eye" view
        distance = np.array([
            [0, 0],
            [max_width - 1, 0],
            [max_width - 1, max_height - 1],
            [0, max_height - 1]], dtype="float32")
        # generate transform matrix and warp the image
        matrix = cv2.getPerspectiveTransform(rectangle, distance)
        warped_image = cv2.warpPerspective(shape_orig, matrix, (max_width, max_height))
        warped_image = cv2.cvtColor(warped_image, cv2.COLOR_BGR2GRAY)
        return warped_image
