# <p align="center"><img src="https://github.com/Zvorky/DropFilter/blob/main/ArtWork/DropFilter_icon.svg" width="44" height="44"> DropFilter</p>


DropFilter is a Python project that simplifies file organization and movement within a directory based on customizable filtering criteria. This tool offers an efficient way to manage your files, helping you maintain order in your file system.  

| 🇺🇸 EN | [README](/README.md)    |
|-------|-------------------------|
| 🇧🇷 PT | [LEIAME](/README-PT.md) |
----

### <p align="center">Key Features</p>

- **Customizable File Filtering:** DropFilter allows you to configure filtering rules based on various criteria such as file name, type, and extension.

- **Automatic Organization:** Files that match the filtering criteria are automatically moved to specific directories, simplifying the organization of your files.

- **Flexible Configuration:** You can customize filtering rules, target directories, and other parameters in the configuration file.

- **Notifications and Logs:** DropFilter provides notifications and detailed logs to keep you informed about the actions taken.

----

### <p align="center">Basic Usage</p>

For DropFilter to start with the system, install it by running the "Install" script.

1. Once you run DropFilter, it will generate a default config file at .config/dropfilter.
2. Edit your config.json as you want, and save it.
3. DropFilter will automatically reload the config file, so it will already being monitoring the specified directory and automatically organize files based on your settings.

----

### <p align="center">Example Configuration</p>

You can define filtering rules and target directories in the JSON configuration file:

```json
{
  "SleepTime": 20,
  "File": {
    "Any": {
      "Contains": [""]
    },
    "Code": {
      "Ends": [".cpp", ".h", ".py", ".sh"]
    },
    "PDF": {
      "Ends": [".pdf"]
    },
    "Video": {
      "Ends": [".mp4", ".mkv", ".webm", ".mov"]
    }
  },
  "Directory": {
    "Dropbox": "/home/user/Dropbox",
    "Desktop": "/home/user/Desktop",
    "Downloads": "/home/user/Downloads",
    "PDF_DL": "/home/user/Downloads/PDF"
  },
  "Filter": [
    {
      "walk": [["Downloads"], "PDF", "PDF_DL"]
    },
    {
      "Only": [["Desktop"], "Code", "Dropbox"]
    }
  ]
}
```

#

**Note:** Ensure that the `gi.repository` library and required dependencies are installed for DropFilter to function correctly.

DropFilter is a versatile tool to assist in efficiently organizing and managing files. Customize your settings and let DropFilter take care of file organization for you.
