import unittest
from Database import DataBase
from ImageCorrection import ImageCorrection
from EdgeDetection import EdgeDetection
from ImageWarper import ImageWarper
from ImageHasher import ImageHasher
from CollectorDB import CollectorDB
import numpy as np
from Scrape import Scraper
import cv2


class MyTest(unittest.TestCase):
    myScraper = Scraper()
    myDb = DataBase('avatar.db')
    collectordb = CollectorDB('collector.db')
    imageCorrection = ImageCorrection()
    edge_detection = EdgeDetection()
    image_warper = ImageWarper()
    image_hasher = ImageHasher()
    test_image = cv2.imread("warped.jpg")
    second_test = cv2.imread("ow.jpg")
    third_test = cv2.imread("dilated.jpg")

    def test(self):
        # test collector string
        self.assertEqual(self.collectordb.check_game("Grand Theft Auto V"), "Grand Theft Auto V")
        # second test
        self.assertNotEqual(self.collectordb.check_game("Grand Theft Auto V"), "Tekken 7")

        # checking hamming distance calculation
        self.assertEqual(self.myDb.ham_dst("2d2ec9e064603833", "2d2ec9e064603833"), 0)
        self.assertEqual(self.myDb.ham_dst("2d2bf9e56460f833", "2d2ec9e064603836"), 5)

        # no two images should have same hash
        self.assertEqual(self.image_hasher.generate_hash(self.test_image), "2f6c71b19336322a")
        self.assertNotEqual(self.image_hasher.generate_hash(self.second_test), "2f6c71b19336322a")

        # retrieving from db should always be a list
        self.assertIsInstance(self.myDb.fetch_hash("2d2ec9e064603836"), list)
        # cv2 should return images
        self.assertIsInstance(self.edge_detection.canny_edge(self.second_test), np.ndarray)

