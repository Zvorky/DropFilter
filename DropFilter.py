#! /usr/bin/python3

#	DropFilter.py
#   Version 0.6

#	~ Enzo 'Zvorky' Delevatti
#	July 2022


import os, sys, time, json
from gi.repository import Notify, GLib
import DropFilter_lib


configDir = os.getenv('HOME') # temporarily home

#   Default Config
SleepTime = 20; #Seconds

File      = {"Any": [""],
            "Code": [".cpp",".h",".py",".sh"],
            "PDF": [".pdf"],
            "Video": [".mp4",".mkv",".webm",".mov"],
            "Audio": [".mp3",".ogg",".wav"],
            "Image": [".gif",".pgn",".jpeg","jpg"],
            "Vector": [".svg", ".eps", ".ai", ".cdr"],
            "Compressed": [".zip",".rar",".tar",".gz",".xz",".tgz",".jar",".deb",".qdz",".run",".exe",".rpm"],
            "Document": [".odt",".odp",".ods",".odf",".doc",".docx",".ppt",".pptx"]}

Directory = {"DropFilter": configDir + "/.dropfilter",
            "Dropbox": configDir + "/Dropbox",
            "Desktop": GLib.get_user_special_dir(GLib.USER_DIRECTORY_DESKTOP),
            "Downloads": GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOWNLOAD)}

Filter =    [[["Desktop"],"PDF", "DropFilter"],
            [["Downloads"],"Code", "DropFilter"]]

#   DropFilter
icon = "/usr/share/icons/hicolor/scalable/apps/DropFilter_icon.svg"
configDir = configDir + "/.dropfilter"
config = "/config.json"
log = ""



def verify(config = "/config.json"):
    global SleepTime, File, Directory, Filter, icon, configDir, log

    #   Reload Log
    logfile = open(log, "a")

    #   Load Config
    try:
        with open(configDir + config) as config:
            configjson = json.load(config)

            if(SleepTime != configjson["SleepTime"]):
                SleepTime = configjson["SleepTime"]

            if(File != configjson["File"]):
                File      = configjson["File"]

            if(Directory != configjson["Directory"]):
                Directory = configjson["Directory"]

            if(Filter != configjson["Filter"]):
                Filter    = configjson["Filter"]
                log = "\nConfig File: " + json.dumps(configjson)
                logfile.write(time.asctime() + " |: " + log)

                print(log)
                ntf.update("Configuration Loaded", "SleepTime: " + str(SleepTime) + "s.", icon)
                ntf.show()
                log = ""
    finally:
        config.close()

    for filter in Filter:
        for source in filter[0]:
            try:
                source = Directory[source]

            finally:
                if(os.path.exists(source)):
                    for file in os.listdir(source):
                        command = "mv \""

                            for end in File[filter[1]]:
                                if(file.endswith(end)):
                                    #   Notify and move the file to the Filtered directory
                                    print(file + " found at \"" + dir + "\", moving it...")
                                    try:
                                        filter[2] = Directory[filter[2]]

                                    finally:
                                        if(not os.path.exists(filter[2])):
                                            mkdir(filter[2])
                                        os.system("mv -n \"" + DropDir[dir] + "/" + file + "\" \"" + filter[2] + "/" + file + "\"")

                                        log = file + " moved to \"" + filter[2] + "\".\n"
                                        logfile.write(time.asctime() + " |: " + log)

                                        print(log)
                                        ntf.update(file, log, icon)
                                        ntf.show()
                                        log = ""

                else:
                    log = source + " don't exists."
                    logfile.write(time.asctime() + " |: " + log)
                    print(log)
                    log = ""

    logfile.close()
    logfile = logfile.name
    time.sleep(SleepTime)
    return config



if __name__ == '__main__':
    Notify.init("DropFilter")
    ntf = Notify.Notification.new("DropFilter", "", icon)

    os.system("clear")
    print("=| DropFilter |=\nv0.6")

    #   Config
    print("\nChecking configuration files...\n\n")

    #   Home .dropfilter dir
    if(not os.path.exists(configDir)):
        log = configDir + " not found\n"
        ntf.update("DropFilter", configDir + " not found, creating.", icon)
        ntf.show()
        os.mkdir(configDir)
        log = log + configDir + " created.\n"
    else:
        log = configDir + " found.\n"
    print(log)

    #   Temp directory
    if(not os.path.exists(configDir + "/tmp")):
        os.mkdir(configDir + "/tmp")
        log = log + configDir + "/tmp created.\n"
        print(configDir + "/tmp created.")
    else:
        log = log + configDir + "/tmp found.\n"
        print(configDir + "/tmp found.")

    #   Log File        !!! needs to be closed o.o
    logfile = configDir + "/tmp/" + time.asctime() + ".txt"
    os.system("touch \"" + logfile + "\"")
    logfile = open(logfile, "a")
    logfile.write("=| DropDir Log - " + time.asctime() + " |=\nv0.6\n\n" + log)
    log = ""

    #   Main config file
    try:
        with open(configDir + "/config.json", "xt") as config:
            configjson = {"SleepTime": SleepTime, "File": File, "DropDir": DropDir, "FilterDir": FilterDir}
            config.write(json.dumps(configjson))
            config.close()

            log = configDir + "/config.json created.\n"
            print(log)
            ntf.update("DropFilter", log, icon)
            ntf.show()
            log = log + "\nDefault Config: " + json.dumps(configjson)

    except FileExistsError:
        log = "config.json found.\n"

    logfile.write(time.asctime() + " |: " + log)
    logfile.close()
    log = logfile.name

    ntf.update("DropFilter", "v0.6 - All ready, " + os.getenv('USER') + "!", icon)
    ntf.show()

    while True:
        config = verify(config)
