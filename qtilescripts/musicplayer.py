#!/usr/bin/env python

import dbus
import re
import subprocess as sp
import os
from libqtile.widget import base
from libqtile.log_utils import logger

class MusicPlayer(base.InLoopPollText):

    bus = dbus.SessionBus()
    user = os.environ['USER']

    def __init__(self, **config):
        base.InLoopPollText.__init__(self, **config)
        self.update_interval = 0.5
        self.add_callbacks({
            'Button1': self.play_pause,
            'Button3': self.record,
            'Button4': self.prev,
            'Button5': self.next
            })

    def get_player_metadata(self):
        lst_players = list()
        player_dict = dict()
        for service in MusicPlayer.bus.list_names():
            if service.startswith('org.mpris.MediaPlayer2.'):
                lst_players.append(str(service))
        len_lst_players = len(lst_players)
        if len_lst_players:
            for player in range(len_lst_players):
                service = lst_players[player]
                music_player = re.findall(
                        r'\bc[hromium]*\b|\bf[irefox]*\b|\bs[potify]*\b',service)
                        #r'\bf[irefox]*\b|\bs[potify]*\b',service)
                player_meta = dbus.SessionBus().get_object(service,
                                                           '/org/mpris/MediaPlayer2')
                player_meta = dbus.Interface(player_meta,
                                             dbus_interface='org.freedesktop.DBus.Properties')
                ctrl_player = dbus.Interface(player_meta,
                                             dbus_interface='org.mpris.MediaPlayer2.Player')
                player_dict = {
                        'PlayerMetadata': player_meta,
                        'Control': ctrl_player,
                        'Player': music_player[0].title()
                        }
                m_player = player_dict['Player']
                if m_player == 'Spotify':
                    player_dict['mediaplayer'] = 'spotify'
                elif m_player == 'chromium':
                    player_dict['mediaplayer'] = 'chromium'
                else:
                    player_dict['mediaplayer'] = 'firefox'
                m_player = ''
                # m_player = ''
                meta = player_dict['PlayerMetadata']
                metas = meta.GetAll('org.mpris.MediaPlayer2.Player')
                sts_playback = metas['PlaybackStatus']
                if sts_playback == 'Playing':
                    artist = f"{metas['Metadata']['xesam:artist'][0]}"
                    title = f"{metas['Metadata']['xesam:title']}"
                    if artist:
                        output = f"{m_player}{artist}"
                    else:
                        output = f"{m_player}{title}"
                    player_dict['CurrentlyPlaying'] = output
                    return player_dict
                elif sts_playback == 'Paused' \
                        and len_lst_players == player+1:
                    output = "Paused"
                    player_dict['CurrentlyPlaying'] = output
                    return player_dict
                elif len_lst_players < player+1:
                    output = "Paused"
                    player_dict['CurrentlyPlaying'] = output
                    return player_dict
        return player_dict

    def poll(self):
        try:
            track_playing = self.get_player_metadata()['CurrentlyPlaying']
            track_playing = track_playing.replace('&','and')
        except:
            return ''
        return track_playing[:40]

    def play_pause(self):
        player = self.get_player_metadata()['Control']
        return player.PlayPause()

    def next(self):
        player = self.get_player_metadata()['Control']
        return player.Next()

    def prev(self):
        player = self.get_player_metadata()['Control']
        return player.Previous()

    def stop(self):
        player = self.get_player_metadata()['Control']
        return player.Stop()

    def record(self):

        if not self.get_player_metadata():
            return
        mediaplayer = self.get_player_metadata()['mediaplayer']

        spotify_running = sp.Popen(
                [f'/home/{MusicPlayer.user}/Documents/GITREPOS/SpotifyAudioRecorded/.venv/bin/python',
                 f'/home/{MusicPlayer.user}/Documents/GITREPOS/SpotifyAudioRecorded/recording_spotify_track.py',
                 '-o','mpqtile']
                ,stdout=sp.PIPE,stderr=sp.PIPE)
        web_spotify = spotify_running.communicate()[0].decode().replace('\n','')

        ytmusic = sp.Popen(
                 [f'/home/{MusicPlayer.user}/Documents/GITREPOS/ytmusic/.venv/bin/python',
                  f'/home/{MusicPlayer.user}/Documents/GITREPOS/ytmusic/yt_music_record.py',
                 'mpqtile'
                 ],stdout=sp.PIPE, stderr=sp.DEVNULL)
        web_any = ytmusic.communicate()[0].decode().replace('\n','')

        if web_spotify.startswith('Web'):
            if web_spotify.endswith('1'):
                logger.warning(f"Recording from [Spotify @ {mediaplayer.title()}]")
                record = sp.Popen(
                        [f'/home/{MusicPlayer.user}/Documents/GITREPOS/SpotifyAudioRecorded/.venv/bin/python',
                         f'/home/{MusicPlayer.user}/Documents/GITREPOS/SpotifyAudioRecorded/recording_spotify_track.py'],
                        stderr=sp.DEVNULL)
                return

            elif web_spotify.endswith('0'):
                if web_any == 'Playing':
                    logger.warning(f"Recording from [{mediaplayer.title()}]")
                    record = sp.Popen(
                            [f'/home/{MusicPlayer.user}/Documents/GITREPOS/ytmusic/.venv/bin/python',
                             f'/home/{MusicPlayer.user}/Documents/GITREPOS/ytmusic/yt_music_record.py'],
                            stderr=sp.DEVNULL)
                    return

            elif web_spotify.endswith('2'):
                if web_any in ('Playing','Paused'):
                    logger.warning(f"Recording from [{mediaplayer.title()}]")
                    record = sp.Popen(
                            [f'/home/{MusicPlayer.user}/Documents/GITREPOS/ytmusic/.venv/bin/python',
                             f'/home/{MusicPlayer.user}/Documents/GITREPOS/ytmusic/yt_music_record.py'],
                            stderr=sp.DEVNULL)
                    return
            logger.warning(f"Recording from [Spotify @ {mediaplayer.title()}]")
            record = sp.Popen(
                    [f'/home/{MusicPlayer.user}/Documents/GITREPOS/SpotifyAudioRecorded/.venv/bin/python',
                     f'/home/{MusicPlayer.user}/Documents/GITREPOS/SpotifyAudioRecorded/recording_spotify_track.py'],
                    stderr=sp.DEVNULL)
            return

        if mediaplayer in ('chromium', 'firefox'):
            logger.warning(f"Recording from [{mediaplayer.title()}]")
            record = sp.Popen(
                    [f'/home/{MusicPlayer.user}/Documents/GITREPOS/ytmusic/.venv/bin/python',
                    f'/home/{MusicPlayer.user}/Documents/GITREPOS/ytmusic/yt_music_record.py'],
                    stderr=sp.DEVNULL)
        else:
            logger.warning(f"Recording from [{mediaplayer.title()}]")
            record = sp.Popen(
                    [f'/home/{MusicPlayer.user}/Documents/GITREPOS/SpotifyAudioRecorded/.venv/bin/python',
                     f'/home/{MusicPlayer.user}/Documents/GITREPOS/SpotifyAudioRecorded/recording_spotify_track.py'],
                    stderr=sp.DEVNULL)

        return
