import os,requests,random
from bs4 import BeautifulSoup
api_link='http://ballroom.mce27.xyz/rest/stream?id={id}&u=ballroom&t=32fc4daf799d520e6701b60cdb3178af&s=ow130p2&v=1.12.0&c=myapp'
dances = {"std":["watlz","tango","vwaltz","foxtrot","quickstep"],
              "lat":["chacha","rumba","samba","jive"],
              "smo":["waltz","tango","vwaltz","foxtrot"],
              "rhy":["chacha","rumba","swing","bolero","mambo"]
              }

def api_request():
    """
    pulls playlists from server and downloads one song for each category
    """
    playlists = requests.get(f'http://ballroom.mce27.xyz/rest/getPlaylists?u=ballroom&t=32fc4daf799d520e6701b60cdb3178af&s=ow130p2&v=1.12.0&c=myapp')
    soup = BeautifulSoup(playlists.content)
    playlist_list = soup.find_all("playlist")
    playlist_dict = {}
    for playlist in playlist_list:
        playlist_dict[playlist['name']] = playlist['id']
    for cat in dances.keys():
        content_of_playlist = requests.get(f'http://ballroom.mce27.xyz/rest/getPlaylist?id={playlist_dict[cat]}&u=ballroom&t=32fc4daf799d520e6701b60cdb3178af&s=ow130p2&v=1.12.0&c=myapp')
        content_of_playlist = BeautifulSoup(content_of_playlist)
        songs = content_of_playlist.find_all('songs')   #@TODO make sure 'songs' is right
        i = random.random(0,len(songs)) #random int to grab a song
        song_to_dl = songs[i]['id']
        req = requests.get(f'http://ballroom.mce27.xyz/rest/stream?id={song_to_dl}&u=ballroom&t=32fc4daf799d520e6701b60cdb3178af&s=ow130p2&v=1.12.0&c=myapp')
        with open(f'music/{cat}/{cat+dances[cat]}/{songs[i]["name"]}.mp3','wb') as file:    #@TODO make sure 'name' is right
            file.write(req.content)

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