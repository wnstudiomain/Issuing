class Blah:

    def __init__(self, name):
        self.name = name

    def __call__(self):
        return self.name

    @staticmethod
    def run(self):
        print(self)


obj = Blah('fsdf')
obj()
print(obj())

import os

# Get the current working
# directory (CWD)
cwd = os.getcwd()

# Print the current working
# directory (CWD)
print("Current working directory:")
print(cwd)