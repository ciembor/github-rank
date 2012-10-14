import requests
import json

def getUsernames(locations):
	usernames = set()
	for location in locations:
		r = requests.get('https://api.github.com/legacy/user/search/' + location)
		if(r.ok):
			result = json.loads(r.text or r.content)['users']
			for user in result:
				usernames.add(user['username'])
	return usernames

def getTop(usernames, n):
	top = {'users': [], 'repositories': [{'watchers': 0}]}

	for username in usernames:
		stars_counter = 0

		### get top repositories ###
		r = requests.get('https://api.github.com/users/' + username + '/repos')
		if(r.ok):
			print(username)
			result = json.loads(r.text or r.content)
			for repository in result:
				# count stars for users rank
				stars_counter += int(repository['watchers'])
				min_top = None 
				to_append = None

				for top_repository in top['repositories']:
					if min_top is None or min_top > top_repository['watchers']:
						min_top = top_repository['watchers']
					if repository['watchers'] >= top_repository['watchers']:
						to_append = repository

				if to_append:
					top['repositories'].append(to_append)
						
				# remove too low repositories
				if min_top < repository['watchers']:
					higher_count = 0
					for repository in top['repositories']:
						if repository['watchers'] > min_top:
							higher_count += 1
					if len(top['repositories']) > higher_count >= n:
						for repository in top['repositories']:
							if repository['watchers'] == min_top:
								top['repositories'].remove(repository)
		
		### get top users ###
		r = requests.get('https://api.github.com/users/' + username)
		if (r.ok):
			result = json.loads(r.text or r.content)
			if ('User' == result['type']):
				min_top_users = None
				to_append = None
				higher_count = 0
	
				result['stars'] = stars_counter
	
				if len(top['users']) < n:
					top['users'].append(result)
				else:
					for top_user in top['users']:
						if top_user['stars'] <= result['stars']:
							to_append = result['stars']
				
				if to_append:
					top['users'].append(result)
	
				for user in top['users']:
					if min_top_users is None or min_top_users > user['stars']:
						min_top_users = user['stars']
	
				if min_top_users < result['stars']:
					higher_count = 0
					for user in top['users']:
						if user['stars'] > min_top_users:
							higher_count += 1
					if len(top['users']) > higher_count >= n:
						for user in top['users']:
							if user['stars'] == min_top_users:
								top['users'].remove(user)	
	return top
