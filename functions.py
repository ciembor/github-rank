# -*- coding: utf-8 -*-

from github import Github, NamedUser, GithubException
from jinja2 import Environment, FileSystemLoader
import sys
import os
import time
import pickle

def getUsernames(locations, gh):
  usernames = set()

  for location in locations:
    print location
    
    while True:
      try:
        result = gh.legacy_search_users(location)
        for user in result:
          try:
            if unicode(location, 'utf-8').lower() in user.location.lower():
              usernames.add(user.login)
          except Exception: 
            pass
        break
      except GithubException as e:
        print('Warning: ' + str(e.data['message']))
        if 403 == e.status:
          print('I will try again after 10 minutes...')
          time.sleep(600)
        else:
          print('I will try again after 5 seconds...')
          time.sleep(5)
      except Exception as e:
        print(e)
        time.sleep(5)
        print('I will try again after 5 seconds...')

  return usernames
  
def getTop(usernames, n, gh):

  top = {'users': [], 'repositories': []}
  for username in usernames:

    while True: 
      try:
        stars_counter = 0
        result_user = gh.get_user(username)
        result_repos = result_user.get_repos()  

        ### get top repositories ###
        for repository in result_repos:
          # count stars for users rank
          stars_counter += repository.watchers
          min_top = None 
          to_append = None
          higher_count = 0

          if len(top['repositories']) < n:
            top['repositories'].append(repository)
          else:
            for top_repository in top['repositories']:
              if top_repository.watchers <= repository.watchers:
                to_append = repository

          if to_append:
            top['repositories'].append(to_append)

            for top_repository in top['repositories']:
              if min_top is None or min_top > top_repository.watchers:
                min_top = top_repository.watchers
                
            # remove too low repositories
            if min_top < repository.watchers:
              higher_count = 0
              for repository in top['repositories']:
                if repository.watchers > min_top:
                  higher_count += 1
              if len(top['repositories']) > higher_count >= n:
                for repository in top['repositories']:
                  if repository.watchers == min_top:
                    top['repositories'].remove(repository)
          
        ### get top users ###
        if ('User' == result_user.type):
          min_top_users = None
          to_append = None
          higher_count = 0

          result_user.stars = stars_counter

          if len(top['users']) < n:
            top['users'].append(result_user)
          else:
            for top_user in top['users']:
              if top_user.stars <= result_user.stars:
                to_append = result_user
          
          if to_append:
            top['users'].append(result_user)

            for user in top['users']:
              if min_top_users is None or min_top_users > user.stars:
                min_top_users = user.stars

            if min_top_users < result_user.stars:
              higher_count = 0
              for user in top['users']:
                if user.stars > min_top_users:
                  higher_count += 1
              if len(top['users']) > higher_count >= n:
                for user in top['users']:
                  if user.stars == min_top_users:
                    top['users'].remove(user)
                  
        break
        
      except GithubException as e:
        print('Warning: ' + str(e.data['message']))
        if 403 == e.status:
          print('I will try again after 10 minutes...')
          time.sleep(600)
        else:
          print(username)
          time.sleep(5)
          print('I will try again after 5 seconds...')
      except Exception as e:
        print(e)
        time.sleep(5)
        print('I will try again after 5 seconds...')
          
  ### sort and format###
  
  top['users'] = sorted(top['users'], key=lambda k: k.stars, reverse=True)
  for i in range(0, len(top['users'])):
    top['users'][i].position = i + 1
    top['users'][i].link = None
    try:
      if not top['users'][i].blog.startswith('http') and len(top['users'][i].blog) > 0:
        top['users'][i].link = 'http://' + top['users'][i].blog
      else:
        top['users'][i].link = top['users'][i].blog
    except:
      pass
    
  top['repositories'] = sorted(top['repositories'], key=lambda k: k.watchers, reverse=True)
  for i in range(0, len(top['repositories'])):
    top['repositories'][i].position = i + 1
    top['repositories'][i].link = None
    try:
      if not top['repositories'][i].homepage.startswith('http') and len(top['repositories'][i].homepage) > 0:
        top['repositories'][i].link = 'http://' + top['repositories'][i].homepage
      else:
        top['repositories'][i].link = top['repositories'][i].homepage
    except:
      pass
      
  ### something is wrong with algorithm, ugly fix;)
  for top_list in top.keys():
    if len(top[top_list]) > n:
      if top[top_list][-1] != top[top_list][-2]:
        top[top_list].pop(-1)
    
  return top

def updateTop(top, location_id, location_names, db_path, output_path):
  old_top = {}
  
  if not os.path.exists(db_path):
    os.makedirs(db_path)
  if not os.path.exists(output_path):
    os.makedirs(output_path)
  
  # read old top dictionary
  try: 
    db = open(db_path + "/" + location_id + ".dat", "r")
    old_top = pickle.load(db)
    db.close()
  except Exception:
    old_top = top
  
  # save new top dictionary
  try:
    db = open(db_path + "/" + location_id + ".dat", "w")
    pickle.dump(top, db, protocol=0)
    db.close()
  except:
    raise

  # save to .md
  env = Environment(loader=FileSystemLoader('./templates'))
  template = env.get_template('page.md')
  output = template.render(top=top, location_id=location_id, location_name=unicode(location_names[0], 'utf8'))
  
  # save new top dictionary
  try:
    md = open(output_path + "/" + location_id + ".md", "w")
    md.write(output.encode('utf8'))
    md.close()
  except:
    raise
