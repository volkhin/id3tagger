#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: add FLAC support
# TODO: add chmod + chown
# TODO: add logger

import sys
import os
import re
import mutagen, mutagen.id3

def process(folder):
    os.chdir(folder)
    folder = os.getcwd()
    walk_result = os.walk(folder)

    for f in walk_result:
        (dirpath, dirnames, filenames) = f
        args = dirpath[len(folder):].split('/')
        artist = 'Unknown' if (len(args) < 2) else args[1]
        album = 'Unknown' if (len(args) < 3) else args[2]
        print "Artist:", artist, ", album:", album
        for file in filenames:
            if file[-4:].lower() != '.mp3':
                continue
            title = file[:-4]
            fullpath = dirpath + "/" + file
            print title
            
            if (os.access(fullpath, os.R_OK | os.W_OK) == False):
                print 'Error: bad permissions on', fullpath
                continue

            #mutagen.id3.delete(fullpath)
            id3 = mutagen.id3.ID3()
            id3.add(mutagen.id3.TPE1(encoding = 3, text = artist.decode("utf-8")))
            id3.add(mutagen.id3.TALB(encoding = 3, text = album.decode("utf-8")))
            id3.add(mutagen.id3.TIT2(encoding = 3, text = title.decode("utf-8")))
            id3.save(fullpath)

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise Exception("Needs exactly 1 argument. Usage: id3tagger FOLDER")
        folder = sys.argv[1]
        if (os.access(folder, os.F_OK) == False):
            raise Exception("Folder \"" + folder + "\" doesn't exist!")
        if (os.access(folder, os.R_OK | os.W_OK | os.X_OK) == False):
            raise Exception("Bad permissions for folder \"" + folder + "\"!")
        process(folder)
    except Exception as e:
        print e
