# -*- coding: utf-8 -*-

from functions import *
from github import Github
import os
import shutil

import config
import auth

gh = Github(auth.oauth)

try:
  if not os.path.exists('./cache'):
    os.makedirs('./cache')
except:
  raise
  
for location in config.locations:
  if not os.path.exists('./cache/' + location + '.md'):
    usernames = getUsernames(config.locations[location], gh)
    top = getTop(usernames, config.result_size, gh)
    updateTop(top, location, config.locations[location], config.db_path, './cache')

shutil.copy('./cache', config.output_path)
shutil.rmdir('./cache')
