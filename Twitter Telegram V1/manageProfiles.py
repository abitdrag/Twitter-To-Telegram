import sys
import dbManager
import twitterManager

# take arguments from command line
# add username
# list
# delete username
# update username lastid

arguments = sys.argv
arguments.append('123') # append at end to handle 0 element list on truncation 
arguments = arguments[1:] # truncate filename - argv[0]

# refetch usernames in database from twitter
print ('Fetching usernames from twitter ...')
users = dbManager.list_all_users()
userids = []
for user in users:
    userids.append(user[0])

if len(userids) != 0:
    usernames = twitterManager.lookup_usernames(userids)
print ('Updating database ...')
for i in range(0, len(userids)):
    dbManager.update_username(userids[i], usernames[i])
print ('Refetch complete !')

if arguments[0].lower() == 'add':
    userid = twitterManager.lookup_id(arguments[1])
    last_post_id = twitterManager.get_last_post_id(userid)
    dbManager.insert_to_userdata(userid, arguments[1], last_post_id)

elif arguments[0].lower() == 'list':
    users = dbManager.list_all_users()
    for user in users:
        print(user[0] + '\t' + user[1] + '\t' + user[2])

elif arguments[0].lower() == 'delete':
    dbManager.delete_user_from_userdata(arguments[1])

elif arguments[0].lower() == 'update':
    dbManager.update_user_in_userdata(arguments[1], arguments[2])

else:
    print ()
    print ('ADD - add new profile')
    print ('LIST - list all profiles')
    print ('DELETE - stop monitoring profile')
    print ('UPDATE - update profilename lastid')
