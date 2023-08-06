#!/usr/bin/env python3
#
# Uses python-vlc   -> https://github.com/oaubert/python-vlc
#
# File              : shufflemilky.py
# Author            : Sam Uel <samuelfreitas@linuxmail.org>
# Date              : 30 dec 2016
# Last Modified Date: 25 nov 2018
# Last Modified By  : Sam Uel <samuelfreitas@linuxmail.org>
import tty
import vlc
import sys
from threading import Thread
from os.path import splitext
from getpass import getuser
from os import path, getcwd
from glob import glob
from random import shuffle
from time import sleep

vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()
volume = 100
player.audio_set_volume(volume)
no_playlist = False
AUDIO_FORMATS = ('.mp3', '.xm', '.mod', '.mid')
ARROWF = '\033[38;5;1m' # red foreground
ARROWB = '\033[48;5;1m' # red background

def get_playlist():
    playlist = [file for file in glob('*') if file.endswith(AUDIO_FORMATS)]

    if(len(playlist) == 0):
        print('\r\033[5m \033[m\033[31m\033[1m'\
            + ' Songs could not be found!'\
            + ' Press q to exit.\033[m\r\033[s', end='', flush=True)
        exit(1)
        no_playlist = True

    return playlist

def shuffle_player():
    playlist = get_playlist()
    last_song = ''

    while True:
        shuffle(playlist)

        if(playlist[0] == last_song):
            del playlist[0]
            playlist.append(last_song)

        for song in playlist:
            while True:
                sleep(1)
                if(player.is_playing() == 0):
                    media = vlc_instance.media_new(song)
                    player.set_media(media)
                    player.play()
                    print('\r\033[K\033[40m\033[97m\033[1m  '\
                        + f'\033[m\033[30m{ARROWB} {path.splitext(song)[0][:28]}...'\
                        + f'\033[m\033[40m{ARROWF}\033[m\033[s', end='', flush=True)
                    on_volume()
                    break
            last_song = song

def on_volume(vol = None):
    global volume

    if(vol):
        if(volume > 100): volume = 100
        if(volume < 0): volume = 0

        player.audio_set_volume(volume)

    print('\033[u\033[K\033[40m\033[97m\033[1m'
        + f'   {volume}% \033[m\033[30m\033[m', end='', flush=True)

def key_pressed():
    tty.setcbreak(sys.stdin.fileno())
    key = sys.stdin.read(1)
    return key

def player_control():
    global volume

    print(f'\033[40m\033[97m \033[1m \033[m\033[30m{ARROWB}'\
        + f'\033[30m {getuser()} \033[m\033[40m{ARROWF}'\
        + f'\033[40m\033[97m  \033[1m {path.basename(getcwd())}'\
        + ' \033[m\033[30m\033[m\n', end='', flush=True)
    print('\033[?25l', end='', flush=True)

    while True:
        key = key_pressed()
        if(key == 'q'):
            sys.stdout.write('\033[?25h \033[K \033[F')
            sys.stdout.flush()
            exit()
            break
        if(no_playlist): continue
        if(key == ','):
            volume -= 1
            on_volume(True)
        elif(key == '.'):
            volume += 1
            on_volume(True)

def main():
    control_thread = Thread(target=player_control)
    player_thread = Thread(target=shuffle_player, daemon=True)
    control_thread.start()
    player_thread.start()

if __name__ == '__main__':
    main()
