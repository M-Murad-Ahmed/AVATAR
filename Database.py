import sqlite3

p = print


class DataBase:

    """
    This class is used to read from the AVATAR DB of games to identify which game the user
    has scanned
    """

    '''
    Constructor for database object, @database represents the database the object is accessing
    '''
    def __init__(self, database):
        self.db = sqlite3.connect(database)
        self.cursor = self.db.cursor()

    '''
    This method retrieves from the db the games which have the most similar hashes 
    compared to the calculated hash
    '''
    def fetch_hash(self, hash_value):
        # p(hash_value)
        self.cursor.execute("SELECT Hash FROM Games WHERE Hash LIKE '" + hash_value[:1] + "%" + "'")
        data = self.cursor.fetchall()
        # set the default best hash to nothin
        best_hash = ''
        # set the best hamming distance to any value > best value
        best_distance = 999
        # set the max distance a hash can be to be considered close to a game in the database
        max_dist = 5
        # iterate through the games to find which has the lowest hamming distance to the original hash
        for d in data:
            # assign the current hash
            current_dist = self.ham_dst(d[0], hash_value)
            # if the current hash has a hamming distance less than the current best and is less than the max distance
            if current_dist < best_distance and current_dist < max_dist:
                # save this hash value
                best_hash = d[0]
                # save the current hamming distance
                best_distance = current_dist
        # retrieve from the database the hash which was closest to the one we identified
        self.cursor.execute("SELECT * FROM Games WHERE Hash = '" + best_hash + "'")
        data = self.cursor.fetchall()
        # return the name of the game for further processing
        if data is not None:
            return data
        else:
            return None
    """
    this method calculates hamming distance between a pair of hexadecimal hashes
    converts each hex value (0-9, A-F) into the respective denary value
    compares the difference between each hex value and for values >
    3 add 1 to hamming distance and return the hamming distance once entire
    hash is traversed
    """
    def ham_dst(self, hash1, hash2):
        # set hamming distance to 0
        hamming_dist = 0
        # iterate through the hash
        for x in range(len(hash1)):
            # compare indexed value of hash
            v1 = int(hash1[x], 16)
            v2 = int(hash2[x], 16)
            # if the difference between the two values is more than 2, add 1 to the hamming distance
            if self.compare(v1, v2) > 2:
                hamming_dist = hamming_dist + 1
        # print("hamming distance is ", hamming_dist)
        return hamming_dist

    @staticmethod
    def compare(a, b):
        if a > b:
            return a - b
        if a == b:
            return 0
        if b > a:
            return b - a
