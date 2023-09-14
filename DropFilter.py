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
        os.system('mkdir -p "' + self.file[0:self.file.rfind('/')] + '"')
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

                        'File':     {   'Any':          {'Contains':['']},
                                        'Code':         {'Ends':    ['.cpp','.h','.py','.sh']},
                                        'PDF':          {'Ends':    ['.pdf']},
                                        'Video':        {'Ends':    ['.mp4','.mkv','.webm','.mov']},
                                        'Audio':        {'Ends':    ['.mp3','.ogg','.wav']},
                                        'Image':        {'Ends':    ['.gif','.pgn','.jpeg','jpg']},
                                        'Vector':       {'Ends':    ['.svg', '.eps', '.ai', '.cdr']},
                                        'Compressed':   {'Ends':    ['.zip','.rar','.tar','.gz','.xz','.tgz','.jar','.deb','.qdz','.run','.exe','.rpm']},
                                        'Document':     {'Ends':    ['.odt','.odp','.ods','.odf','.doc','.docx','.ppt','.pptx']}         },

                        'Directory':{   'Dropbox':      os.getenv('HOME') + '/Dropbox',
                                        'Desktop':      GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP),
                                        'Downloads':    GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD),
                                        'PDF_DL':       GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD) + '/PDF'   },

                        'Filter':   [  {'Walk':         [['Desktop'],   'PDF', 'PDF_DL'],
                                        'Only':         [['Downloads'], 'PDF', 'PDF_DL']}   ]   }

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
        os.sytem('mkdir -p "' + Config.dir + '"')
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


    #   File Action (By now, just Move without overwrite)
    def action(self, source: str, file: str, target: str):
        os.system('mv -n "' + source + '/' + file + '" "' + target + '/' + file + '"')
        DropFilter.log.info(file + ' moved to ' + target, 'File Moved')


    #   Scan Source directory only
    def scan(self, source, filter):
        for scan in filter:
            f = filter[scan]

            try:
                target = self.config.directories()[f[2]]    
            except:
                target = f[2]
            finally:
                #   Recursive make directory if destination don't exists
                if(not os.path.exists(target)):
                    os.sytem('mkdir -p "' + target + '"')
                
            for file in os.listdir(source):
                for criteria in self.config.files()[f[1]]:
                    for word in self.config.files()[f[1]]:
                        if(criteria == 'Contains'):
                            if(file.find(word) > -1):
                                self.action(source, file, target)
                        
                        elif(criteria == 'Starts'):
                            if(file.startswith(word)):
                                self.action(source, file, target)
                        
                        else:
                            if(file.endswith(word)):
                                self.action(source, file, target)


    def walk(self, source, filter):
        for dir in os.walk(source):
            self.scan(dir[0], filter)


    #   Verify existence of directories to been filtered
    def verify(self):
        for filter in self.config.filters():
            for scan in filter:
                for s in filter[scan][0]:
                    
                    try:
                        source = self.config.directories()[s]

                    except:
                        source = s

                    finally:
                        #   Path existence
                        if(os.path.exists(source)):
                            if(scan == 'Walk'):
                                self.walk(source, filter)
                            else:
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
