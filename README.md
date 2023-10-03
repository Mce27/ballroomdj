# Ballroom DJ
This is a python application that interfaces with a Subsonic api to play music in ballroom-esk ways.

## Client Setup
1. Clone or download this repo. 
2. Create a file named config.txt in the same directory, with the following contents:
    1. Url (ex: navidrome.domain.com or 192.168.192.168:3533)
    2. Username from the server
    3. Token for the user (Refer to the 'Authentication' section in http://www.subsonic.org/pages/api.jsp for more information)
    4. Salt (Refer to previous point)
3. Run `pip install -r requirements.txt` to install the requrements
    1. In the event you're on linux and pip throws a fit, you'll have to go through each of the modules and install them with your package manager.
    2. On debian you'd use `apt install python3-xyz`

## Server Setup
The program expects the Subsonic server. I used a Navidrome docker and would recommend the same.

### Playlists
On the server, make the following playlists:
- smowaltz
- smotango
- smovwaltz
- smofoxtrot
- stdwaltz
- stdtango
- stdvwaltz
- stdfoxtrot
- stdquickstep
- rhychacha
- rhyrumba
- rhyswing
- rhybolero
- rhymambo
- latsamba
- latchacha
- latrumba
- latjive
- latpaso

I know this is a pain. I might make a script to automate this, not sure.

Anyway, with those playlists created, add your music to their respecive playlists.  
These can be in any file type, but this program used mp3 and will transcode.
As long as you're not running the server on a potato, it shouldn't be that bad.

## Run it!
With the client and server setup, you should be all set to dance! 
### Windows:
Run `python ballroomdj.py` in the command line, or just double click the ballroomdj.py file. 
### Linux:
Run `python3 ballroomdj.py` in the command line.