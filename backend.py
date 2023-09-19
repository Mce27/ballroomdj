import os
import requests


def api_request(link:str):
    req = requests.get(link)
    with open('music/song.mp3','wb') as file:
        file.write(req.content)
    return 'music/song.mp3'
