#! /usr/bin/python3

#	DropFilter.py
Version   =   0.6

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
        December  2022     |||
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
    def __init__(self, path: str, title: str, version, console = False, notify = False, icon = ''):
        self.title = title
        # self.subtitle = ''    # for future Log organization
        self.version = version
        self.console = console
        self.notify = notify
        self.icon = icon
        self.file = path + time.asctime() + '.txt'

        self.make()
    

    # #   Singleton implementation
    # def __new__(self, *args, **kwargs):
    #     if not hasattr(Log, "_instance"):
    #         with Log._instance_lock:
    #             if not hasattr(Log, "_instance"):
    #                 Log._instance = object.__new__(self)  
    #     return Log._instance


    def make(self):
        #   Make [home]/.dropfilter/logs/
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


    #   Logs neutral message
    def log(self, message: str, newNotify = False):
        text = '~ | ' + time.asctime() + ' |: ' + message

        self << text

        if(self.console):
            print(text)

        if(self.notify):
            if(newNotify):
                self.notify = Notify.Notification.new(self.title, message, self.icon)
            else:
                self.notify.update(self.title, message, self.icon)
            self.notify.show()


    #   Logs Informative message
    def info(self, message: str, subtitle: str, newNotify = True):
        self << '¡ ' + subtitle + ' | ' + time.asctime() + ' |: ' + message

        if(self.console):
            print('\033[0;1;30;47m ¡ ' + subtitle + ' \033[2;7;37m \033[0m | ' + time.asctime() + ' |: ' + message)

        if(self.notify):
            if(newNotify):
                self.notify = Notify.Notification.new(subtitle, message, self.icon)
            else:
                self.notify.update(subtitle, message, self.icon)
            self.notify.show()


    #   Logs Warning message
    def warn(self, message: str, subtitle: str, newNotify = True):
        self << '/!\\ ' + subtitle + ' | ' + time.asctime() + ' |: ' + message

        if(self.console):
            print('\033[0;5;1;30;43m /!\\ ' + subtitle + ' \033[2;7;33m \033[0m | ' + time.asctime() + ' |: ' + message)

        if(self.notify):
            if(newNotify):
                self.notify = Notify.Notification.new('⚠️ ' + subtitle, message, self.icon)
            else:
                self.notify.update('⚠️ ' + subtitle, message, self.icon)
            self.notify.show()


    #   Logs Failure message
    def error(self, message: str, subtitle = '', newNotify = True):
        self << 'ERROR ' + subtitle + ' | ' + time.asctime() + ' |: ' + message

        if(self.console):
            print('\033[0;1;30;41m ERROR ' + subtitle + ' \033[2;7;31m \033[0m | ' + time.asctime() + ' |: ' + message)

        if(self.notify):
            if(newNotify):
                self.notify = Notify.Notification.new('ERROR ' + subtitle, message, self.icon)
            else:
                self.notify.update('ERROR ' + subtitle, message, self.icon)
            self.notify.show()



class Config:
    dir     = os.getenv('HOME') + '/.dropfilter'


    def __init__(self, configName = 'config', log: Log = None):
        self.log  = log if log else Log(Config.dir + '/logs/', str(configName).capitalize(), Version, False, False)
        self.name = configName
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

                        'Directory':{   'DropFilter':   os.getenv('HOME') + '/.dropfilter',
                                        'Dropbox':      os.getenv('HOME') + '/Dropbox',
                                        'Desktop':      GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP),
                                        'Downloads':    GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD)    },

                        'Filter':   [   [['Desktop'],   'PDF',  'DropFilter'],
                                        [['Downloads'], 'Code', 'DropFilter']   ]   }

        #   Config file
        print('\nChecking configuration file...\n\n')
        if(not self.make()):
            time.sleep(1)
            self.log.log('config.json found.')
            self.load()


    #   Create config file when it don't exists
    def make(self):
        try:
            with open(str(Config.dir) + '/' + self.name + '.json', 'xt') as config:                    
                config.write(json.dumps(self.dict))
                config.close()

                time.sleep(1)
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
                    self.log.log(self.name + '.json saved.')
        
        except FileNotFoundError:
            with open(str(Config.dir) + '/' + self.name + '.json', 'w') as config:
                config.write(json.dumps(self.dict))
                config.close()
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

                self.log << '\nConfig File: ' + json.dumps(configjson)

                try:
                    self.dict['SleepTime'] = configjson['SleepTime']
                    loaded += 1
                except KeyError:
                    self.log.warn(self.name + '.json does not have a "SleepTime" key', 'KeyError', False)
                
                try:
                    self.dict['File'] = configjson['File']
                    loaded += 1
                except KeyError:
                    self.log.warn(self.name + '.json does not have a "File" key', 'KeyError', False)
                
                try:
                    self.dict['Directory'] = configjson['Directory']
                    loaded += 1
                except KeyError:
                    self.log.warn(self.name + '.json does not have a "Directory" key', 'KeyError', False)
                
                try:
                    self.dict['Filter'] = configjson['Filter']
                    loaded += 1
                except KeyError:
                    self.log.warn(self.name + '.json does not have a "Filter" key', 'KeyError', False)

                if(not loaded):
                    self.log.warn("Configuration Couldn't be Loaded", 'ConfigFile Error', True)
                elif(loaded < 4):
                    self.log.info('SleepTime: ' + str(self.sleepTime()) + 's.\n', 'Configuration Partially Loaded', True)
                else:
                    self.log.info('SleepTime: ' + str(self.sleepTime()) + 's.\n', 'Configuration Loaded', False)

                config.close()
                return loaded == 4

        except FileNotFoundError:
            self.log.warn(self.name + '.json not found', self.name.capitalize(), False)
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
    log     = Log(Config.dir + '/logs/', 'DropFilter', Version, True, True, '/usr/share/icons/hicolor/scalable/apps/DropFilter_icon.svg')
    config  = Config(log = log)


    def __init__(self, config = ''):

        #   Main config file
        if(not config):
            self.config = DropFilter.config
        else:
            self.config = Config(config)
            DropFilter.log.info('New DropFilter instance initialized', config)

        #   Log.__init__() already makes /.dropfilter and /.dropfilter/tmp directories when they don't exist


    #   Scan Source directory only
    def scan(self, source, f):
        filter = f
        for file in os.listdir(source):
            #   File ends with
            for end in self.config.files()[filter[1]]:
                if(file.endswith(end)):

                    try:
                        filter[2] = self.config.directories()[f[2]]

                    finally:
                        #   Recursive make directory if destination don't exists
                        if(not os.path.exists(filter[2])):
                            mkdir(filter[2])
                        os.system('mv -n "' + source + '/' + file + '" "' + filter[2] + '/' + file + '"')

                        DropFilter.log.info(file + ' moved to "' + filter[2], 'File Moved')


    #   Verify existence of files to been filtered
    def verify(self):
        #   Probably I'll rewrite this sequence, again...
        for filter in self.config.filters():
            for s in filter[0]:
                source = s

                try:
                    source = self.config.directories()[s]

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
