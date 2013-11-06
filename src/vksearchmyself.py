#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013, Durachenko Aleksey V. <durachenko.aleksey@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import urllib2, json, time, codecs, getopt, sys, socket

# start section: temporary file with information about founded purpose information
dbFile = 0
dbMachineFile = 0
def openDbFile(fileName, fileNameMachine):
    global dbFile 
    global dbMachineFile
    dbFile = codecs.open(fileName, 'a', 'utf-8')
    dbMachineFile = codecs.open(fileNameMachine, 'a', 'utf-8')

def writePostRecord(owner_id, post_id, text):
    global dbFile
    global dbMachineFile
    data = "POST %d %d %s" % (owner_id, post_id, text)
    print data
    dbFile.write(data + "\n")
    dbMachineFile.write("POST %d %d\n" % (owner_id, post_id))

def writePostCommentRecord(owner_id, post_id, comment_id, text):
    global dbFile
    global dbMachineFile
    data = "POST_COMMENT %d %d %d %s" % (owner_id, post_id, comment_id, text)
    print data
    dbFile.write(data + "\n")
    dbMachineFile.write("POST_COMMENT %d %d %d\n" % (owner_id, post_id, comment_id))

def writePhotoRecord(owner_id, photo_id, text):
    global dbFile
    global dbMachineFile
    data = "PHOTO %d %d %s" % (owner_id, photo_id, text)
    print data
    dbFile.write(data + "\n")
    dbMachineFile.write("PHOTO %d %d\n" % (owner_id, photo_id))

def writePhotoCommentRecord(owner_id, comment_id, text):
    global dbFile
    global dbMachineFile
    data = "PHOTO_COMMENT %d %d %s" % (owner_id, comment_id, text)
    print data
    dbFile.write(data + "\n")
    dbMachineFile.write("PHOTO_COMMENT %d %d\n" % (owner_id, comment_id))

def writeTopicRecord(group_id, topic_id, text):
    global dbFile
    global dbMachineFile
    data = "TOPIC %d %d %s" % (group_id, topic_id, text)
    print data
    dbFile.write(data + "\n")
    dbMachineFile.write("TOPIC %d %d\n" % (group_id, topic_id))

def writeTopicCommentRecord(group_id, topic_id, comment_id, text):
    global dbFile
    global dbMachineFile
    data = "TOPIC_COMMENT %d %d %d %s" % (group_id, topic_id, comment_id, text)
    print data
    dbFile.write(data + "\n")
    dbMachineFile.write("TOPIC_COMMENT %d %d %d\n" % (group_id, topic_id, comment_id))

def writeVideoRecord(owner_id, topic_id, text):
    global dbFile
    global dbMachineFile
    data = "VIDEO %d %d %s" % (owner_id, topic_id, text)
    print data
    dbFile.write(data + "\n")
    dbMachineFile.write("VIDEO %d %d\n" % (owner_id, topic_id))

def writeVideoCommentRecord(owner_id, video_id, comment_id, text):
    global dbFile
    global dbMachineFile
    data = "VIDEO_COMMENT %d %d %d %s" % (owner_id, video_id, comment_id, text)
    print data
    dbFile.write(data + "\n")
    dbMachineFile.write("VIDEO_COMMENT %d %d %d\n" % (owner_id, video_id, comment_id))

def writeNoteRecord(user_id, note_id, text):
    global dbFile
    global dbMachineFile
    data = "NOTE %d %d %s" % (user_id, note_id, text)
    print data
    dbFile.write(data + "\n")
    dbMachineFile.write("NOTE %d %d\n" % (user_id, note_id))

def writeNoteCommentRecord(user_id, note_id, comment_id, text):
    global dbFile
    global dbMachineFile
    data = "NOTE_COMMENT %d %d %d %s" % (user_id, note_id, comment_id, text)
    print data
    dbFile.write(data + "\n")
    dbMachineFile.write("NOTE_COMMENT %d %d %d\n" % (user_id, note_id, comment_id))

def closeDbFile():
    global dbFile
    global dbMachineFile
    dbFile.close()
    dbMachineFile.close()
# end section

# start section: debug information
def printQuery(query):
    print query
    pass

def printProgress(offset, count):
    print "Progress %d of %d scanned" % (offset, count) 
# end debug section

# start sction: vk wall scanner
def scanWallComments(owner_id, post_id, access_token, purpose_id):
    count = 100
    offset = 0
    
    while True:
        wallQuery = "https://api.vk.com/method/wall.getComments?v=5.2&access_token=%s&owner_id=%d&post_id=%d&count=%d&offset=%d" % (access_token, owner_id, post_id, count, offset)
        printQuery(wallQuery)
        
        try:        
            f = urllib2.urlopen(wallQuery)
            data = json.load(f)
            f.close()
        except:
            time.sleep(2)
            continue

        if "error" in data:
            # user deactivated
            if data["error"]["error_code"] == 15:
                break;
            # user was deleted or banned
            if data["error"]["error_code"] == 18:
                break;
            # too many queryes per second
            if data["error"]["error_code"] == 6:
                time.sleep(0.5)
                continue
            else:
                print "ERROR: ", data
                continue
                exit(-1)               
        # end if
        
        for item in data['response']['items']:
            if item['from_id'] == purpose_id:
                writePostCommentRecord(owner_id, post_id, item['id'], item['text']);
        # end for
        
        if data['response']['count'] <= offset + count:
            break;

        offset += 100
    # end while
# end def

def scanWall(owner_id, access_token, purpose_id):
    count = 100
    offset = 0
    
    while True:
        wallQuery = "https://api.vk.com/method/wall.get?v=5.2&access_token=%s&owner_id=%d&count=%d&offset=%d" % (access_token, owner_id, count, offset)
        printQuery(wallQuery)       
        
        try:        
            f = urllib2.urlopen(wallQuery)
            data = json.load(f)
            f.close()
        except:
            time.sleep(2)
            continue

        if "error" in data:
            # user deactivated
            if data["error"]["error_code"] == 15:
                break;
            # user was deleted or banned
            if data["error"]["error_code"] == 18:
                break;
            # too many queryes per second
            if data["error"]["error_code"] == 6:
                time.sleep(0.5)
                continue
            else:
                print "ERROR: ", data
                continue
                exit(-1)   
        #end if
        
        for item in data['response']['items']:
            if item['from_id'] == purpose_id:
                writePostRecord(owner_id, item['id'], item['text']);
            if item['comments']['count'] > 0:
                scanWallComments(owner_id, item['id'], access_token, purpose_id)
        # end for
        
        printProgress(offset, data['response']['count'])
        if data['response']['count'] <= offset + count:
            break;

        offset += 100
    # end while
# end def
# end section

# start sction: vk photo scanner
def scanPhotoComments(owner_id, access_token, purpose_id):
    count = 100
    offset = 0
    
    while True:
        wallQuery = "https://api.vk.com/method/photos.getAllComments?v=5.2&access_token=%s&owner_id=%d&count=%d&offset=%d" % (access_token, owner_id, count, offset)
        printQuery(wallQuery)       
        
        try:        
            f = urllib2.urlopen(wallQuery)
            data = json.load(f)
            f.close()
        except:
            time.sleep(2)
            continue

        if "error" in data:
            # user deactivated
            if data["error"]["error_code"] == 15:
                break;
            # user was deleted or banned
            if data["error"]["error_code"] == 18:
                break;
            # too many queryes per second
            if data["error"]["error_code"] == 6:
                time.sleep(0.5)
                continue
            else:
                print "ERROR: ", data
                continue
                exit(-1)   
        #end if
        
        for item in data['response']['items']:
            if item['from_id'] == purpose_id:
                writePhotoCommentRecord(owner_id, item['id'], item['text']);
        # end for
        
        printProgress(offset, data['response']['count'])
        if data['response']['count'] <= offset + count:
            break;

        offset += 100
    # end while
# end def

def scanPhoto(owner_id, access_token, purpose_id):
    count = 100
    offset = 0
    
    while True:
        wallQuery = "https://api.vk.com/method/photos.getAll?v=5.2&access_token=%s&owner_id=%d&count=%d&offset=%d" % (access_token, owner_id, count, offset)
        printQuery(wallQuery)       
        
        try:        
            f = urllib2.urlopen(wallQuery)
            data = json.load(f)
            f.close()
        except:
            time.sleep(2)
            continue

        if "error" in data:
            # user deactivated
            if data["error"]["error_code"] == 15:
                break;
            # user was deleted or banned
            if data["error"]["error_code"] == 18:
                break;
            # too many queryes per second
            if data["error"]["error_code"] == 6:
                time.sleep(0.5)
                continue
            else:
                print "ERROR: ", data
                continue
                exit(-1)   
        #end if
        
        for item in data['response']['items']:
            if 'user_id' in item:
                if item['user_id'] == purpose_id:
                    writePhotoRecord(owner_id, item['id'], item['text']);
        # end for
        
        printProgress(offset, data['response']['count'])
        if data['response']['count'] <= offset + count:
            break;

        offset += 100
    # end while
# end def
# end section

# start sction: vk topic scanner
def scanTopicComments(group_id, topic_id, access_token, purpose_id):
    count = 100
    offset = 0
    
    while True:
        wallQuery = "https://api.vk.com/method/board.getComments?v=5.2&access_token=%s&group_id=%d&topic_id=%d&count=%d&offset=%d" % (access_token, group_id, topic_id, count, offset)
        printQuery(wallQuery)
        
        try:        
            f = urllib2.urlopen(wallQuery)
            data = json.load(f)
            f.close()
        except:
            time.sleep(2)
            continue

        if "error" in data:
            # user deactivated
            if data["error"]["error_code"] == 15:
                break;
            # user was deleted or banned
            if data["error"]["error_code"] == 18:
                break;
            # too many queryes per second
            if data["error"]["error_code"] == 6:
                time.sleep(0.5)
                continue
            else:
                print "ERROR: ", data
                continue
                exit(-1)               
        # end if
        
        for item in data['response']['items']:
            if item['from_id'] == purpose_id:
                writeTopicCommentRecord(group_id, topic_id, item['id'], item['text']);
        # end for
        
        if data['response']['count'] <= offset + count:
            break;

        offset += 100
    # end while
# end def

def scanTopic(group_id, access_token, purpose_id):
    count = 100
    offset = 0
    
    while True:
        wallQuery = "https://api.vk.com/method/board.getTopics?v=5.2&access_token=%s&group_id=%d&count=%d&offset=%d" % (access_token, group_id, count, offset)
        printQuery(wallQuery)
        
        try:        
            f = urllib2.urlopen(wallQuery)
            data = json.load(f)
            f.close()
        except:
            time.sleep(2)
            continue

        if "error" in data:
            # user deactivated
            if data["error"]["error_code"] == 15:
                break;
            # user was deleted or banned
            if data["error"]["error_code"] == 18:
                break;
            # too many queryes per second
            if data["error"]["error_code"] == 6:
                time.sleep(0.5)
                continue
            else:
                print "ERROR: ", data
                continue
                exit(-1)   
        #end if
        
        if 'topics' in data['response']:
            for item in data['response']['topics']['items']:
                if item['created_by'] == purpose_id:
                    writeTopicRecord(group_id, item['id'], item['title']);
                if item['comments'] > 0:
                    scanTopicComments(group_id, item['id'], access_token, purpose_id)
            # end for
            printProgress(offset, data['response']['topics']['count'])
            if data['response']['topics']['count'] <= offset + count:
                break;
        else:
            for item in data['response']['items']:
                if item['created_by'] == purpose_id:
                    writeTopicRecord(group_id, item['id'], item['title']);
                if item['comments'] > 0:
                    scanTopicComments(group_id, item['id'], access_token, purpose_id)
            # end for
            printProgress(offset, data['response']['count'])
            if data['response']['count'] <= offset + count:
                break;

        offset += 100
    # end while
# end def
# end section


# start sction: vk video scanner
def scanVideoComments(owner_id, video_id, access_token, purpose_id):
    count = 100
    offset = 0
    
    while True:
        wallQuery = "https://api.vk.com/method/video.getComments?v=5.2&access_token=%s&owner_id=%d&video_id=%d&count=%d&offset=%d" % (access_token, owner_id, video_id, count, offset)
        printQuery(wallQuery)
        
        try:        
            f = urllib2.urlopen(wallQuery)
            data = json.load(f)
            f.close()
        except:
            time.sleep(2)
            continue

        if "error" in data:
            # user deactivated
            if data["error"]["error_code"] == 15:
                break;
            # user was deleted or banned
            if data["error"]["error_code"] == 18:
                break;
            # too many queryes per second
            if data["error"]["error_code"] == 6:
                time.sleep(0.5)
                continue
            else:
                print "ERROR: ", data
                continue
                exit(-1)               
        # end if
        
        for item in data['response']['items']:
            if item['from_id'] == purpose_id:
                writeVideoCommentRecord(owner_id, video_id, item['id'], item['text']);
        # end for
        
        if data['response']['count'] <= offset + count:
            break;

        offset += 100
    # end while
# end def

def scanVideo(owner_id, access_token, purpose_id):
    count = 100
    offset = 0
    
    while True:
        wallQuery = "https://api.vk.com/method/video.get?v=5.2&access_token=%s&owner_id=%d&count=%d&offset=%d" % (access_token, owner_id, count, offset)
        printQuery(wallQuery)
        
        try:        
            f = urllib2.urlopen(wallQuery)
            data = json.load(f)
            f.close()
        except:
            time.sleep(2)
            continue

        if "error" in data:
            # user deactivated
            if data["error"]["error_code"] == 15:
                break;
            # user was deleted or banned
            if data["error"]["error_code"] == 18:
                break;
            # too many queryes per second
            if data["error"]["error_code"] == 6:
                time.sleep(0.5)
                continue
            else:
                print "ERROR: ", data
                continue
                exit(-1)   
        #end if
        
        for item in data['response']['items']:
            if item['owner_id'] == purpose_id:
                writeVideoRecord(owner_id, item['id'], item['title']);
            if item['comments'] > 0:
                scanVideoComments(owner_id, item['id'], access_token, purpose_id)
        # end for
        
        printProgress(offset, data['response']['count'])
        if data['response']['count'] <= offset + count:
            break;

        offset += 100
    # end while
# end def
# end section


# start sction: vk note scanner
def scanNoteComments(owner_id, note_id, access_token, purpose_id):
    count = 100
    offset = 0
    
    while True:
        wallQuery = "https://api.vk.com/method/notes.getComments?v=5.2&access_token=%s&owner_id=%d&note_id=%d&count=%d&offset=%d" % (access_token, owner_id, note_id, count, offset)
        printQuery(wallQuery)
        
        try:        
            f = urllib2.urlopen(wallQuery)
            data = json.load(f)
            f.close()
        except:
            time.sleep(2)
            continue

        if "error" in data:
            # user deactivated
            if data["error"]["error_code"] == 15:
                break;
            # user was deleted or banned
            if data["error"]["error_code"] == 18:
                break;
            # too many queryes per second
            if data["error"]["error_code"] == 6:
                time.sleep(0.5)
                continue
            else:
                print "ERROR: ", data
                continue
                exit(-1)               
        # end if
        
        for item in data['response']['items']:
            if int(item['uid']) == purpose_id:
                writeNoteCommentRecord(owner_id, note_id, int(item['id']), item['message']);
        # end for
        
        if data['response']['count'] <= offset + count:
            break;

        offset += 100
    # end while
# end def

def scanNote(user_id, access_token, purpose_id):
    count = 100
    offset = 0
    
    while True:
        wallQuery = "https://api.vk.com/method/notes.get?v=5.2&access_token=%s&user_id=%d&count=%d&offset=%d" % (access_token, user_id, count, offset)
        printQuery(wallQuery)
        
        try:        
            f = urllib2.urlopen(wallQuery)
            data = json.load(f)
            f.close()
        except:
            time.sleep(2)
            continue

        if "error" in data:
            # user deactivated
            if data["error"]["error_code"] == 15:
                break;
            # user was deleted or banned
            if data["error"]["error_code"] == 18:
                break;
            # note not found
            if data["error"]["error_code"] == 180:
                break
            # too many queryes per second
            if data["error"]["error_code"] == 6:
                time.sleep(0.5)
                continue
            else:
                print "ERROR: ", data
                continue
                exit(-1)   
        #end if
        
        for item in data['response']['items']:
            if item['owner_id'] == purpose_id:
                writeNoteRecord(user_id, item['id'], item['title']);
            if item['comments'] > 0:
                scanNoteComments(user_id, item['id'], access_token, purpose_id)
        # end for
        
        printProgress(offset, data['response']['count'])
        if data['response']['count'] <= offset + count:
            break;

        offset += 100
    # end while
# end def
# end section


# my friends
def getFriendIds(user_id, access_token):
    wallQuery = "https://api.vk.com/method/friends.get?v=5.2&access_token=%s&user_id=%d" % (access_token, user_id)
    printQuery(wallQuery)       

    while True:        
        try:        
            f = urllib2.urlopen(wallQuery)
            data = json.load(f)
            f.close()
        except:
            time.sleep(2)
            continue
    
        if "error" in data:
            # user deactivated
            if data["error"]["error_code"] == 15:
                break;
            # user was deleted or banned
            if data["error"]["error_code"] == 18:
                break;
            # too many queryes per second
            if data["error"]["error_code"] == 6:
                time.sleep(0.5)
                continue
            else:
                print "ERROR: ", data
                continue
                exit(-1)   
        #end if
        
        return data['response']['items']
    # end while
    return []
# end def

# my followers
def getFollowersIds(user_id, access_token):
    wallQuery = "https://api.vk.com/method/users.getFollowers?v=5.2&access_token=%s&user_id=%d" % (access_token, user_id)
    printQuery(wallQuery)       

    while True:        
        try:        
            f = urllib2.urlopen(wallQuery)
            data = json.load(f)
            f.close()
        except:
            time.sleep(2)
            continue
    
        if "error" in data:
            # user deactivated
            if data["error"]["error_code"] == 15:
                break;
            # user was deleted or banned
            if data["error"]["error_code"] == 18:
                break;
            # too many queryes per second
            if data["error"]["error_code"] == 6:
                time.sleep(0.5)
                continue
            else:
                print "ERROR: ", data
                continue
                exit(-1)   
        #end if
        
        return data['response']['items']
    # end while
    return []
# end def

# my groups
def getGroupsIds(user_id, access_token):
    count = 1000
    offset = 0
    ids = []
    
    while True:
        wallQuery = "https://api.vk.com/method/groups.get?v=5.2&access_token=%s&user_id=%d&count=%d&offset=%d" % (access_token, user_id, count, offset)
        printQuery(wallQuery)       
        
        try:        
            f = urllib2.urlopen(wallQuery)
            data = json.load(f)
            f.close()
        except:
            time.sleep(2)
            continue

        if "error" in data:
            # Access to the group list is denied due to the user's privacy settings
            if data["error"]["error_code"] == 260:
                break;
            # user deactivated
            if data["error"]["error_code"] == 15:
                break;
            # user was deleted or banned
            if data["error"]["error_code"] == 18:
                break;
            # too many queryes per second
            if data["error"]["error_code"] == 6:
                time.sleep(0.5)
                continue
            else:
                print "ERROR: ", data
                continue
                exit(-1)   
        #end if
        
        ids += data['response']['items']
        
        #printProgress(offset, data['response']['count'])
        if data['response']['count'] <= offset + count:
            break;

        offset += 1000
    # end while
    return ids
# end def

# my subscription: users, groups
def getSubscriptionIds(user_id, access_token):
    count = 200
    offset = 0
    #ids = []
    
    while True:
        wallQuery = "https://api.vk.com/method/users.getSubscriptions?v=5.2&access_token=%s&user_id=%d&count=%d&offset=%d" % (access_token, user_id, count, offset)
        printQuery(wallQuery)       
        
        try:        
            f = urllib2.urlopen(wallQuery)
            data = json.load(f)
            f.close()
        except:
            time.sleep(2)
            continue

        if "error" in data:
            # user deactivated
            if data["error"]["error_code"] == 15:
                break;
            # user was deleted or banned
            if data["error"]["error_code"] == 18:
                break;
            # too many queryes per second
            if data["error"]["error_code"] == 6:
                time.sleep(0.5)
                continue
            else:
                print "ERROR: ", data
                continue
                exit(-1)   
        #end if
        return data['response']['users']['items'], data['response']['groups']['items']
        
        #printProgress(offset, data['response']['count'])
        #if data['response']['count'] <= offset + count:
        #    break;
        # 
        #offset += 1000
    # end while
    #return ids
    return [], []
# end def

def showUsage():
    print "== vksearchmyself.py - v.0.1.0  =="
    print "Usage: "
    print "    vksearchmyself.py --access_token <> --purpose_id <> --users_state <> --groups_state <> --found_file <> --found_file_desc <> [--deep <>][--groups_of_friends]"

access_token = None
purpose_id = None
users_state = None
groups_state = None
found_file = None
found_file_desc = None
deep = 0
groups_of_friends = False

options, remainder = getopt.getopt(sys.argv[1:], 'o:v', ['access_token=', 'purpose_id=', 'users_state=', 'groups_state=', 'found_file=', 'found_file_desc=', 'deep=', 'groups_of_friends'])
for opt, arg in options:
    if opt == '--access_token':
        access_token = arg
    elif opt == '--purpose_id':
        purpose_id = int(arg)
    elif opt == '--users_state':
        users_state = arg
    elif opt == '--groups_state':
        groups_state = arg
    elif opt == '--found_file':
        found_file = arg
    elif opt == '--found_file_desc':
        found_file_desc = arg
    elif opt == "--deep":
        deep = int(arg)
    elif opt == "--groups_of_friends":
        groups_of_friends = True

if access_token == None or purpose_id == None or users_state == None or groups_state == None or found_file == None or found_file_desc == None:
    showUsage()
    exit(-1)

print "Access token           :", access_token
print "Purpose ID             :", purpose_id
print "Users state file       :", users_state
print "Groups state file      :", groups_state
print "Founded records        :", found_file
print "Desc of founded records:", found_file_desc
print "Deep                   :", deep
print "Groups of friends      :", groups_of_friends
# deduplicate
processedUsers = []
processedGroups = []

try:
    file = open(users_state, "r")    
    for item in file.read().split(';'):
        processedUsers.append(int(item))
    print file.read()
    
    file.close()
except:
    print "users not found"

try:
    file = open(groups_state, "r")
    for item in file.read().split(';'):
        processedGroups.append(int(item))
    file.close()
except:
    print "groups not found"

fUsers = open(users_state, "a")
fGroups = open(groups_state, "a")

# configure
openDbFile(found_file_desc, found_file)
# setup timeout
socket.setdefaulttimeout(3)

# result: userList, groupList
def weNeedToBeDeeper(user_id, access_token, deep, processedUserList):
    # info
    print "Deep = %d, user_id = %d | Processing number = %d" % (deep, user_id, len(processedUserList))    
    # process the user    
    userFriendList = getFriendIds(user_id, access_token)
    userFollowList = getFollowersIds(user_id, access_token)
    userGroupList = getGroupsIds(user_id, access_token)
    userSubscribeUserList, mySubscribeGroupList = getSubscriptionIds(user_id, access_token)
    localUserList = userFriendList + userFollowList + userSubscribeUserList
    localGroupList = userGroupList + mySubscribeGroupList
    # mark current user as processed
    processedUserList += [user_id]
    # go to deeper    
    if deep > 0:
        for id in localUserList:
            if id not in processedUserList:
                u, g, processedUserList = weNeedToBeDeeper(id, access_token, deep-1, processedUserList)
                localUserList = list(set(localUserList + u))
                localGroupList = list(set(localGroupList + g))
                print "Users count :", len(localUserList)
                print "Groups count:", len(localGroupList)
        # end for
    # end if                
    return localUserList, localGroupList, processedUserList

# result: userList, groupList
def groupsOfFriends(user_id, access_token):
    # process the user    
    userFriendList = getFriendIds(user_id, access_token)
    userFollowList = getFollowersIds(user_id, access_token)
    userSubscribeUserList, mySubscribeGroupList = getSubscriptionIds(user_id, access_token)
    localUserList = userFriendList + userFollowList + userSubscribeUserList
    # scan groups
    groups = []
    for id in localUserList:
        groups += getGroupsIds(id, access_token)
    return groups
    
userList, groupList, processedUserList = weNeedToBeDeeper(purpose_id, access_token, deep, [])
userList = list(set(userList + [purpose_id]))
if deep == 0 and groups_of_friends:
    groupList = list(set(groupList + groupsOfFriends(purpose_id, access_token)))
print "Total users count :", len(userList)
print "Total groups count:", len(groupList)

# scan
for id in userList:
    if id in processedUsers:
        print "User %d already processed" % (id)
        continue
    scanWall(id, access_token, purpose_id)
    scanPhoto(id, access_token, purpose_id)
    scanPhotoComments(id, access_token, purpose_id)
    scanVideo(id, access_token, purpose_id)
    scanNote(id, access_token, purpose_id)
    fUsers.write("%d;" % (id))
    processedUsers.append(id)
for id in groupList:
    if id in processedGroups:
        print "Group %d already processed" % (id)
        continue
    scanWall(-id, access_token, purpose_id)
    scanPhoto(-id, access_token, purpose_id)
    scanPhotoComments(-id, access_token, purpose_id)
    scanVideo(-id, access_token, purpose_id)
    scanTopic(id, access_token, purpose_id)
    fGroups.write("%d;" % (id))
    processedGroups.append(id)

fUsers.close()
fGroups.close()
    
# deconfigure
closeDbFile()
