import random
import string
import urllib
import threading

class ImageDownloader():
    def download(self, file_link):
        download_thread = threading.Thread(target=self.save_image_from_link, args=(file_link,))
        download_thread.start()

    def save_image_from_link(self, file_link):
        image_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        urllib.urlretrieve(file_link, './images/' + image_name + '.jpg')
