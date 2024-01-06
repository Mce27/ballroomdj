import os,random,re
dances = {"smo":["waltz","tango","foxtrot","vwaltz"],
          "std":["waltz","tango","vwaltz","foxtrot","quickstep"],
          "rhy":["chacha","rumba","swing","bolero","mambo"],
          "lat":["samba","chacha","rumba","paso","jive"]
            }

def round_request(style:str,song_dict:dict):
    """
    pulls playlists from server and downloads one song for each dance in the style
    """
    if style == "all":
        for cat in dances.keys():
            for dance in dances[cat]:
                songs = os.listdir(f"music/{cat}/{dance}")
                i = random.randrange(0,len(songs)) #random int to grab a song
                song_to_play = f"music/{cat}/{dance}/{songs[i]}"
                song_name = re.sub(r'\.[a-z0-9]{3,4}$','',songs[i])
                song_dict[cat+dance] = (song_name,song_to_play)
    else:            
        for dance in dances[style]:
            songs = os.listdir(f"music/{style}/{dance}")
            i = random.randrange(0,len(songs)) #random int to grab a song
            song_to_play = f"music/{style}/{dance}/{songs[i]}"
            song_name = re.sub(r'\.[a-z0-9]{3,4}$','',songs[i])
            song_dict[style+dance] = (song_name,song_to_play)

        

def get_random_style_song(style:str):
    """
    Returns the filepath and song title of a random song from a certain style
    """
    if style == 'all':
        styles_list = list(dances.keys())
        rand = random.randint(0,len(styles_list)-1)
        style = styles_list[rand]

    dances_list = dances[style]
    i = random.randrange(0,len(dances_list)) #random int to grab a dance
    dance_to_get = dances_list[i]
    songs = os.listdir(f'music/{style}/{dance_to_get}')
    i = random.randrange(0,len(songs)) #random int to grab a song
    song_to_return = songs[i]

    filepath = f'music/{style}/{dance_to_get}/{song_to_return}'
    song_to_return = re.sub(r'\.[a-z0-9]{3,4}$','',song_to_return)
    return filepath,dance_to_get,song_to_return

def get_random_dance_song(style:str,dance:str):
    """
    Downloads a random song from a certain dance and style
    Returns the filepath
    """

    songs = os.listdir(f"music/{style}/{dance}")
    i = random.randrange(0,len(songs)) #random int to grab a song
    song_to_return = songs[i]
    filepath = f'music/{style}/{dance}/{song_to_return}'
    song_to_return = re.sub(r'\.[a-z0-9]{3,4}$','',song_to_return)
    return filepath, song_to_return


def setup():
    """
    builds media file structure 
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