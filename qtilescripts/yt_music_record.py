#!/usr/bin/env python

# Daniel Mendoza
# Robotics Engineer

import dbus
from pathlib import Path
import time
import re
import subprocess as sp
import sys


videos = str(Path.home()) + '/Music/'
script_path = str(Path(__file__).parent.absolute()) + '/'
sp.run(f'rm -f {script_path}*.mp4',shell=True,stdout=sp.DEVNULL)
audio_sources = sp.Popen(['pactl','list','short','sources'],stdout=sp.PIPE,stderr=sp.PIPE,text=True).communicate()[0].strip()
audio_ouput = re.search(r'(?<=\s)alsa_output[^\s]+',audio_sources).group(0)


bus = dbus.SessionBus()

s = None
for service in bus.list_names():
    if service.startswith('org.mpris.MediaPlayer2.'):
        try:
            ffox = re.findall(r'\bf[irefox]*\b',service)[0]
        except IndexError:
            sys.exit("[ERROR] firefox player not found")
            continue
        if ffox:
            s = service
            break
ffox_player = dbus.SessionBus().get_object(s, '/org/mpris/MediaPlayer2')
meta = dbus.Interface(ffox_player, 
        dbus_interface='org.freedesktop.DBus.Properties')
metadata = meta.GetAll('org.mpris.MediaPlayer2.Player')
song = metadata['Metadata']['xesam:title']
ffox_device = dbus.Interface(ffox_player, dbus_interface='org.mpris.MediaPlayer2.Player')
album = metadata['Metadata']['xesam:album']
artist = str(metadata['Metadata']['xesam:artist'][0])
album_cover = metadata['Metadata']['mpris:artUrl'].replace('file://','')
if metadata['PlaybackStatus'] != 'Playing':
    ffox_device.PlayPause()



# OUTPUT
def print_to_terminal():
    data = f"""

        {'Album':<7}: {album}
        {'Artist':<7}: {artist}
        {'Song':<7}: {song}
        {'Cover':<7}: {album_cover}

    """
    return data


# Get album cover - wget and imagemagick required
def cover(image):
    # Validate if the size of the album cover is 640x640
    # if the size is different it will be changed to 640x640
    image_size1 = sp.Popen(
            ['file', image], stdout=sp.PIPE)
    image_size2 = sp.Popen(
            ["awk {'print $5\"x\"$7'}"],
            shell=True, stdin=image_size1.stdout, stdout=sp.PIPE)
    image_size1.stdout.close()
    image_size3 = sp.Popen(
            ['tr', '-d', '\,'],
            text=True, stdin=image_size2.stdout, stdout=sp.PIPE, stderr=sp.PIPE)
    image_size2.stdout.close()
    size = image_size3.communicate()[0]
    if size not in ('540x540','544x544','640x640'):
         convert = sp.Popen(
                 ['convert', image, 
                     '-resize', '640x640!', image],
                 stdout=sp.PIPE,
                 stderr=sp.DEVNULL)
         convert.communicate()[0]
    return image

# Check if the track already exists
def mp4_exists(track):
    counter = 0
    track_exists = Path(track)
    while track_exists.is_file():
        counter += 1
        track = f'{videos}{artist} : {song}_{counter}.mp4'
        track_exists = Path(track)
    return track

# Record ("30" secs) audio from your computer 
def record(image,song):

    recorded = sp.Popen(
            ['ffmpeg','-y','-framerate','1','-i',image,
            '-f','pulse','-i',audio_ouput,'-t','30','-vf','format=yuv420p',
             song
            ],stdout=sp.PIPE, stderr=sp.PIPE)

    return recorded.communicate()

def add_thumbnail(video,image):
    thumb = sp.Popen(
            ['ffmpeg','-y','-i',video,'-vf',"thumbnail,scale=320:320",
                '-frames:v','1',image,
            ],stdout=sp.PIPE, stderr=sp.DEVNULL)
    thumb.communicate()[0]

    thumbnailed = sp.Popen(
            ['ffmpeg','-y','-i',video,'-i',image,
                '-map','1','-map','0','-c','copy','-disposition:0','attached_pic',
                f'{track}'
            ],stdout=sp.PIPE, stderr=sp.DEVNULL)

    return thumbnailed.communicate()

print(print_to_terminal())
cover(album_cover)
song = song.replace('/','-')
track = f'{videos}{artist} : {song}.mp4'
track = mp4_exists(track)
song_to_record = f'{script_path}{artist} : {song}.mp4'
record(album_cover,song_to_record)
add_thumbnail(f'{song_to_record}',f'{script_path}thumb.png')
