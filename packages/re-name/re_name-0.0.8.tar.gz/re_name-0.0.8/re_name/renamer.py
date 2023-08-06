import os

class Renamer:

    def __init__(self):
        self.currentPath = os.getcwd()
        print('Current path:' + self.currentPath)

    def update(self):
        print('Renamer update is called!')
