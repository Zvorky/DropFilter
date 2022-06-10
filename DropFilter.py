#! /usr/bin/python3

#	DropFilter.py
#   Version 0.4

#	~ Enzo 'Zvorky' Delevatti
#	June 2022


import time
import os
from gi.repository import Notify


SleepTime = 20; #Seconds
DropDir   = ["/home/zvorky/Dropbox", "/home/zvorky/Área de Trabalho", "/home/zvorky/Dropbox/zvk-here", "/home/zvorky/Downloads"]
FilterDir = [[[0,1],[".cpp",".h",".py",".sh"],"/home/zvorky/Dropbox/Documentos/Projetinhos/Coding"],
            [[0],[".pdf"],"/home/zvorky/Dropbox/Livros"],
            [[2],[""],"/home/zvorky/Downloads"],
            [[3],[".pdf"],"/home/zvorky/Downloads/PDFs"],
            [[3],[".mp4",".mkv",".webm",".mov"],"/home/zvorky/Downloads/Media/Vídeos"],
            [[3],[".mp3",".ogg"],"/home/zvorky/Downloads/Media/Áudios"],
            [[3],[".gif",".pgn",".jpeg","jpg"],"/home/zvorky/Downloads/Media/Imagens"],
            [[3],[".zip",".rar",".tar",".gz",".xz",".tgz",".jar",".deb",".qdz",".run",".exe",".rpm"],"/home/zvorky/Downloads/Compactados"],
            [[3],[".odt",".odp",".ods",".odf",".doc",".docx",".ppt",".pptx"],"/home/zvorky/Downloads/Office"]]

if __name__ == '__main__':
    Notify.init("DropFilter")

    while True:

        for dir in DropDir:
            for file in os.listdir(dir):
                for filter in FilterDir:
                    for i in filter[0]:
                        if(dir == DropDir[i]):
                            for end in filter[1]:
                                if(file.endswith(end)):
                                    print(file + " found at \"" + dir + "\", moving it...")
                                    os.system("mv \"" + dir + "/" + file + "\" \"" + filter[2] + "/" + file + "\"")
                                    print(file + " moved to \"" + filter[2] + "\".\n")
                                    moved = Notify.Notification.new(file, "moved to \"" + filter[2] + "\"", "/home/zvorky/Dropbox/Documentos/Projetinhos/Coding/DropFilter/DropFilter.svg")
                                    moved.show()

        time.sleep(SleepTime)
