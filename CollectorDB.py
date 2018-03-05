import sqlite3


class CollectorDB:

    """
    Class is used to check if game collector has game in their database

    """
    # constructor for db reader, @database is the database which you want to access
    def __init__(self, database):
        self.db = sqlite3.connect(database)
        self.cursor = self.db.cursor()

    # method which finds if the game is in the collectors database
    def check_game(self, game_name):
        name = None
        self.cursor.execute("SELECT * FROM Games WHERE name = '" + game_name + "'")
        data = self.cursor.fetchall()
        for d in data:
            name = d[0]
        if data is None:
            return None
        return name

    def get_all_games(self):
        self.cursor.execute("SELECT * FROM Games")
        data = self.cursor.fetchall()
        return data
