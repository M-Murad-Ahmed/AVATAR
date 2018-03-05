import cv2
import numpy as np


class ImageWarper:

    @staticmethod
    def get_warped_image(game_cnts, shape_ratio, shape_orig):
        points = game_cnts.reshape(4, 2)
        rectangle = np.zeros((4, 2), dtype="float32")

        # the top-left point has the smallest sum where as the
        # bottom-right has the largest sum
        s = points.sum(axis=1)
        rectangle[0] = points[np.argmin(s)]
        rectangle[2] = points[np.argmax(s)]

        # compute the difference between the points -- the top-right
        # will have the minimum difference and the bottom-left will
        # have the maximum difference
        diff = np.diff(points, axis=1)
        rectangle[1] = points[np.argmin(diff)]
        rectangle[3] = points[np.argmax(diff)]

        # multiply the rectangle by the original ratio
        rectangle *= shape_ratio
        # now that we have our rectangle of points, let's compute the width of our new image
        (tl, tr, br, bl) = rectangle
        width_A = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        width_B = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

        # ...and now for the height of our new image
        height_A = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        height_B = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

        # take the maximum of the width and height values to reach our final dimensions
        maxWidth = max(int(width_A), int(width_B))
        maxHeight = max(int(height_A), int(height_B))

        # construct our destination points which will be used to
        # map the screen to a top-down, "birds eye" view
        distance = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype="float32")
        # calculate the perspective transform matrix and warp
        # the perspective to grab the box
        matrix = cv2.getPerspectiveTransform(rectangle, distance)
        warped_image = cv2.warpPerspective(shape_orig, matrix, (maxWidth, maxHeight))
        warped_image = cv2.cvtColor(warped_image, cv2.COLOR_BGR2GRAY)
        return warped_image
