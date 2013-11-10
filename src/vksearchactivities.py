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
import urllib2, json, time, codecs, getopt, sys, socket, os

#
def printMessage(message):
    print time.strftime("%Y-%m-%d %H:%M:%S:", time.gmtime()), message

#
class ActivitiesSearcher:
    # -------------------------------------------------------------------------
    # section: settings
    # -------------------------------------------------------------------------
    #
    __targetId = None
    __accessToken = None
    __apiVersion = 5.2
    __showApiQuery = False
    __showApiError = False
    #
    def setAccessToken(self, accessToken):
        self.__accessToken = accessToken
    #
    def accessToken(self):
        return self.__accessToken
    #
    def setApiVersion(self, apiVersion):
        self.__apiVersion = apiVersion
    #
    def setTargetId(self, id):
        self.__targetId = id
    #
    def targetId(self):
        return self.__targetId
    #
    def setShowApiQuery(self, state):
        self.__showApiQuery = state
    #
    def isShowApiQuery(self):
        return self.__showApiQuery
    #
    def setShowApiError(self, state):
        self.__showApiError = state
    #
    def isShowError(self):
        return self.__showApiError
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
            if self.__showApiQuery:
                printMessage(url)
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
                if self.__showApiError:
                    printMessage(data)
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

#
class StateStorage:
    #
    __stateFile = None
    __processedSet = set()
    #
    def open(self, fileName, rewrite = False):
        if rewrite == False:
            lines = []
            try:
                file = open(fileName, "r")    
                lines = file.readlines()
                file.close()
            except:
                printMessage("state file not found %s" % (fileName))
            #
            for item in lines:
                self.__processedSet.add(int(item))
            #
            try:
                self.__stateFile = open(fileName, "a")
                printMessage("open state file for append %s" % (fileName))
            except:
                printMessage("can't open state file for append %s" % (fileName))
        # end if
    #
    def close(self):
        self.__stateFile.close()
    #
    def contains(self, item):
        return item in self.__processedSet
    #
    def add(self, item):
        if not self.contains(int(item)):
            self.__processedSet.add(int(item))
            self.__stateFile.write("%d\n" % int(item))
            self.__stateFile.flush()
            os.fsync(self.__stateFile)
    # 
    def addList(self, itemList):
        for item in itemList:
            self.add(item)
    # 
    def userList(self):
        userList = []
        for item in self.__processedSet:
            if item > 0:
                userList.append(item)
        return userList
    # 
    def groupList(self):
        userList = []
        for item in self.__processedSet:
            if item < 0:
                userList.append(item)
        return userList
# 
def showUsage():
    print "== vksearchactivities.py - v.0.1.0  =="
    print "Usage: "
    print "    vksearchactivities.py --access-token <> --target-id <> "     \
    "--state-file <> --activities-file <> --activities-detail-file <> "     \
    "[--custom-user-ids <>][--custom-group-ids <>][--search-user-depth <>]" \
    "[--search-group-depth <>][--show-api-queries][--show-api-errors]"      \
    "[--disable-scan-friends][--disable-scan-followers]"                    \
    "[--disable-scan-user-subscriptions][--disable-scan-group-subscriptions]"

#
gAccessToken = None
gTargetId = None
gActivitiesFileName = None
gActivitiesDetailFileName = None
gStateFileName = None
gCustomUserIds = []
gCustomGroupIds = []
gSearchUserDepth = 1
gSearchGroupDepth = 1
gScanFriends = True
gScanFollowers = True
gScanUserSubscriptions = True
gScanGroupSubscriptions = True
gShowApiQueries = False
gShowApiErrors = False

#
try:
    options, remainder = getopt.getopt(sys.argv[1:], 'o:v', ['access-token=', 
            'target-id=', 'state-file=', 'activities-file=', 
            'activities-detail-file=', 'custom-user-ids=', 
            'custom-group-ids=', 'search-user-depth=', 'search-group-depth=',
            'disable-scan-friends', 'disable-scan-followers',
            'disable-scan-user-subscriptions', 'disable-scan-group-subscriptions'
            'show-api-queries', 'show-api-errors'])
    for opt, arg in options:
        if opt == '--access-token':
            gAccessToken = arg
        elif opt == '--target-id':
            gTargetId = int(arg)            
        elif opt == '--state-file':
            gStateFileName = arg
        elif opt == '--activities-file':
            gActivitiesFileName = arg            
        elif opt == '--activities-detail-file':
            gActivitiesDetailFileName = arg
        elif opt == "--search-user-depth":
            gSearchUserDepth = int(arg)
        elif opt == "--search-group-depth":
            gSearchGroupDepth = int(arg)
        elif opt == "--custom-user-ids":
            gCustomUserIds = arg.split(",")
        elif opt == "--custom-group-ids":
            gCustomGroupIds = arg.split(",")
        elif opt == "--disable-scan-friends":
            gScanFriends = False
        elif opt == "--disable-scan-followers":
            gScanFollowers = False
        elif opt == "--disable-scan-user-subscriptions":
            gScanUserSubscriptions = False
        elif opt == "--ddisable-scan-group-subscriptions":
            gScanGroupSubscriptions = False
        elif opt == "--show-api-errors":
            gShowApiErrors = True
        elif opt == "--show-api-queries":
            gShowApiQueries = True
except:
    showUsage()
    exit(-1)

#
if (gAccessToken == None or gTargetId == None or gActivitiesFileName == None or 
        gActivitiesDetailFileName == None or gStateFileName == None):
    showUsage()
    exit(-1)

#
print "-------------------------------------------------------"
print "                   < Configuration >                   "
print "-------------------------------------------------------"
print "Target ID                  :", gTargetId
print "Access token               :", gAccessToken
print "State file                 :", gStateFileName
print "Activities file            :", gActivitiesFileName
print "Activities detail file     :", gActivitiesDetailFileName
print "Search user depth          :", gSearchUserDepth
print "Search group depth         :", gSearchGroupDepth
print "Scan friends               :", gScanFriends
print "Scan followers             :", gScanFollowers
print "Scan user subscription     :", gScanUserSubscriptions
print "Scan group subscription    :", gScanGroupSubscriptions
print "Custom user ID's           :", gCustomUserIds
print "Custom group ID's          :", gCustomGroupIds
print "Show API queries           :", gShowApiQueries
print "Show API errors            :", gShowApiErrors
print "-------------------------------------------------------"

#
state = StateStorage()
state.open(gStateFileName)

#
searcher = ActivitiesSearcher()
searcher.setAccessToken(gAccessToken)
searcher.setTargetId(gTargetId)
searcher.openActivitiesFile(gActivitiesFileName)
searcher.openActivitiesDetailFile(gActivitiesDetailFileName)
searcher.setShowApiQuery(gShowApiQueries)
searcher.setShowApiError(gShowApiErrors)

# setup timeout because vk may keep the connection for a long time
socket.setdefaulttimeout(3)

#
print "-------------------------------------------------------"

# first, list is empty
totalUserList = []
totalGroupList = []

#
def weNeedToBeDeeper(user_id, processedUserList, depth):
    global totalUserList, totalGroupList
    # we shouldn't scan user_id in the future
    processedUserList += [user_id]
    #
    if depth == 0:
        printMessage("[*] Fetching friends and groups... (UserId = %d)" % (user_id))
    #
    userList = []
    groupList = []
    #
    if gScanFriends:
        userList += searcher.fetchFriendIds(user_id)
    if gScanFollowers:
        userList += searcher.fetchFollowerIds(user_id)
    if gScanUserSubscriptions or gScanGroupSubscriptions:
        users, groups = searcher.fetchSubscriptionIds(user_id)
        if gScanUserSubscriptions:
            userList += users
        if gScanGroupSubscriptions:
            groupList += groups
    #
    if depth < gSearchGroupDepth:
        totalGroupList += groupList + searcher.fetchGroupIds(user_id)
    #
    if depth < gSearchUserDepth:
        totalUserList += userList
    #        
    if depth+1 < gSearchUserDepth or depth+1 < gSearchGroupDepth:
        num = 0
        for id in userList:
            num += 1
            printMessage("%s[+] Fetching friends and groups... User %d of %d is processing (UserId = %d)" % 
                    ('   ' * (depth+1), num, len(userList), id))
            if id not in processedUserList:
                processedUserList = weNeedToBeDeeper(id, processedUserList, depth+1)
    #
    return processedUserList
#
processedUserList = weNeedToBeDeeper(gTargetId, [], 0)

# add custom user/group ids
for id in gCustomUserIds:
    totalUserList += [int(id)]
for id in gCustomGroupIds:
    totalGroupList += [int(id)]

# remove duplicates 
# we woun't scan page of gTargetId
totalUserList = set(totalUserList)
totalUserList.discard(gTargetId)
totalUserList = list(totalUserList)
#
totalGroupList = list(set(totalGroupList))

#
print "-------------------------------------------------------"
print "                     < Summarize >                     "
print "-------------------------------------------------------"
print "Total user count           :", len(totalUserList)
print "Total group count          :", len(totalGroupList)
print "-------------------------------------------------------"

# search targetId on the user pages
num = userNum = 0
for id in totalUserList:
    #
    userNum += 1    
    num += 1
    printMessage("Search progress %.3f%%: processing %d of %d users (UserId = %d)" % 
        ((num * 100.0)/(len(totalUserList) + len(totalGroupList)), userNum, len(totalUserList), id))
    #
    if state.contains(id):
        printMessage("[*] User with ID = %d already processed" % (id))
        continue
    searcher.searchPost(id)
    searcher.searchPhotoComment(id)
    searcher.searchVideo(id)
    searcher.searchNote(id)
    state.add(id)

# search targetId on the group pages
groupNum = 0
for id in totalGroupList:
    #
    groupNum += 1    
    num += 1
    printMessage("Search progress %.3f%%: processing %d of %d groups (GroupId = %d)" %
        ((num * 100.0)/(len(totalUserList) + len(totalGroupList)), groupNum, len(totalGroupList), id))
    #    
    if state.contains(-id):
        printMessage("[*] Group with ID = %d already processed" % (-id))
        continue
    searcher.searchPost(-id)
    searcher.searchPhoto(-id)
    searcher.searchPhotoComment(-id)
    searcher.searchVideo(-id)
    searcher.searchTopic(id)
    state.add(-id)
    
# deconfigure
searcher.closeActivitiesFile()
searcher.closeActivitiesDetailFile()
state.close()