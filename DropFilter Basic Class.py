#  DropFilter Basic Class
#  (not officially implemented 👍)

#  Enzo 'Zvorky' Delevatti

class DropFilter:
  icon = "/usr/share/icons/hicolor/scalable/apps/DropFilter_icon.svg"
  configDir = os.getenv('HOME') + "/.dropfilter"
  config = "/config.json"
  log = ""
  
  # Default Config
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

  
  __init__(self, config):
    