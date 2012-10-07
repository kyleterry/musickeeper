import os
from os.path import join, exists
import glob
import shutil

import id3reader

MUSIC_DIR = '/home/kyle/unsorted_music'
DESTINATION_DIR = '/home/kyle/Music'

def main():
    #import ipdb; ipdb.set_trace()
    for directory in os.walk(MUSIC_DIR):
        for _file in directory[2]:
            _file = join(directory[0], _file)
            try:
                reader = id3reader.Reader(_file)
            except IOError:
                continue
            if not reader.getValue('performer'):
                print 'ERROR: skipping %s' % _file
                continue
            artist_album = os.path.join(DESTINATION_DIR, 
                    reader.getValue('performer'),
                    reader.getValue('album'))
            track = reader.getValue('track')
            if '/' in track:
                track = track.split('/')[0]
            if len(track) == 1:
                track = '0%s' % track
            new_file_name = '%s - %s.mp3' % (
                track, reader.getValue('title').replace('/', ','))
            new_file_path = join(artist_album, new_file_name)
            if exists(new_file_path):
                continue
            try:
                os.makedirs(artist_album)
            except OSError:
                pass
            shutil.copy2(_file, new_file_path)
            print 'Made: %s' % os.path.join(artist_album, new_file_name)


if __name__ == '__main__':
    main()
