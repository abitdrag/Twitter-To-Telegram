import twitterManager
import dbManager 
import time 

# update usernames every hour 
while True: 
	print('Entering loop')
	# get userids from db 
	users = dbManager.list_all_users()
	userids = []
	for user in users:
		userids.append(user[0])
	print('Userids:' , userids)
	# get usernames from twitter and update db 
	for id in userids:
		try:
			username = twitterManager.lookup_usernames(id)
			print(username)
			username = username[0]
		except:
			username = None
		print(username)
		if username != None:
			dbManager.update_username(id, username)
		else:
			for user in users:
				if(user[0] == id):
					old_username = user[1]
					break
			print('[Deleting] Username - '+ old_username +' not found (user id - ' + str(id) + ')')
			if(old_username != None):
				dbManager.delete_user_from_userdata(old_username)			
	time.sleep(10)
				