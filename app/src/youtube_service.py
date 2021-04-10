from app.helpers import background
from flask import json
import requests
import re
from bs4 import BeautifulSoup
from app import config

class YoutubeService:

    def __init__(self):
        pass

    def get_scrap(self, form):
        # https://www.youtube.com/watch?v=cnZfPPiivwk&list=RDMMcnZfPPiivwk

        page_text = requests.get(form.url.data).text

        soup = BeautifulSoup(page_text.encode('utf-8'), 'html.parser')
        pattern = re.compile("var ytInitialData")
        script = soup.find("script", text=pattern)
        m = re.search('var ytInitialData = (.*?)', script.string.strip())
        f = open("./app/data.json", "w")
        f.write(m.string.strip().replace('var ytInitialData = ', '').replace(';', '').encode('utf-8'))
        f.close()

        data = json.load(open('./app/data.json', 'r'))
        if re.search("^(https|http):\/\/(?:www\.)?youtube\.com\/watch\?((v=.*&list=.*)|(list=.*&v=.*))(&.*)*$",
                     form.url.data):
            values = self._play_list_scraping(data)
        else:
            values = self._channel_scraping(data)

        return values

    def _play_list_scraping(self, data):
        rows = []
        i = 0
        async_class = background.Background()

        for content in data['contents']['twoColumnWatchNextResults']['playlist']['playlist']['contents']:
            content = content['playlistPanelVideoRenderer']

            # Image to be saved in background
            thumbnail = content['thumbnail']['thumbnails'][len(content['thumbnail']['thumbnails']) - 1]['url']
            image_name = async_class.download(file_link=thumbnail)

            # We can optimize it more to get if the video id exits before update only data if there is a change
            try:
                if i == 0:
                    views = data['contents']['twoColumnWatchNextResults']['results']['results']['contents'][i][
                        'videoPrimaryInfoRenderer']['viewCount']['videoViewCountRenderer']['viewCount']['simpleText']
                else:
                    views = data['contents']['twoColumnWatchNextResults']['secondaryResults']['secondaryResults'][
                        'results'][i]['compactVideoRenderer']['shortViewCountText']['simpleText']
                row = {
                    'duration': content['lengthText']['simpleText'],
                    'url': "https://www.youtube.com" +
                           content['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url'],
                    'title': content['title']['simpleText'],
                    'thumbnail': thumbnail,
                    'views': views,
                    'image_path': config['APP_URL'] + image_name[1:]
                }
                async_class.save_data(collection='videos', row=row)
                row['_id'] = str(row['_id'])
                rows.append(row)
            except:
                print ('ERROR')
            finally:
                i += 1
        return rows

    def _channel_scraping(self, data):
        i = 0
        rows = []
        try:
            async_class = background.Background()

            for content in data['contents']['twoColumnBrowseResultsRenderer']['tabs'][1]['tabRenderer'][
                'content']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][0]['gridRenderer'][
                'items']:
                try:
                    content = content['gridVideoRenderer']
                    thumbnail = content['thumbnail']['thumbnails'][len(content['thumbnail']['thumbnails']) - 1]['url']
                    image_name = async_class.download(file_link=thumbnail)

                    row = {
                        'duration': content['thumbnailOverlays'][0]['thumbnailOverlayTimeStatusRenderer']['text'][
                            'simpleText'],
                        'url': "https://www.youtube.com" +
                               content['navigationEndpoint']['commandMetadata']['webCommandMetadata']['url'],
                        'title': content['title']['runs'][0]['text'],
                        'thumbnail': thumbnail,
                        'views': content['viewCountText']['simpleText'],
                        'image_path': config['APP_URL'] + image_name[1:]
                    }
                    async_class.save_data(collection='videos', row=row)
                    row['_id'] = str(row['_id'])
                    rows.append(row)
                except:
                    print ('ERROR')
                finally:
                    i += 1
        except:
            print ('ERROR')

        return rows
