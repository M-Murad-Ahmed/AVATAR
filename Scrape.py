from bs4 import BeautifulSoup
import requests
from tkinter import *
p = print


class Scraper:

    """
    This method will scrape the web for a game that is NOT in the collectors database
    """
    @staticmethod
    def scrape_game(game_name, real_name):
        # generate request URL
        url = "http://www.argos.co.uk/search/" + game_name + "ps4/"
        # retrieve page
        page = requests.get(url)
        # parse page as HTML
        soup = BeautifulSoup(page.content, 'html.parser')
        # find relevant span tags for each item required from html
        price = soup.find('span', class_='ac-product-price__amount').get_text()
        name = soup.find('div', class_='ac-product-name ac-product-card__name').get_text()
        rating = soup.find('div', class_='ac-product-card__rating').get_text()
        rating = rating.split(" ")
        rating = rating[1]
        rating = rating.split(".")
        rating = rating[0]
        lower_name = str(name).lower()
        real_name = real_name.lower()
        check_name = real_name.split(" ")
        count = 0
        coll_root = Tk()
        output = ""
        # check if the game retrieved matches our search criteria
        for words in check_name:
            if words in lower_name:
                count = count + 1
        # if it does, inform user of the name, price and rating
        if count == len(check_name):
            # print(name + " available for " + price + " at " + url)
            output = output + name + " available for " + price + " at " + url + "\n"
            output = output + rating + "out of 5 stars\n"
            # print(rating, "out of 5 stars")
            p("")
        else:
            output = "Unable to find game at " + url +"\n"
            # print("Unable to find game at " + url)
            # p("")
        coll_label = Label(coll_root, text=output)
        coll_label.pack()
        coll_root.mainloop()
