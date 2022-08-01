#! /usr/bin/python3

#	DropFilter.py
#   Version 0.6

#	~ Enzo 'Zvorky' Delevatti
#	July 2022


import os, sys, time, json
from gi.repository import Notify, GLib

class DropFilter:
    icon = "/usr/share/icons/hicolor/scalable/apps/DropFilter_icon.svg"
    home = os.getenv('HOME')
    configDir = home + "/.dropfilter"
    config = "/config.json"
    log = ""

    def __init__(self, config = "/config.json"):
        Notify.init("DropFilter")
        self.ntf = Notify.Notification.new("DropFilter", "", DropFilter.icon)

        os.system("clear")
        print("=| DropFilter |=\nv0.6")

        #   Config
        print("\nChecking configuration files...\n\n")

        #   Home .dropfilter dir
        if(not os.path.exists(DropFilter.configDir)):
            log = DropFilter.configDir + " not found\n"
            self.ntf.update("DropFilter", DropFilter.configDir + " not found, creating.", DropFilter.icon)
            self.ntf.show()
            os.mkdir(DropFilter.configDir)
            log = log + DropFilter.configDir + " created.\n"
        else:
            log = DropFilter.configDir + " found.\n"
        print(log)

        #   Temp directory
        if(not os.path.exists(DropFilter.configDir + "/tmp")):
            os.mkdir(DropFilter.configDir + "/tmp")
            log = log + DropFilter.configDir + "/tmp created.\n"
            print(DropFilter.configDir + "/tmp created.")
        else:
            log = log + DropFilter.configDir + "/tmp found.\n"
            print(DropFilter.configDir + "/tmp found.")
        
        #   Log File        !!! needs to be closed o.o -----------------------------------------------------------------------------------
        logfile = DropFilter.configDir + "/tmp/" + time.asctime() + ".txt"
        os.system("touch \"" + logfile + "\"")
        logfile = open(logfile, "a")
        logfile.write("=| DropFilter Log - " + time.asctime() + " |=\nv0.6\n\n" + log)
        log = ""

        #   Main config file
        try:
            with open(DropFilter.configDir + "/config.json", "xt") as config:
                configjson = {  "SleepTime": 20,

                                "File": {   "Any": [""],
                                            "Code": [".cpp",".h",".py",".sh"],
                                            "PDF": [".pdf"],
                                            "Video": [".mp4",".mkv",".webm",".mov"],
                                            "Audio": [".mp3",".ogg",".wav"],
                                            "Image": [".gif",".pgn",".jpeg","jpg"],
                                            "Vector": [".svg", ".eps", ".ai", ".cdr"],
                                            "Compressed": [".zip",".rar",".tar",".gz",".xz",".tgz",".jar",".deb",".qdz",".run",".exe",".rpm"],
                                            "Document": [".odt",".odp",".ods",".odf",".doc",".docx",".ppt",".pptx"] },
                                
                                "Directory": {  "DropFilter": DropFilter.home + "/.dropfilter",
                                                "Dropbox": DropFilter.home + "/Dropbox",
                                                "Desktop": GLib.get_user_special_dir(GLib.USER_DIRECTORY_DESKTOP),
                                                "Downloads": GLib.get_user_special_dir(GLib.USER_DIRECTORY_DOWNLOAD)},
                                
                                "Filter": [ [["Desktop"],"PDF", "DropFilter"],
                                            [["Downloads"],"Code", "DropFilter"]]  }
                
                config.write(json.dumps(configjson))
                config.close()

                log = DropFilter.configDir + "/config.json created.\n"
                print(log)
                self.ntf.update("DropFilter", log, DropFilter.icon)
                self.ntf.show()
                log = log + "\nDefault Config: " + json.dumps(configjson)

        except FileExistsError:
            log = "config.json found.\n"

        logfile.write(time.asctime() + " |: " + log)
        logfile.close()
        DropFilter.log = logfile.name

        self.load(config)

        self.ntf.update("DropFilter", "v0.6 - " + config + " All ready, " + os.getenv('USER') + "!", DropFilter.icon)
        self.ntf.show()


    #   Load Config
    def load(self, config = "/config.json"):
        #   Reload Log
        logfile = open(log, "a")
        
        try:
            with open(DropFilter.configDir + config) as config:
                configjson = json.load(config)

                if(self.SleepTime != configjson["SleepTime"]):
                    self.SleepTime = configjson["SleepTime"]

                if(self.File != configjson["File"]):
                    self.File      = configjson["File"]

                if(self.Directory != configjson["Directory"]):
                    self.Directory = configjson["Directory"]

                if(self.Filter != configjson["Filter"]):
                    self.Filter    = configjson["Filter"]
                    log = "\nConfig File: " + json.dumps(configjson)
                    logfile.write(time.asctime() + " |: " + log)

                    print(log)
                    self.ntf.update("Configuration Loaded", "SleepTime: " + str(self.SleepTime) + "s.", DropFilter.icon)
                    self.ntf.show()
                    log = ""
        
        finally:
            config.close()
    

    def verify(self, config = "/config.json"):
        # global SleepTime, File, Directory, Filter, icon, configDir, log

        #   Reload Log
        logfile = open(log, "a")

        for filter in self.Filter:
            for source in filter[0]:
                try:
                    source = self.Directory[source]

                finally:
                    if(os.path.exists(source)):
                        for file in os.listdir(source):
                            for end in self.File[filter[1]]:
                                if(file.endswith(end)):
                                    #   Notify and move the file to the Filtered directory
                                    print(file + " found at \"" + dir + "\", moving it...")
                                    try:
                                        filter[2] = self.Directory[filter[2]]

                                    finally:
                                        if(not os.path.exists(filter[2])):
                                            mkdir(filter[2])
                                        os.system("mv -n \"" + self.Directory[dir] + "/" + file + "\" \"" + filter[2] + "/" + file + "\"")

                                        log = file + " moved to \"" + filter[2] + "\".\n"
                                        logfile.write(time.asctime() + " |: " + log)

                                        print(log)
                                        self.ntf.update(file, log, DropFilter.icon)
                                        self.ntf.show()
                                        log = ""

                    else:
                        log = source + " don't exists."
                        logfile.write(time.asctime() + " |: " + log)
                        print(log)
                        log = ""

        logfile.close()
        logfile = logfile.name
        time.sleep(self.SleepTime)
        return config


#   Recursive make directory
def mkdir(dir: str):
    if(not os.path.exists(dir[0:dir.rfind('/')])):
        mkdir(dir[0:dir.rfind('/')])
    os.system("mkdir \"" + dir + "\"")
