#! /usr/bin/python3

#	DropFilter.py
Version   =   0.7

''' Enzo Zavorski Delevatti
||| @Zvorky
\\\          ___,
 \\\      .~´    `-,
  \\°    /  _    _ \.
   \°   ,\`|_|''|_|´\
    °    /          /)   °
        (\  ,    , .\`   |°
         `) ;`,; `,^,)   ||°
         ´,´  `,  `  `   |||
                          \\\
        September 2023     |||
                           '''



import os, sys, time, json
from gi.repository import Notify, GLib



#   Recursive make directory
def mkdir(dir: str):
    if(not dir.rfind('/')):
        dir += '/'

    if(not os.path.exists(dir[0:dir.rfind('/')])):
        mkdir(dir[0:dir.rfind('/')])

    if(not os.path.exists(dir)):
        os.system('mkdir "' + dir + '"')



#   Logger with Notify implementation
class Log:
    path = ''
    def __init__(self, path: str, title: str, version, console = False, notify = False, icon = ''):
        self.title = title
        self.subtitle = title
        self.version = version
        self.console = console
        self.notify = notify
        self.icon = icon
        self.file = path + time.asctime() + '.txt'

        Log.path = path

        self.make()


    def make(self):
        #   Make [home]/.log/dropfilter/
        mkdir(self.file[0:self.file.rfind('/')])
        os.system('touch "' + self.file + '"')

        text = '=| {} Log - {} |=\nVersion {}\n\n{}\nNotify: {}\n\n'.format(self.title, time.asctime(), self.version, self.file, self.notify)
        self << text    #   Append

        if(self.notify):
            Notify.init(self.title)
            self.notify = Notify.Notification.new(self.title, 'v{} started!...'.format(self.version), self.icon)
            self.notify.show()

        if(self.console):
            os.system('clear')
            print(text)


    #   Append to log file
    def __lshift__(self, text: str):
        try:
            with open(self.file, 'a') as log:
                log.write(text + '\n')
                log.close()
        
        except FileNotFoundError:
            self.make()
            self << text
    

    #   Set Subtitle
    def __sub__(self, subtitle: str):
        # if(not subtitle):
        #     self.subtitle = self.title
        #     return
        
        if(subtitle and self.subtitle != subtitle):
            self.subtitle = subtitle
            self << '\n -| ' + subtitle + ' |-'
            print  ('\n\033[0;1;30;47m -| ' + subtitle + ' |-\033[2;7;37m \033[0m ')


    #   Logs neutral message
    def log(self, message: str, newNotify = False):
        text = '       | ' + time.asctime() + ' |: ' + message

        self << text

        if(self.console):
            print(text)

        if(self.notify):
            if(newNotify):
                self.notify = Notify.Notification.new(self.subtitle, message, self.icon)
            else:
                self.notify.update(self.subtitle, message, self.icon)
            self.notify.show()


    #   Logs Informative message
    def info(self, message: str, subtitle = '', newNotify = True):
        self - subtitle
        self << 'info   | ' + time.asctime() + ' |: ' + message

        if(self.console):
            print('\033[0;1;30;47m ¡    \033[2;7;37m \033[0m| ' + time.asctime() + ' |: ' + message)

        if(self.notify):
            if(newNotify):
                self.notify = Notify.Notification.new(self.subtitle, message, self.icon)
            else:
                self.notify.update(self.subtitle, message, self.icon)
            self.notify.show()


    #   Logs Warning message
    def warn(self, message: str, subtitle = '', newNotify = True):
        self - subtitle
        self << 'warn   | ' + time.asctime() + ' |: ' + message

        if(self.console):
            print('\033[0;5;1;30;43m/!\\   \033[2;7;33m \033[0m| ' + time.asctime() + ' |: ' + message)

        if(self.notify):
            if(newNotify):
                self.notify = Notify.Notification.new('⚠️ ' + self.subtitle, message, self.icon)
            else:
                self.notify.update('⚠️ ' + self.subtitle, message, self.icon)
            self.notify.show()


    #   Logs Failure message
    def error(self, message: str, subtitle = '', newNotify = True):
        self - subtitle
        self << 'ERROR | ' + time.asctime() + ' |: ' + message

        if(self.console):
            print('\033[0;1;30;41m ERROR | ' + time.asctime() + ' |:\033[2;7;31m \033[0m' + message)

        if(self.notify):
            if(newNotify):
                self.notify = Notify.Notification.new(self.subtitle + ' ERROR', message, self.icon)
            else:
                self.notify.update(self.subtitle + ' ERROR', message, self.icon)
            self.notify.show()
    
    
    #   Move the log folder to trash
    def trash():
        os.system('gio trash ' + Log.path)



class Config:
    dir = os.getenv('HOME') + '/.config/dropfilter'


    def __init__(self, configName = 'config', log: Log = None):
        self.name = configName
        if(configName == 'config'):
            configName = 'Dropfilter'
        self.log  = log
        self.dict = {   'SleepTime':    20,

                        'File':     {   'Any':          [''],
                                        'Code':         ['.cpp','.h','.py','.sh'],
                                        'PDF':          ['.pdf'],
                                        'Video':        ['.mp4','.mkv','.webm','.mov'],
                                        'Audio':        ['.mp3','.ogg','.wav'],
                                        'Image':        ['.gif','.pgn','.jpeg','jpg'],
                                        'Vector':       ['.svg', '.eps', '.ai', '.cdr'],
                                        'Compressed':   ['.zip','.rar','.tar','.gz','.xz','.tgz','.jar','.deb','.qdz','.run','.exe','.rpm'],
                                        'Document':     ['.odt','.odp','.ods','.odf','.doc','.docx','.ppt','.pptx']         },

                        'Directory':{   'Dropbox':      os.getenv('HOME') + '/Dropbox',
                                        'Desktop':      GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP),
                                        'Downloads':    GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD),
                                        'PDF_DL':       GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD) + '/PDF'   },

                        'Filter':   [   [['Desktop'],   'PDF', 'PDF_DL'],
                                        [['Downloads'], 'PDF', 'PDF_DL']   ]   }

        if(self.log):
            self.log - configName.capitalize()
        
        #   Config file
        if(not self.make()):
            time.sleep(1)
            if(self.log):
                self.log.log('config.json found.')
            self.load()


    #   Create config file when it don't exists
    def make(self):
        mkdir(Config.dir)
        try:
            with open(str(Config.dir) + '/' + self.name + '.json', 'xt') as config:                    
                config.write(json.dumps(self.dict))
                config.close()

                time.sleep(1)
                if(self.log):
                    self.log.log(str(Config.dir) + '/' + self.name + '.json created.')
                return True

        except FileExistsError:
            return False
    

    #   save actual config into file
    def save(self):
        try:
            with open(str(Config.dir) + '/' + self.name + '.json') as config:
                configjson = json.load(config)

                configjson['SleepTime'] = self.dict['SleepTime']
                configjson['File']      = self.dict['File']
                configjson['Directory'] = self.dict['Directory']
                configjson['Filter']    = self.dict['Filter']

                config.close()

                with open(str(Config.dir) + '/' + self.name + '.json', 'w') as config:
                    config.write(json.dumps(configjson))
                    config.close()
                    if(self.log):
                        self.log.log(self.name + '.json saved.')
        
        except FileNotFoundError:
            with open(str(Config.dir) + '/' + self.name + '.json', 'w') as config:
                config.write(json.dumps(self.dict))
                config.close()
                if(self.log):
                    self.log.log(self.name + '.json saved.')

    
    #   Loads a config file into config.dict
    def load(self, config = ''):
        if(config):
            self.name = config

        try:
            with open(str(Config.dir) + '/' + str(self.name) + '.json') as config:
                configjson = json.load(config)
                loaded     = 0

                if(self == configjson):
                    config.close()
                    return True

                if(self.log):
                    self.log << '\nConfig File: ' + json.dumps(configjson)

                try:
                    self.dict['SleepTime'] = configjson['SleepTime']
                    loaded += 1
                except KeyError:
                    if(self.log):
                        self.log.warn(self.name + '.json does not have a "SleepTime" key', False)
                
                try:
                    self.dict['File'] = configjson['File']
                    loaded += 1
                except KeyError:
                    if(self.log):
                        self.log.warn(self.name + '.json does not have a "File" key', False)
                
                try:
                    self.dict['Directory'] = configjson['Directory']
                    loaded += 1
                except KeyError:
                    if(self.log):
                        self.log.warn(self.name + '.json does not have a "Directory" key', False)
                
                try:
                    self.dict['Filter'] = configjson['Filter']
                    loaded += 1
                except KeyError:
                    if(self.log):
                        self.log.warn(self.name + '.json does not have a "Filter" key', False)

                if(not loaded):
                    if(self.log):
                        self.log.error("Configuration Couldn't be Loaded", True)
                elif(loaded < 4):
                    if(self.log):
                        self.log.warn('Configuration Partially Loaded, SleepTime: ' + str(self.sleepTime()) + 's.', True)
                else:
                    if(self.log):
                        self.log.info('Configuration Loaded, SleepTime: ' + str(self.sleepTime()) + 's.', False)

                config.close()
                return loaded == 4

        except FileNotFoundError:
            if(self.log):
                self.log.warn(self.name + '.json not found', False)
            return False
    

    #   Equals dictionary
    def __eq__(self, another: dict):
        try:
            if(self.dict['SleepTime'] != another['SleepTime']):
                return False
            if(self.dict['File']      != another['File']):
                return False
            if(self.dict['Directory'] != another['Directory']):
                return False
            if(self.dict['Filter']    != another['Filter']):
                return False
            return True
        except KeyError:
            return False


    def sleepTime(self):
        return self.dict['SleepTime']
    
    def files(self):
        return self.dict['File']
    
    def directories(self):
        return self.dict['Directory']
    
    def filters(self):
        return self.dict['Filter']



#   Main DropFilter Class
class DropFilter:
    #       Global DropFilter attributes
    log     = Log(os.getenv('HOME') + '/.log/dropfilter/', 'DropFilter', Version, True, True, '/usr/share/icons/hicolor/scalable/apps/DropFilter_icon.svg')
    config  = Config(log = log)


    def __init__(self, config = ''):

        #   Main config file
        if(not config):
            self.config = DropFilter.config
        else:
            self.config = Config(config)
            DropFilter.log.info('New DropFilter instance initialized', config.capitalize())

        #   Log.__init__() already makes /.config/dropfilter/ and /.log/dropfilter/ directories when they don't exist


    #   Scan Source directory only
    def scan(self, source, filter):
        for file in os.listdir(source):
            #   File ends with
            for end in self.config.files()[filter[1]]:
                if(file.endswith(end)):

                    try:
                        target = self.config.directories()[filter[2]]
                    
                    except:
                        target = filter[2]

                    finally:
                        #   Recursive make directory if destination don't exists
                        if(not os.path.exists(target)):
                            mkdir(target)
                        os.system('mv -n "' + source + '/' + file + '" "' + target + '/' + file + '"')

                        DropFilter.log.info(file + ' moved to ' + target, 'File Moved')


    #   Verify existence of directories to been filtered
    def verify(self):
        #   Probably I'll rewrite this sequence, again...
        for filter in self.config.filters():
            for s in filter[0]:
                
                try:
                    source = self.config.directories()[s]

                except:
                    source = s

                finally:
                    #   Path existence
                    if(os.path.exists(source)):
                        self.scan(source, filter)

                    else:
                        DropFilter.log << source + " don't exists."


    #   Verification loop, count = -1 means infinite
    def loop(self, count = -1):
        while(count):
            if(not self.config.load()):
                self.config.save()
            
            self.verify()

            #   Countdown
            if(count > 0):
                count -= 1

            #   Wait if still in loop
            if(count):
                if(count >= 0):
                    print('Countdown: ' + count)
                time.sleep(self.config.sleepTime())



if __name__ == '__main__':
    main = DropFilter()
    main.loop()
