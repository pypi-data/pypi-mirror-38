import os
from ctrlf import main_class
class command_main:
    def __init__(self):
        self.argv    = os.sys.argv
        print(self.argv)
        self.option  = self.argv[1]
        self.options = {
                '-o':self.omatch,
                '-d':self.dmatch,
                '-h':self.help
                }
        ret = self.options.get(self.option,self.unknown)
        ret()

    def unknown(self):
        print("unknow option...")

    def omatch(self):
        '''
        -o <match_pattern> <path>                 :: find all that matches a <match_pattern> in <path>
                                                     if <path> is not given the current directory is
                                                     used
        '''
        opat   = self.argv[2]
        dire   = self.argv[3] if len(self.argv ) == 4 else None
        main_class(opat,dire)

    def dmatch(self):
        """
        -d <match_pattern> <reject_pattern <path> :: find all that matches a <match_pattern> in <path>
                                                     and doesnot match <reject_pattern>
                                                     if <path> is not given the current directory is

        """
        opat  = self.argv[2]
        dpat  = self.argv[3]
        dire  = self.argv[4] if len(self.argv ) == 5 else None
        main_class(opat,dire,dpat)

    def help(self):
        """
        -h                                        :: show this help message
        """
        for key in self.options:
            print(self.options[key].__doc__)
