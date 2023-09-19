import os
import requests
api_link='http://ballroom.mce27.xyz/rest/stream?id={id}&u=ballroom&t=32fc4daf799d520e6701b60cdb3178af&s=ow130p2&v=1.12.0&c=myapp'


def api_request(link:str):
    req = requests.get(link)
    with open('music/song.mp3','wb') as file:
        file.write(req.content)
    return 'music/song.mp3'
