import cv2
import imutils
from Database import DataBase
from ImageCorrection import ImageCorrection
from EdgeDetection import EdgeDetection
from ImageWarper import ImageWarper
from ImageHasher import ImageHasher
from CollectorDB import CollectorDB
from Scrape import Scraper
from tkinter import *
warped = None
p = print


def scan_game():
    cap = cv2.VideoCapture(1)
    # p("press command q to exit")
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
                cv2.namedWindow('Warped', cv2.WINDOW_GUI_NORMAL)
                # if there is a game contour within the image...
                if game_cnts is not None:
                    # draw the contour of the game box onto the screen
                    frame = edge_detection.draw_cnts(game_cnts, frame)
                    # create a warped image of the content within the contour
                    global warped
                    warped = image_warper.get_warped_image(game_cnts, ratio, orig)

            # set a event listener for the image
            cv2.setMouseCallback('Warped', get_warped_hash)
            # show the user the screen
            cv2.imshow('Warped', frame)
            # loop all of above until user quits program
            if cv2.waitKey(1) == 1048689:
                sys.exit()


''' 
@event is the event type, the next two param are the x and y coordinates respectively
flag contains any flags being used on the method call
'''


def get_colls():
    game_coll = []
    text = collectordb.get_all_games()
    for item in text:
        game_coll.append(item)
    # p(game_coll)
    output = "Games in collectors database: \n\n"
    for game in game_coll:
        output = output + "Name: " + game[0] + "\n"
        output = output + "Developer: " + game[2] + "\n"
        output = output + "Publisher: " + game[3] + "\n"
        output = output + "\n\n"
    coll_root = Tk()
    coll_label = Label(coll_root, text=output)
    coll_label.pack()
    coll_root.mainloop()


def get_warped_hash(event, x_cords, y_cords, flag, void):
    try:
        if event == cv2.EVENT_LBUTTONDOWN:
            this_hash = image_hasher.generate_hash(warped)
            game_info = myDb.fetch_hash(this_hash)
            if game_info is not []:
                found_game = game_info[0]
                # p (found_game[1])
                name = found_game[1]
                game = collectordb.check_game(name)
                search_query = ''
                query_words = name.split(' ')
                for words in query_words:
                    search_query += words + '-'

                if game is not None:
                    output = "Game is found to be: "
                    output = output + "Name: " + found_game[1] + "\n"
                    output = output + "Developer: " + found_game[2] + "\n"
                    output = output + "Publisher: " + found_game[3] + "\n"
                    output = output + "Game is in your database \n"
                    found_root = Tk()
                    found_label = Label(found_root, text=output)
                    found_label.pack()
                    found_root.mainloop()
                elif name is not "":
                    myScraper.scrape_game(search_query, name)
    except IndexError:
        p("No game found")


if __name__ == '__main__':
    myScraper = Scraper()
    myDb = DataBase('avatar.db')
    collectordb = CollectorDB('collector.db')
    imageCorrection = ImageCorrection()
    edge_detection = EdgeDetection()
    image_warper = ImageWarper()
    image_hasher = ImageHasher()
    root = Tk()
    topframe = Frame(root)
    topLabel = Label(root, text="What would you like to do?")
    topLabel.grid(row=0, column=0)
    view = Button(root, text="View", command=get_colls)
    view.grid(row=1, column=0)
    scan = Button(root, text="scan", command=scan_game)
    scan.grid(row=1, column=1)
    root.mainloop()
