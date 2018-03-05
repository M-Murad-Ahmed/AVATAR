
import Image
import imagehash


class ImageHasher:

    """
    This class is used to generate hashes
    """

    # method which uses difference hashing to generate a hash for a given image
    @staticmethod
    def generate_hash(image_to_hash):
        image = Image.fromarray(image_to_hash)
        this_hash = imagehash.dhash(image).__str__()
        # print(this_hash)
        return this_hash
