import os
import re
class main_class():
    def __init__(self,match,path = None,reject=None):
        if not path:
            path  = os.getcwd()
        os.chdir(path)
        pattern = re.compile(match)
        try:
            os.sys.stdout  = open('res.txt',"w")
            ok = True
        except Exception as exc:
            print(exc)
            ok = False
        dirs = set()
        files= set()
        for dirpath,dirnames,filenames in os.walk(os.getcwd()):
            for filename in filenames:
                if re.search(pattern,filename):
                    files.add((filename,dirpath))

            for dirname in dirnames:
                if re.search(pattern,dirname):
                    dirs.add((dirname,dirpath))

        if reject:
            self.reject = re.compile(reject)
            rejfun      = lambda  tupl :not re.search(self.reject,tupl[0])
            files       = filter(rejfun,files)
            dirs        = filter(rejfun,dirs)

        print('found files')
        for nm in files:
            print('{} --> {}'.format(nm[0],nm[1]))
        print('found directories...')
        for nm in dirs:
            print('{} --> {}'.format(nm[0],nm[1]))
        if ok:
            os.sys.stdout.close()
            os.system("res.txt")


