import cv2
import imutils
from Database import DataBase
from ImageCorrection import ImageCorrection
from EdgeDetection import EdgeDetection
from ImageWarper import ImageWarper
from ImageHasher import ImageHasher
from CollectorDB import CollectorDB
from AVATAR.Scrape import Scrape
from tkinter import *
from tkinter import ttk

p = print


''' 
@event is the event type, the next two param are the x and y coordinates respectively
flag contains any flags being used on the method call
'''


def get_warped_hash(event, x_cords, y_cords, flag, void):
    if event == cv2.EVENT_LBUTTONDOWN:
        this_hash = image_hasher.generate_hash(warped)
        # cv2.imwrite('warped.jpg', warped)
        name = myDb.fetch_hash(this_hash)
        game = collectordb.check_game(name)
        search_query = ''
        query_words = name.split(' ')
        for words in query_words:
            search_query += words + '-'

        if game is not None:
            p('Game is in collectors database.')
            p('')
        elif name is not "":
            scraper.scrape_game(search_query, name)


# todo add GUI function
if __name__ == '__main__':

    myDb = DataBase('avatar.db')
    collectordb = CollectorDB('collector.db')
    imageCorrection = ImageCorrection()
    edge_detection = EdgeDetection()
    image_warper = ImageWarper()
    image_hasher = ImageHasher()
    scraper = Scrape()

    choice = int(input("What would you like to do? 1)View own collection 2)Scan a game"))
    if choice == 1:
        p("Your collection contains: ")
        p("")
        collectordb.get_all_games()

    elif choice == 2:
        cap = cv2.VideoCapture(1)
        p("press command q to exit")
        while cap.isOpened():
                ret, frame = cap.read()
                if frame is not None:
                    # keep a shallow copy of the frame (required for warping)
                    orig = frame.copy()
                    # set aspect ratio of captured frame
                    ratio = frame.shape[0] / 300.0
                    # set size of frame visible to user to be 300 pixels in height
                    frame = imutils.resize(frame, height=300)

                    if ret:
                        # apply image correction techniques (gray scale, bilateral filter and adaptive thresholding)
                        corrected_image = ImageCorrection.get_gray(self=imageCorrection, frame=frame)
                        # returns a dilated canny edge image of corrected image from above
                        canny = edge_detection.canny_edge(corrected_image)
                        # identifies the contours in dilated canny edge image
                        cnts = edge_detection.find_contours(canny)
                        # identifies the contour of the game within the contours of the image
                        game_cnts = edge_detection.find_game_cnt(cnts)
                        # creates a named window called warped
                        cv2.namedWindow('Warped')
                        # if there is a game contour within the image...
                        if game_cnts is not None:
                            # draw the contour of the game box onto the screen
                            frame = edge_detection.draw_cnts(game_cnts, frame)
                            # create a warped image of the content within the contour
                            warped = image_warper.get_warped_image(game_cnts, ratio, orig)

                    # set a event listener for the image
                    cv2.setMouseCallback('Warped', get_warped_hash)
                    # show the user the screen
                    cv2.imshow('Warped', frame)
                    # loop all of above until user quits program
                    if cv2.waitKey(1) == 1048689:
                        break
