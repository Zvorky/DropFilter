#! /usr/bin/python3

#	DropFilter.py
#   Version 0.6

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
    def __init__(self, path: str, title: str, version, console = True, notify = True, icon = ''):
        self.title = title
        # self.subtitle = ''    # for future Log organization
        self.version = version
        self.console = console
        self.notify = notify
        self.icon = icon
        self.file = path + time.asctime() + '.txt'

        text = '=| {} Log - {} |=\nv{}\n\n{}\nNotify: {}\n\n'.format(title, time.asctime(), version, self.file, notify)
        self << text    #   Create, Append and Close file

        if(notify):
            Notify.init(title)
            self.notify = Notify.Notification.new(title, 'v{} started!...'.format(version), icon)
            self.notify.show()

        if(console):
            os.system('clear')
            print(text)


    #   Append to log file
    def __lshift__(self, text: str):
        # try:
        #     with open(self.file, 'a') as log:
        #         log.write(text + '\n')
        #
        # except FileNotFoundError:

        #   Make [home]/.dropfilter/tmp/
        mkdir(self.file[0:self.file.rfind('/')])
        os.system('touch "' + self.file + '"')

        with open(self.file, 'a') as log:
            log.write(text + '\n')

        # finally:
        log.close()


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



#   Main DropFilter Class
class DropFilter:
    #   Global DropFilter attributes
    icon = '/usr/share/icons/hicolor/scalable/apps/DropFilter_icon.svg'
    home = os.getenv('HOME')
    configDir = home + '/.dropfilter'
    config = '/config.json'
    log = Log(configDir + '/tmp/', 'DropFilter', 0.6, True, True, icon)


    def __init__(self, config = ''):

        #   Main config file
        if(config == ''):
            config = DropFilter.config
        else:
            DropFilter.log.info('New DropFilter instance initialized', config[1:config.rfind('.')])

        self.config = config

        #   Log.__init__() already makes /.dropfilter and /.dropfilter/tmp directories when they don't exists

        #   Config file
        print('\nChecking configuration files...\n\n')

        #   Default configuration (when config file do not exists)
        self.SleepTime  = 20

        self.File       = { 'Any':          [''],
                            'Code':         ['.cpp','.h','.py','.sh'],
                            'PDF':          ['.pdf'],
                            'Video':        ['.mp4','.mkv','.webm','.mov'],
                            'Audio':        ['.mp3','.ogg','.wav'],
                            'Image':        ['.gif','.pgn','.jpeg','jpg'],
                            'Vector':       ['.svg', '.eps', '.ai', '.cdr'],
                            'Compressed':   ['.zip','.rar','.tar','.gz','.xz','.tgz','.jar','.deb','.qdz','.run','.exe','.rpm'],
                            'Document':     ['.odt','.odp','.ods','.odf','.doc','.docx','.ppt','.pptx'] }

        self.Directory  = { 'DropFilter':   DropFilter.home + '/.dropfilter',
                            'Dropbox':      DropFilter.home + '/Dropbox',
                            'Desktop':      GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DESKTOP),
                            'Downloads':    GLib.get_user_special_dir(GLib.UserDirectory.DIRECTORY_DOWNLOAD) }
        
        self.Filter     = [ [['Desktop'],   'PDF',  'DropFilter'],
                            [['Downloads'], 'Code', 'DropFilter'] ]

        #   Create default config file when not exists
        try:
            with open(DropFilter.configDir + '/config.json', 'xt') as config:
                configjson = {  'SleepTime':    self.SleepTime,
                                'File':         self.File,
                                'Directory':    self.Directory,
                                'Filter':       self.Filter     }

                config.write(json.dumps(configjson))
                config.close()

                time.sleep(2.5)
                DropFilter.log.log(DropFilter.configDir + '/config.json created.')

        except FileExistsError:
            time.sleep(2.5)
            DropFilter.log.log('config.json found.')

        #   Loads config to this instance
        self.load(config)


    #   Load Config
    def load(self, config = ''):

        if(config != ''):
            self.config = config

        #   Consistency missing
        try:
            with open(DropFilter.configDir + self.config) as config:
                configjson = json.load(config)

                #   Too much ifs :/
                if(self.SleepTime != configjson['SleepTime']):
                    self.SleepTime = configjson['SleepTime']

                if(self.File != configjson['File']):
                    self.File      = configjson['File']

                if(self.Directory != configjson['Directory']):
                    self.Directory = configjson['Directory']

                if(self.Filter != configjson['Filter']):
                    self.Filter    = configjson['Filter']
                    DropFilter.log << '\nConfig File: ' + json.dumps(configjson)
                    DropFilter.log.info('SleepTime: ' + str(self.SleepTime) + 's.', 'Configuration Loaded', True)
                    
                config.close()

        except FileNotFoundError:
            return False

        finally:
            return True


    #   Scan Source directory only
    def scan(self, source, filter):
        for file in os.listdir(source):
            #   File ends with
            for end in self.File[filter[1]]:
                if(file.endswith(end)):

                    try:
                        filter[2] = self.Directory[filter[2]]

                    finally:
                        #   Recursive make directory if destination don't exists
                        if(not os.path.exists(filter[2])):
                            mkdir(filter[2])
                        os.system('mv -n "' + source + '/' + file + '" "' + filter[2] + '/' + file + '"')

                        DropFilter.log.info(file + ' moved to "' + filter[2], 'File Moved')


    #   Verify existence of files to been filtered
    def verify(self):
        #   Probably I'll rewrite this sequence, again...
        for filter in self.Filter:
            for source in filter[0]:

                try:
                    source = self.Directory[source]

                finally:
                    #   Path existence
                    if(os.path.exists(source)):
                        self.scan(source, filter)

                    else:
                        DropFilter.log << source + " don't exists."


    #   Verification loop, count = -1 means infinite
    def loop(self, count = -1):
        while(count):
            if(not self.load()):
                DropFilter.log.warn(self.config + " not found, using last config", self.config[1:self.config.rfind('/')].capitalize())

            print(self.load())
            self.verify()

            #   Countdown
            if(count > 0):
                count -= 1

            #   Wait if still in loop
            if(count):
                print(count)
                time.sleep(self.SleepTime)



if __name__ == '__main__':
    main = DropFilter()
    main.loop()
