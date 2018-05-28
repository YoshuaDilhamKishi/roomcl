from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys

#FlickrAPI
key = "363701b80a36893673634fe3db99769e"
secret = "78582e2647c1e1c6"
wait_time = 1

#保存フォルダ
roomname = sys.argv[1]
savedir = "./" + roomname

flickr= FlickrAPI(key, secret, format='parsed-json')
result = flickr.photos.search(
    text = roomname,
    per_page = 400,
    media = 'photos',
    sort = 'relevance',
    safe_search = 1,
    extras = 'url_q, licence'
)

photos = result['photos']


for i, photo in enumerate(photos['photo']):
    url_q = photo['url_q']
    filepath = savedir + '/' + photo['id'] + '.jpg'
    if os.path.exists(filepath): continue
    urlretrieve(url_q, filepath)
    time.sleep(wait_time)
