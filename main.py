try:
  import config
except Exception:
  print("Can't load config.py")
  sys.exit(1)
try:
  import auth
except Exception:
  print("Warning: can't load auth.py")

locations = ['Krakow', 'Kraków', 'Cracow']
usernames = getUsernames(locations)
users = getTop(usernames, 10)['users']
users = sorted(users, key=lambda k: k['stars'])
for user in users:
	print(user['login'] + '			' + str(user['stars'])) 
