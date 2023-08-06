# -*- coding: utf-8 -*-
"""
@author: djclavero@yahoo.com

Script for testing 'video' package
"""

# Projects: contain setup.py and packages 
# Packages: contain __init__.py and modules (.py files)

from video.players import mp4play 

# Call function
mp4play.test_video()

# Call variable
print('EXTENSION is ' + mp4play.EXTENSION)

# Create object
videofile = mp4play.VideoFile('Pulp Fiction')
videofile.videofile_info()



