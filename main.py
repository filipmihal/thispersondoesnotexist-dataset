import urllib.request
import os, os.path
import dhash
from wand.image import Image
import time
from collections import Counter


class ThisPersonIsFake:

    url = "https://thispersondoesnotexist.com"
    default_path = "new.jpg"
    path = "data"
    image_name = "image_{0}.jpg"
    hashes_path = "db.txt"

    def __init__(self):
        self.number_of_faces = self.get_number_of_faces()
        self.image_hashes = self.get_hashes()

    def get_hashes(self):
        with open(self.hashes_path, 'r') as file:
            return file.read().split(',')

    def get_number_of_faces(self):
        return len([name for name in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, name))])

    def get_image_path(self, number: int):
        return self.path + "/" + self.image_name.format(number)

    def save_picture_from_web(self):
        urllib.request.urlretrieve(self.url, self.default_path)

    @staticmethod
    def get_image_hash(image_path: str):
        with Image(filename=image_path) as image:
            row, col = dhash.dhash_row_col(image)
        return dhash.format_hex(row, col)

    def is_duplicated(self, image_hash):
        return True if image_hash in self.image_hashes else False

    def save_image_hash(self, new_hash: str):
        self.image_hashes.append(new_hash)
        with open(self.hashes_path, 'a') as file:
            file.write("," + new_hash)

    def move_image_to_db(self):
        self.number_of_faces += 1
        os.rename(self.default_path, self.get_image_path(self.number_of_faces))

    def run(self):
        self.save_picture_from_web()
        new_hash = self.get_image_hash(self.default_path)
        if self.is_duplicated(new_hash):
            print("duplicated")
            return False
        else:
            self.move_image_to_db()
            self.save_image_hash(new_hash)
            return True


fake = ThisPersonIsFake()
for a in range(0, 200):
    time.sleep(2)
    if not fake.run():
        print("!!!!!!!!!!")
        break
# todo: repeat
print('fff')
# todo: if there is 5 pictures in a row that were repeated then stop the process

