from flask import json, request
from app import app
from bs4 import BeautifulSoup
from app.helpers import background
from app.helpers import response
from flask_pymongo import PyMongo
import requests
import re
from youtube_validation import ScrapValidation

mongo = PyMongo(app)
db = mongo.db


@app.route('/youtube/scrap', methods=['POST'])
def get_scrap():
    form = ScrapValidation(request.form)
    if not form.validate():
        errors = []
        for fieldName, errorMessages in form.errors.items():
            errors.append({fieldName: errorMessages})

        return response.error_response(422, 'Failed', errors)

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
        values = play_list_scraping(data)

    return response.success_response(200, 'Success', values)


def play_list_scraping(data):
    rows = []
    i = 0
    for content in data['contents']['twoColumnWatchNextResults']['playlist']['playlist']['contents']:
        content = content['playlistPanelVideoRenderer']

        # Image to be saved in background
        thumbnail = content['thumbnail']['thumbnails'][len(content['thumbnail']['thumbnails']) - 1]['url']
        async_class = background.Background()
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
                'image_path': image_name
            }
            async_class.save_data(collection='videos', row=row)
            row['_id'] = str(row['_id'])
            rows.append(row)
        except:
            print ('ERROR')
        finally:
            i += 1
    return rows
