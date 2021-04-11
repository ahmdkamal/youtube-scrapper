import random
import string
import urllib
import threading


class Background:
    def __init__(self):
        pass

    def download(self, file_link):
        image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        image_name = './images/' + image_name + '.jpg'
        download_thread = threading.Thread(target=self.save_image_from_link, args=(file_link,image_name))
        download_thread.start()
        return image_name

    def save_image_from_link(self, file_link, image_name):
        urllib.urlretrieve(file_link, image_name)