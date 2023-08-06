import os
import argparse
import re


class Renamer:

    def __init__(self):
        self.currentPath = os.getcwd()
        # self.currentPath = '/Users/george/lll/'
        self.oldPatten = ''
        self.newPatten = ''
        self.isPreview = False
        self.parser = argparse.ArgumentParser()
        self.parseInputs(self.parser)
        print('Working Path:' + self.currentPath)

    def update(self):
        files = os.listdir(self.currentPath)
        if(len(files) > 0):
            for file in files:
                if(os.path.isfile(os.path.join(self.currentPath, file))):
                    newfileName = re.sub(self.oldPatten, self.newPatten, file)
                    if not self.isPreview:
                        os.rename(os.path.join(self.currentPath, file),
                                  os.path.join(self.currentPath, newfileName))
                    print(file, ' ----> ', newfileName)

    def parseInputs(self, parser):
        parser.add_argument("old", help="specify old patten to remove")
        parser.add_argument("new", help="specify new patten you wanted")
        parser.add_argument("-p", "--preview", action="store_true",
                            help="This will show what the result will be.", default=False)
        args = parser.parse_args()
        if(args.old):
            self.oldPatten = args.old.strip()
        if(args.new):
            self.newPatten = args.new.strip()
        self.isPreview = args.preview
        # if(self.oldPatten == "" or self.newPatten == ""):
        #     print("You haven't spcify valid parameters, use --help for usage")
        #     os._exit(1)
