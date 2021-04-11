from app import db


class YoutubeRepository:
    def __init__(self):
        pass

    def save_video(self, row):
        db.videos.insert(row)
