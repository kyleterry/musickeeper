import os
from os.path import join, exists
import shutil
import argparse

import id3reader

MUSIC_DIR = '/home/kyle/unsorted_music'
DESTINATION_DIR = '/home/kyle/Music'

def main():
    parser = argparse.ArgumentParser(
            description='Sorts music into Artist/Album/01 - Song Title.mp3 like structures')
    parser.add_argument('-s', '--source', dest='source_dir', required=True,
            help='Source directory (with the unsorted music in it)')
    parser.add_argument('-d', '--destination',
            dest='destination_dir', required=True,
            help='Destination directory (where the sorted music goes)')
    args = parser.parse_args()
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
