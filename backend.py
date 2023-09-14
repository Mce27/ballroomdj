import os
import requests


def api_request(link:str):
    req = requests.get(link)
    if not os.path.exists('music'):
        os.mkdir('music')
    with open('music/song.mp3','wb') as file:
        file.write(req.content)
    return 'music/song.mp3'
