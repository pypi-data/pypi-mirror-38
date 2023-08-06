# -*- coding: utf-8 -*-
"""
@author: djclavero@yahoo.com

Python Module
"""

# Projects: contain setup.py and packages 
# Packages: contain __init__.py and modules (.py files)

# Define a function
def test_video():
    print('Calling to test_video function')
    

# Define a variable
EXTENSION = 'mp4'


# Define a class
class VideoFile:
    def __init__(self, name):
        self.name = name

    def videofile_info(self):
        print("Video file name is " + self.name)
        
        


