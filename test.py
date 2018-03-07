import unittest
from Database import DataBase
from ImageCorrection import ImageCorrection
from EdgeDetection import EdgeDetection
from ImageWarper import ImageWarper
from ImageHasher import ImageHasher
from CollectorDB import CollectorDB
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

    def test(self):
        # test collector string
        self.assertEqual(self.collectordb.check_game("Grand Theft Auto V"), "Grand Theft Auto V")
        self.assertEqual(self.myDb.ham_dst("2d2ec9e064603833", "2d2ec9e064603836"), 1)
        self.assertEqual(self.image_hasher.generate_hash(self.test_image), "2f6c71b19336322a")
        self.assertNotEqual(self.image_hasher.generate_hash(self.second_test), "2f6c71b19336322a")
