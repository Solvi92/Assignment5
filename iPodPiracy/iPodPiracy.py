from datetime import datetime
from collections import Counter
import itertools as it
import re
import urllib
from urllib import request as req
import json
import csv
import xml.etree.ElementTree as ET
from math import radians, cos, sin, asin, sqrt, pi
import os
import shutil
import stagger



def copyMusic(targetPath, sourcePath):
    for root, dir, files in os.walk(sourcePath):
        for file in files:
            try:
                tag = stagger.read_tag(os.path.join(root, file))
                album = tag.album.replace('/','').replace('\\', '').replace('?','').replace('*','')\
                    .replace(':','').replace('"','').replace('>','').replace('<','').replace('|','').strip()
                artist = tag.artist.replace('/','').replace('\\', '').replace('?','').replace('*','')\
                    .replace(':','').replace('"','').replace('>','').replace('<','').replace('|','').strip()
                songPath = os.path.join(targetPath, artist, album)
                if not os.path.exists(songPath):
                    os.makedirs(songPath)
                filename, extension = os.path.splitext(os.path.join(root,file))

                if tag.track:
                    newFileName = str(tag.track) + ' - ' + tag.title + extension
                else:
                    newFileName = tag.title + extension

                newFileName = newFileName.replace('/','').replace('\\', '').replace('?','').replace('*','')\
                    .replace(':','').replace('"','').replace('>','').replace('<','').replace('|','').strip()

                os.rename(os.path.join(root, file), os.path.join(root, newFileName))
                shutil.copy(os.path.join(root, newFileName), os.path.join(songPath, newFileName))
                os.rename(os.path.join(root, newFileName), os.path.join(root, file))
            except :
                pass

def main():
    print('   ###########################################\n'
          '   #                                         #\n'
          '   #      Welcome to iPod copy-er            #\n'
          '   #                                         #\n'
          '   #                                         #\n'
          '   ###########################################\n')
	
    #init globals
    superSorter = 1

    while superSorter != 0:

        sourceFolder = input('-> Input the complete path of the folder to copy\n')
        while not os.path.exists(os.path.abspath(sourceFolder)):
            sourceFolder = input('-> Must be a valid path, please try again \n')

        targetFolder = input('-> Input the complete path of the target folder \n')
        while not os.path.exists(os.path.abspath(targetFolder)):
            targetFolder = input('-> Must be a valid path, please try again \n')
        targetFolder = os.path.join(targetFolder, '_music')

        #targetFolder = r'C:\Users\Lenovo\Documents\GitHub\Assignment5\iPodPiracy\Target'
        #sourceFolder = r'C:\Users\Lenovo\Documents\GitHub\Assignment5\iPodPiracy\ipod'
        print('-> Copying...')
        copyMusic(targetFolder, sourceFolder)
        print('-> Done.')
        superSorter = input('Type 0 if you want to quit or type 1 to continue \n')
        while superSorter != '1' and superSorter != '0':
            superSorter = input('Wrong input please type 0 if you want to quit or type 1 to continue \n')
        superSorter = int(superSorter)
main()