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

class ActivitiesSearcher:
    # -------------------------------------------------------------------------
    # section: settings
    # -------------------------------------------------------------------------
    #
    __targetId = None
    __accessToken = None
    __apiVersion = 5.2
    #
    def setAccessToken(self, accessToken):
        self.__accessToken = accessToken
    # 
    def setApiVersion(self, apiVersion):
        self.__apiVersion = apiVersion
    #
    def setTargetId(self, id):
        self.__targetId = id
    # -------------------------------------------------------------------------
    # section: open/close files
    # -------------------------------------------------------------------------
    #
    __activitiesFile = None
    __activitiesDetailFile = None
    #
    def openActivitiesFile(self,  fileName, rewrite = False):
        if rewrite == False:
            self.__activitiesFile = open(fileName,  'a')
        else:
            self.__activitiesFile = open(fileName,  'w')
    #
    def openActivitiesDetailFile(self, fileName, rewrite = False):
        if rewrite == False:
            self.__activitiesDetailFile = codecs.open(fileName, 'a', 'utf-8')
        else:
            self.__activitiesDetailFile = codecs.open(fileName, 'w', 'utf-8')
    #
    def closeActivitiesFile(self):
        self.__activitiesFile.close()        
    #
    def closeActivitiesDetailFile(self):
        self.__activitiesDetailFile.close()        
    #
    # -------------------------------------------------------------------------
    # section: write activities details to the file
    # -------------------------------------------------------------------------
    #
    def writePostDetail(self, owner_id, post_id, text):
        data  = "========================================"
        data += "\n" + "TYPE       : POST"
        data += "\n" + "OWNER_ID   : %d" % (owner_id)
        data += "\n" + "POST_ID    : %d" % (post_id)
        data += "\n" + "TEXT       : %s" % (text)
        data += "\n"
        self.__activitiesDetailFile.write(data)
    #
    def writePostCommentDetail(self, owner_id, post_id, comment_id, text):
        data  = "========================================"
        data += "\n" + "TYPE       : POST_COMMENT"
        data += "\n" + "OWNER_ID   : %d" % (owner_id)
        data += "\n" + "POST_ID    : %d" % (post_id)
        data += "\n" + "COMMENT_ID : %d" % (comment_id)
        data += "\n" + "TEXT       : %s" % (text)
        data += "\n"
        self.__activitiesDetailFile.write(data)
    #
    def writePhotoDetail(self, owner_id, photo_id, text):
        data  = "========================================"
        data += "\n" + "TYPE       : PHOTO"
        data += "\n" + "OWNER_ID   : %d" % (owner_id)
        data += "\n" + "PHOTO_ID   : %d" % (photo_id)
        data += "\n" + "TEXT       : %s" % (text)
        data += "\n"
        self.__activitiesDetailFile.write(data)    
    #
    def writePhotoCommentDetail(self, owner_id, comment_id, text):
        data  = "========================================"
        data += "\n" + "TYPE       : PHOTO_COMMENT"
        data += "\n" + "OWNER_ID   : %d" % (owner_id)
        data += "\n" + "COMMENT_ID : %d" % (comment_id)
        data += "\n" + "TEXT       : %s" % (text)
        data += "\n"
        self.__activitiesDetailFile.write(data)    
    #
    def writeTopicDetail(self, group_id, topic_id, text):
        data  = "========================================"
        data += "\n" + "TYPE       : TOPIC"
        data += "\n" + "GROUP_ID   : %d" % (group_id)
        data += "\n" + "TOPIC_ID   : %d" % (topic_id)
        data += "\n" + "TEXT       : %s" % (text)
        data += "\n"
        self.__activitiesDetailFile.write(data)    
    #
    def writeTopicCommentDetail(self, group_id, topic_id, comment_id, text):
        data  = "========================================"
        data += "\n" + "TYPE       : TOPIC_COMMENT"
        data += "\n" + "GROUP_ID   : %d" % (group_id)
        data += "\n" + "TOPIC_ID   : %d" % (topic_id)
        data += "\n" + "COMMENT_ID : %d" % (comment_id)
        data += "\n" + "TEXT       : %s" % (text)
        data += "\n"
        self.__activitiesDetailFile.write(data)    
    #
    def writeVideoDetail(self, owner_id, video_id, text):
        data  = "========================================"
        data += "\n" + "TYPE       : VIDEO"
        data += "\n" + "OWNER_ID   : %d" % (owner_id)
        data += "\n" + "VIDEO_ID   : %d" % (video_id)
        data += "\n" + "TEXT       : %s" % (text)
        data += "\n"
        self.__activitiesDetailFile.write(data)    
    #
    def writeVideoCommentDetail(self, owner_id, video_id, text):
        data  = "========================================"
        data += "\n" + "TYPE       : VIDEO_COMMENT"
        data += "\n" + "OWNER_ID   : %d" % (owner_id)
        data += "\n" + "VIDEO_ID   : %d" % (video_id)
        data += "\n" + "COMMENT_ID : %d" % (video_id)
        data += "\n" + "TEXT       : %s" % (text)
        data += "\n"
        self.__activitiesDetailFile.write(data)   
    #
    def writeNoteDetail(self, user_id, note_id, text):
        data  = "========================================"
        data += "\n" + "TYPE       : NOTE"
        data += "\n" + "USER_ID    : %d" % (user_id)
        data += "\n" + "NOTE_ID    : %d" % (note_id)
        data += "\n" + "TEXT       : %s" % (text)
        data += "\n"
        self.__activitiesDetailFile.write(data)    
    #
    def writeNoteCommentDetail(self, user_id, note_id, comment_id, text):
        data  = "========================================"
        data += "\n" + "TYPE       : NOTE_COMMENT"
        data += "\n" + "USER_ID    : %d" % (user_id)
        data += "\n" + "NOTE_ID    : %d" % (note_id)
        data += "\n" + "COMMENT_ID : %d" % (comment_id)
        data += "\n" + "TEXT       : %s" % (text)
        data += "\n"
        self.__activitiesDetailFile.write(data)    
    # 
    # -------------------------------------------------------------------------
    # section: write activities to the file
    # -------------------------------------------------------------------------
    #
    def writePost(self, owner_id, post_id):
        self.__activitiesFile.write("POST %d %d\n" % (owner_id, post_id));
    #
    def writePostComment(self, owner_id, post_id, comment_id):
        self.__activitiesFile.write("POST_COMMENT %d %d %d\n" % (owner_id, post_id, comment_id));
    #
    def writePhoto(self, owner_id, photo_id):
        self.__activitiesFile.write("PHOTO %d %d\n" % (owner_id, photo_id))
    #
    def writePhotoComment(self, owner_id, comment_id):
        self.__activitiesFile.write("PHOTO_COMMENT %d %d\n" % (owner_id, comment_id))
    #
    def writeTopic(self, group_id, topic_id):
        self.__activitiesFile.write("TOPIC %d %d\n" % (group_id, topic_id))
    #
    def writeTopicComment(self, group_id, topic_id, comment_id):
        self.__activitiesFile.write("TOPIC_COMMENT %d %d %d\n" % (group_id, topic_id, comment_id))
    #
    def writeVideo(self, owner_id, video_id):
        self.__activitiesFile.write("VIDEO %d %d\n" % (owner_id, video_id))
    #
    def writeVideoComment(self, owner_id, video_id, comment_id):
        self.__activitiesFile.write("VIDEO_COMMENT %d %d %d\n" % (owner_id, video_id, comment_id))
    #
    def writeNote(self, user_id, note_id):
        self.__activitiesFile.write("NOTE %d %d\n" % (user_id, note_id))
    #
    def writeNoteComment(self, user_id, note_id, comment_id):
        self.__activitiesFile.write("NOTE_COMMENT %d %d %d\n" % (user_id, note_id, comment_id))
    #
    # -------------------------------------------------------------------------
    # section: api call's
    # -------------------------------------------------------------------------
    #    
    # return: response or None on error
    def callApi(self, url):
        url = "https://api.vk.com/method/" + url;
        url += "&v=%s" % (self.__apiVersion)
        if self.__accessToken != None:
            url += "&access_token=%s" % (self.__accessToken)
        
        while True:
            print url
            try:        
                reply = urllib2.urlopen(url)
                data = json.load(reply)
                reply.close()
            except:
                time.sleep(2)
                continue
    
            if "error" in data:
                # too many queryes per second. wait and retry
                if data["error"]["error_code"] == 6:
                    time.sleep(1)
                    continue
                # something else
                return None
            # end if
            return data["response"]
        # end while    
    #        
    # return: response or None on error
    def singleQuery(self, query):        
        return self.callApi(query)
    #
    # return: [response] or None on error
    def multiQuery(self, query, itemperpage):
        pages = []
        offset = 0
        while True:
            localQuery = query + "&offset=%d&count=%d" % (offset, itemperpage)
            
            response = self.callApi(localQuery)
            if response == None:
                return None
                
            pages.append(response)
            
            # one exception exists for searchTopic()
            if 'topics' in response:
                if response['topics']['count'] <= offset + itemperpage:
                    break;   
            # another exception exists for fetchSubscriptionIds()
            if 'users' in response and 'groups' in response:
                if response['users']['count'] <= offset + itemperpage and response['groups']['count'] <= offset + itemperpage :
                    break;
            else:
                if response['count'] <= offset + itemperpage:
                    break;
                
            offset += itemperpage
        # end while
        return pages
    #
    def searchPostComment(self, owner_id, post_id):
        result = self.multiQuery("wall.getComments?owner_id=%d&post_id=%d" % (owner_id, post_id), 100)        
        if result != None:
            for response in result:
                for item in response['items']:
                    if item['from_id'] == self.__targetId:
                        self.writePostComment(owner_id, post_id, item['id'])
                        self.writePostCommentDetail(owner_id, post_id, item['id'], item['text'])
                # end for
            # end for
    #
    def searchPost(self, owner_id):
        result = self.multiQuery("wall.get?owner_id=%d" % (owner_id), 100)
        if result != None:
            for response in result:
                for item in response['items']:
                    if item['from_id'] == self.__targetId:
                        self.writePost(owner_id, item['id'])
                        self.writePostDetail(owner_id, item['id'], item['text'])
                    if item['comments']['count'] > 0:
                        self.searchPostComment(owner_id, item['id'])
                # end for
            # end for        
    #
    def searchPhotoComment(self, owner_id):
        result = self.multiQuery("photos.getAllComments?owner_id=%d" % (owner_id), 100)
        if result != None:
            for response in result:
                for item in response['items']:
                    if item['from_id'] == self.__targetId:
                        self.writePhotoComment(owner_id, item['id'])
                        self.writePhotoCommentDetail(owner_id, item['id'], item['text'])
                # end for
            # end for
    #
    def searchPhoto(self, owner_id):
        result = self.multiQuery("photos.getAll?owner_id=%d" % (owner_id), 100)
        if result != None:
            for response in result:
                for item in response['items']:
                    if 'user_id' in item:
                        if item['user_id'] == self.__targetId:
                            self.writePhoto(owner_id, item['id'])
                            self.writePhotoDetail(owner_id, item['id'], item['text'])
                # end for
            # end for
    #
    def searchTopicComment(self, group_id, topic_id):
        result = self.multiQuery("board.getComments?group_id=%d&topic_id=%d" % (group_id, topic_id), 100)
        if result != None:
            for response in result:
                for item in response['items']:
                    if item['from_id'] == self.__targetId:
                        self.writeTopicComment(group_id, topic_id, item['id'])
                        self.writeTopicCommentDetail(group_id, topic_id, item['id'], item['text'])
                # end for
            # end for        
    #
    def searchTopic(self, group_id):
        result = self.multiQuery("board.getTopics?group_id=%d" % (group_id), 100)
        if result != None:
            for response in result:     
                tmp = response
                if 'topics' in response:
                    tmp = response['topics']
                    
                for item in tmp['items']:
                    if item['created_by'] == self.__targetId:
                        self.writeTopic(group_id, item['id'])
                        self.writeTopicDetail(group_id, item['id'], item['title'])
                        if item['comments']['count'] > 0:
                            self.searchTopicComment(group_id, item['id'])                
                # end for
            # end for   
    #
    def searchVideoComment(self, owner_id, video_id):
        result = self.multiQuery("video.getComments?owner_id=%d&video_id=%d" % (owner_id, video_id), 100)
        if result != None:
            for response in result:
                for item in response['items']:
                    if item['from_id'] == self.__targetId:
                        self.writeVideoComment(owner_id, video_id, item['id'])
                        self.writeVideoCommentDetail(owner_id, video_id, item['id'], item['text'])
                # end for
            # end for     
    #
    def searchVideo(self, owner_id):
        result = self.multiQuery("video.get?owner_id=%d" % (owner_id), 100)
        if result != None:
            for response in result:
                for item in response['items']:
                    if item['owner_id'] == self.__targetId:
                        self.writeVideo(owner_id, item['id'])
                        self.writeVideoDetail(owner_id, item['id'], item['title'])
                    if item['comments'] > 0:
                        self.searchVideoComment(owner_id, item['id'])
                # end for
            # end for    
    #
    def searchNoteComment(self, owner_id, note_id):
        result = self.multiQuery("notes.getComments?owner_id=%d&note_id=%d" % (owner_id, note_id), 100)
        if result != None:
            for response in result:
                for item in response['items']:
                    if int(item['uid']) == self.__targetId:
                        self.writeNoteComment(owner_id, note_id, int(item['id']))
                        self.writeNoteCommentDetail(owner_id, note_id, int(item['id']), item['message'])
                # end for
            # end for  
    #
    def searchNote(self, owner_id):
        result = self.multiQuery("notes.get?owner_id=%d" % (owner_id), 100)
        if result != None:
            for response in result:
                for item in response['items']:
                    if item['owner_id'] == self.__targetId:
                        self.writeNote(owner_id, item['id'])
                        self.writeNoteDetail(owner_id, item['id'], item['title'])
                    if item['comments']['count'] > 0:
                        self.searchNoteComment(owner_id, item['id'])
                # end for
            # end for   
    #
    #  return: ID's list
    def fetchFriendIds(self, user_id):
        result = self.singleQuery("friends.get?user_id=%d" % (user_id))
        if result != None:
            return result['items']
        return []
    #
    #  return: ID's list
    def fetchFollowerIds(self, user_id):
        result = self.singleQuery("users.getFollowers?user_id=%d" % (user_id))
        if result != None:
            return result['items']
        return []
    #
    # return ID's list
    def fetchGroupIds(self, user_id):
        result = self.multiQuery("groups.get?user_id=%d" % (user_id), 1000)

        itemList = []
        if result != None:
            for response in result:
                itemList += response['items']
        return itemList
    #
    # return ID's list user_list, group_list
    def fetchSubscriptionIds(self, user_id):
        result = self.multiQuery("users.getSubscriptions?user_id=%d" % (user_id), 200)

        userList = []
        groupList = []
        if result != None:
            for response in result:
                userList += response['users']['items']
                groupList += response['groups']['items']
        return userList, groupList        

def showUsage():
    print "== vksearchactivities.py - v.0.1.0  =="
    print "Usage: "
    print "    vksearchactivities.py --access-token <> --target-id <> --users-state-file <> --groups-state-file <> --activities-file <> --activities-detail-file <> [--custom-user-ids <>][--custom-group-ids <>][--search-depth <>][--scan-groups-of-friends]"

access_token = None
purpose_id = None
users_state = None
groups_state = None
found_file = None
found_file_desc = None
deep = 0
groups_of_friends = False
custom_user_ids = []
custom_group_ids = []

try:
    options, remainder = getopt.getopt(sys.argv[1:], 'o:v', ['access-token=', 'target-id=', 'users-state-file=', 'groups-state-file=', 'activities-file=', 'activities-detail-file=', 'custom-user-ids=', 'custom-group-ids=', 'search-depth=', 'scan-groups-of-friends'])
    for opt, arg in options:
        if opt == '--access-token':
            access_token = arg
        elif opt == '--target-id':
            purpose_id = int(arg)
        elif opt == '--users-state-file':
            users_state = arg
        elif opt == '--groups-state-file':
            groups_state = arg
        elif opt == '--activities-file':
            found_file = arg
        elif opt == '--activities-detail-file':
            found_file_desc = arg
        elif opt == "--search-depth":
            deep = int(arg)
        elif opt == "--custom-user-ids":
            custom_user_ids = arg.split(",")
        elif opt == "--custom-group-ids":
            custom_group_ids = arg.split(",")
        elif opt == "--scan-groups-of-friends":
            groups_of_friends = True
except:
    showUsage()
    exit(-1)

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
print "Custom user ids        :", custom_user_ids
print "Custom group ids       :", custom_group_ids

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

searcher = ActivitiesSearcher()
searcher.openActivitiesFile(found_file)
searcher.openActivitiesDetailFile(found_file_desc)
searcher.setAccessToken(access_token)
searcher.setTargetId(purpose_id)

# setup timeout
socket.setdefaulttimeout(3)

# result: userList, groupList
def weNeedToBeDeeper(user_id, access_token, deep, processedUserList):
    # info
    print "Deep = %d, user_id = %d | Processing number = %d" % (deep, user_id, len(processedUserList))    
    # process the user    
    userFriendList = searcher.fetchFriendIds(user_id)
    userFollowList = searcher.fetchFollowerIds(user_id)
    userGroupList = searcher.fetchGroupIds(user_id)
    userSubscribeUserList, mySubscribeGroupList = searcher.fetchSubscriptionIds(user_id)
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
    userFriendList = searcher.fetchFriendIds(user_id)
    userFollowList = searcher.fetchFollowerIds(user_id)
    userSubscribeUserList, mySubscribeGroupList = searcher.fetchSubscriptionIds(user_id)
    localUserList = userFriendList + userFollowList + userSubscribeUserList
    # scan groups
    groups = []
    for id in localUserList:
        groups += searcher.fetchGroupIds(id)
    return groups
    
userList, groupList, processedUserList = weNeedToBeDeeper(purpose_id, access_token, deep, [])
userList = list(set(userList + [purpose_id]))
if deep == 0 and groups_of_friends:
    groupList = list(set(groupList + groupsOfFriends(purpose_id, access_token)))

# add custom ids
for id in custom_user_ids:
    userList += [int(id)]
for id in custom_group_ids:
    groupList += [int(id)]

# remove duplicate
userList = list(set(userList))
groupList = list(set(groupList))    

print "Total users count :", len(userList)
print "Total groups count:", len(groupList)

# scan
for id in userList:
    if id in processedUsers:
        print "User %d already processed" % (id)
        continue
    searcher.searchPost(id)
    searcher.searchPhoto(id)
    searcher.searchPhotoComment(id)
    searcher.searchVideo(id)
    searcher.searchNote(id)
    fUsers.write("%d;" % (id))
    processedUsers.append(id)
for id in groupList:
    if id in processedGroups:
        print "Group %d already processed" % (id)
        continue
    searcher.searchPost(-id)
    searcher.searchPhoto(-id)
    searcher.searchPhotoComment(-id)
    searcher.searchVideo(-id)
    searcher.searchTopic(id)
    fGroups.write("%d;" % (id))
    processedGroups.append(id)

fUsers.close()
fGroups.close()
    
# deconfigure
searcher.closeActivitiesFile()
searcher.closeActivitiesDetailFile()
