#! /usr/bin/python3

#	DropFilter.py
#   Version 0.6

#	~ Enzo 'Zvorky' Delevatti
#	June 2022

#   Recursive make directory
def mkdir(dir: str):
    if(not os.path.exists(dir[0:dir.rfind('/')])):
        mkdir(dir[0:dir.rfind('/')])
    os.system("mkdir \"" + dir + "\"")
