import os
import requests
api_link='http://ballroom.mce27.xyz/rest/stream?id={id}&u=ballroom&t=32fc4daf799d520e6701b60cdb3178af&s=ow130p2&v=1.12.0&c=myapp'


def api_request(link:str):
    req = requests.get(link)
    with open('music/song.mp3','wb') as file:
        file.write(req.content)
    return 'music/song.mp3'

def setup():
    """
    builds media file structure and dls music from server
    """
    print("Setting up!\n")
    if not os.path.exists('music'):#means no fs is there
        os.mkdir('music')
        for cat in dances.keys():
            os.mkdir(f'music/{cat}')
            for dance in dances[cat]:
                os.mkdir(f'music/{cat}/{dance}')
    else:#check if rest of fs is there
        for cat in dances.keys():
            if not os.path.exists(f'music/{cat}'):
                os.mkdir(f'music/{cat}')
                for dance in dances[cat]:
                    os.mkdir(f'music/{cat}/{dance}')
            else:
                for dance in dances[cat]:#see if dir for each dance exists
                    if not os.path.exists(f'music/{cat}/{dance}'):
                        os.mkdir(f'music/{cat}/{dance}')
    #now that fs is in place, time to dl music