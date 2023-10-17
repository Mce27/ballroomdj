import os,requests,random
from bs4 import BeautifulSoup
URL = ''
token = ''
user = ''
salt = ''
dances = {"smo":["waltz","tango","vwaltz","foxtrot"],
          "std":["waltz","tango","vwaltz","foxtrot","quickstep"],
          "rhy":["chacha","rumba","swing","bolero","mambo"],
          "lat":["samba","chacha","rumba","jive","paso"]
            }

def round_request(style:str):
    """
    pulls playlists from server and downloads one song for each dance in the style
    """
    playlists = requests.get(f'http://{URL}/rest/getPlaylists?u={user}&t={token}&s={salt}&v=1.12.0&c=myapp')
    soup = BeautifulSoup(playlists.content,features='lxml')
    playlist_list = soup.find_all("playlist")
    playlist_dict = {}
    for playlist in playlist_list:
        if playlist['name'].startswith(style) or style == 'all':
            playlist_dict[playlist['name']] = playlist['id']
    for cat in playlist_dict.keys():
        content_of_playlist = requests.get(f'http://{URL}/rest/getPlaylist?id={playlist_dict[cat]}&u={user}&t={token}&s={salt}&v=1.12.0&c=myapp')
        content_of_playlist = BeautifulSoup(content_of_playlist.content,features='lxml')
        songs = content_of_playlist.find_all('entry')
        i = random.randrange(0,len(songs)) #random int to grab a song
        song_to_dl = songs[i]['id']
        req = requests.get(f'http://{URL}/rest/stream?id={song_to_dl}&u={user}&t={token}&format=mp3&s={salt}&v=1.12.0&c=myapp')
        with open(f'music/{cat[:3]}/{cat[3:]}/{songs[i]["title"]}.mp3','wb') as file:
            file.write(req.content)

def get_random_style_song(style:str):
    """
    Downloads a random song from a certain style
    Returns the filepath and song title
    """
    if style == 'all':
        styles_list = list(dances.keys())
        rand = random.randint(0,len(styles_list)-1)
        style = styles_list[rand]
    dances_list = dances[style]
    i = random.randrange(0,len(dances_list)) #random int to grab a dance
    dance_to_get = dances_list[i]
    playlists = requests.get(f'http://{URL}/rest/getPlaylists?u={user}&t={token}&s={salt}&v=1.12.0&c=myapp')
    soup = BeautifulSoup(playlists.content,features='lxml')
    playlist_list = soup.find_all("playlist")
    playlist_dict = {}

    for playlist in playlist_list:
        playlist_dict[playlist['name']] = playlist['id']

    content_of_playlist = requests.get(f'http://{URL}/rest/getPlaylist?id={playlist_dict[style + dance_to_get]}&u={user}&t={token}&s={salt}&v=1.12.0&c=myapp')
    content_of_playlist = BeautifulSoup(content_of_playlist.content,features='lxml')
    songs = content_of_playlist.find_all('entry')
    i = random.randrange(0,len(songs)) #random int to grab a song
    song_to_dl = songs[i]
    filepath = f'music/{style}/{dance_to_get}/{song_to_dl["title"]}.mp3'
    get_song(song_to_dl['id'],filepath)
    return filepath,dance_to_get,song_to_dl['title']

def get_random_dance_song(style:str,dance:str):
    """
    Downloads a random song from a certain dance and style
    Returns the filepath
    """
    playlists = requests.get(f'http://{URL}/rest/getPlaylists?u={user}&t={token}&s={salt}&v=1.12.0&c=myapp')
    soup = BeautifulSoup(playlists.content,features='lxml')
    playlist_list = soup.find_all("playlist")
    playlist_dict = {}

    for playlist in playlist_list:
        playlist_dict[playlist['name']] = playlist['id']

    content_of_playlist = requests.get(f'http://{URL}/rest/getPlaylist?id={playlist_dict[style + dance]}&u={user}&t={token}&s={salt}&v=1.12.0&c=myapp')
    content_of_playlist = BeautifulSoup(content_of_playlist.content,features='lxml')
    songs = content_of_playlist.find_all('entry')
    i = random.randrange(0,len(songs)) #random int to grab a song
    song_to_dl = songs[i]
    filepath = f'music/{style}/{dance}/{song_to_dl["title"]}.mp3'
    get_song(song_to_dl['id'],filepath)
    return filepath, song_to_dl['title']

def get_song(id:str,out_path:str):
    if not os.path.exists(out_path):
        song = requests.get(f'http://{URL}/rest/stream?id={id}&u={user}&t={token}&format=mp3&s={salt}&v=1.12.0&c=myapp')
        try:
            with open(out_path,'wb') as file:
                file.write(song.content)
        except PermissionError as e:
            print("error: " + str(e))

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
    # time to get user creds
    if not os.path.exists('config.txt'):
        print("Please put your credentials in a file named config.txt\n"\
              "They should be in the form:\n URL\nuser\ntoken\nsalt\n"\
              "This program is built to access a Subsonic api, namely Navidrome."\
              "Refer to the 'Authentication' section in http://www.subsonic.org/pages/api.jsp for more information"
              )
    else:
        global URL, user, token, salt
        with open("config.txt") as file:
            data = file.read().strip()
            URL, user, token, salt = data.split('\n')