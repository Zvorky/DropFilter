#! /usr/bin/python3

#	DropFilter.py
#   Version 0.5

#	~ Enzo 'Zvorky' Delevatti
#	June 2022


import os, sys, time, json
from gi.repository import Notify, GLib



configDir = os.getenv('HOME') # temporarily home

#   Default Config
SleepTime = 20; #Seconds

Type      = {"Any": [""],
            "Code": [".cpp",".h",".py",".sh"],
            "PDF": [".pdf"],
            "Video": [".mp4",".mkv",".webm",".mov"],
            "Audio": [".mp3",".ogg"],
            "Image": [".gif",".pgn",".jpeg","jpg"],
            "Compressed": [".zip",".rar",".tar",".gz",".xz",".tgz",".jar",".deb",".qdz",".run",".exe",".rpm"],
            "Document": [".odt",".odp",".ods",".odf",".doc",".docx",".ppt",".pptx"]}

DropDir   = {"DropFilter": configDir + "/.dropfilter",
            "Dropbox": configDir + "/Dropbox",
            "Desktop": GLib.get_user_special_dir(GLib.USER_DIRECTORY_DESKTOP),
            "Downloads": GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOWNLOAD)}

FilterDir = [[["Desktop"],"PDF", configDir + "/.dropfilter"],
            [["Downloads"],"Code", configDir + "/.dropfilter"]]

#   DropFilter
icon = "/usr/share/icons/hicolor/scalable/apps/DropFilter_icon.svg"
configDir = configDir + "/.dropfilter"



if __name__ == '__main__':
    Notify.init("DropFilter")
    ntf = Notify.Notification.new("DropFilter", "", icon)

    os.system("clear")
    print("=| DropFilter |=\nv0.5")

    #   Config
    print("\nChecking configuration files...\n\n")

    #   Home .dropfilter dir
    if(not os.path.exists(configDir)):
        print(configDir + " not found, creating.")
        ntf.update("DropFilter", configDir + " not found, creating.", icon)
        ntf.show()
        os.mkdir(configDir)

    #   Main config file
    try:
        with open(configDir + "/config.json", "xt") as config:
            configjson = {"SleepTime": SleepTime, "Type": Type, "DropDir": DropDir, "FilterDir": FilterDir}
            config.write(json.dumps(configjson))
            config.close()

            print(configDir + "/config.json created.")
            ntf.update("DropFilter", configDir + "/config.json created.", icon)
            ntf.show()

    except FileExistsError:
        print("config.json found")


    ntf.update("DropFilter", "v0.5 - All ready, " + os.getenv('USER') + "!", icon)
    ntf.show()

    while True:

        #   Load Config
        try:
            with open(configDir + "/config.json") as config:
                configjson = json.load(config)
                SleepTime = configjson["SleepTime"]
                Type      = configjson["Type"]
                DropDir   = configjson["DropDir"]
                FilterDir = configjson["FilterDir"]
        finally:
            config.close()


        for dir in DropDir:
            for file in os.listdir(DropDir[dir]):
                for filter in FilterDir:
                    for source in filter[0]:
                        if(DropDir[dir] == DropDir[source]):
                            for end in Type[filter[1]]:
                                if(file.endswith(end)):
                                    print(file + " found at \"" + dir + "\", moving it...")
                                    os.system("mv \"" + DropDir[dir] + "/" + file + "\" \"" + filter[2] + "/" + file + "\"")
                                    print(file + " moved to \"" + filter[2] + "\".\n")
                                    ntf.update(file, "moved to \"" + filter[2] + "\"", icon)
                                    ntf.show()

        time.sleep(SleepTime)
