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
#
# The remove order:
# * POST_COMMENT owner_id, post_id, comment_id
# * POST owner_id, post_id
# * PHOTO_COMMENT owner_id, comment_id
# * PHOTO owner_id, photo_id
# * VIDEO_COMMENT owner_id, video_id, comment_id
# * VIDEO owner_id, topic_id
# * TOPIC_COMMENT group_id, topic_id, comment_id
# * TOPIC group_id, topic_id
# * NOTE_COMMENT user_id, note_id, comment_id
# * NOTE user_id, note_id
import urllib2, json, time, getopt, sys, socket

def executeQuery(query):
    localQuery = query
    while True:
        print localQuery
        try:
            f = urllib2.urlopen(localQuery)
            data = json.load(f)
            f.close()
        except:
            time.sleep(2)
            continue
        
        if "error" in data:
            print "ERROR: ", data
            # captcha needed
            if data["error"]["error_code"] == 14:
                captcha = raw_input("Enter a captcha code:")
                localQuery = query + "&captcha_sid=%d&captcha_key=%s" % (int(data['error']['captcha_sid']), captcha)
                continue
            if data["error"]["error_code"] == 15:
                return False
            # user was deleted or banned
            if data["error"]["error_code"] == 18:
                return False
            # too many queryes per second
            if data["error"]["error_code"] == 6:
                time.sleep(0.5)
                continue
            else:
                #print "ERROR: ", data
                return False
        # end if
    
        return True
    # end while        

def removeWallComment(access_token, owner_id, comment_id):
    return executeQuery("https://api.vk.com/method/wall.deleteComment?v=5.2&access_token=%s&owner_id=%d&comment_id=%d" % (access_token, int(owner_id), int(comment_id)))

def removeWall(access_token, owner_id, post_id):
    return executeQuery("https://api.vk.com/method/wall.delete?v=5.2&access_token=%s&owner_id=%d&post_id=%d" % (access_token, int(owner_id), int(post_id)))

def removePhotoComment(access_token, owner_id, comment_id):
    return executeQuery("https://api.vk.com/method/photos.deleteComment?v=5.2&access_token=%s&owner_id=%d&comment_id=%d" % (access_token, int(owner_id), int(comment_id)))

def removePhoto(access_token, owner_id, photo_id):
    return executeQuery("https://api.vk.com/method/photos.delete?v=5.2&access_token=%s&owner_id=%d&photo_id=%d" % (access_token, int(owner_id), int(photo_id)))

def removeVideoComment(access_token, owner_id, comment_id):
    return executeQuery("https://api.vk.com/method/video.deleteComment?v=5.2&access_token=%s&owner_id=%d&comment_id=%d" % (access_token, int(owner_id), int(comment_id)))

def removeVideo(access_token, owner_id, video_id):
    return executeQuery("https://api.vk.com/method/video.delete?v=5.2&access_token=%s&owner_id=%d&video_id=%d" % (access_token, int(owner_id), int(video_id)))

def removeTopicComment(access_token, group_id, topic_id, comment_id):
    return executeQuery("https://api.vk.com/method/board.deleteComment?v=5.2&access_token=%s&group_id=%d&topic_id=%d&comment_id=%d" % (access_token, int(group_id), int(topic_id), int(comment_id)))

def removeTopic(access_token, group_id, topic_id):
    return executeQuery("https://api.vk.com/method/board.deleteTopic?v=5.2&access_token=%s&group_id=%d&topic_id=%d" % (access_token, int(group_id), int(topic_id)))

def removeNoteComment(access_token, owner_id, comment_id):
    return executeQuery("https://api.vk.com/method/notes.deleteComment?v=5.2&access_token=%s&owner_id=%d&comment_id=%d" % (access_token, int(owner_id), int(comment_id)))

def removeNote(access_token, note_id):
    return executeQuery("https://api.vk.com/method/notes.delete?v=5.2&access_token=%s&note_id=%d" % (access_token, int(note_id)))

def showUsage():
    print "== vkdelete.py - v.0.1.0  =="
    print "Usage: "
    print "    vkdelete.py --access_token <> --activity-file <>"


access_token = None
activity_file = None

options, remainder = getopt.getopt(sys.argv[1:], 'o:v', ['access_token=', 'activity-file='])
for opt, arg in options:
    if opt == '--access_token':
        access_token = arg
    elif opt == '--activity-file':
        activity_file = arg

if access_token == None or activity_file == None:
    showUsage()
    exit(-1)

print "Access token :", access_token
print "Activty file :", activity_file

# vk can hold the connection for a long time
socket.setdefaulttimeout(3)

# read lines with activities
dbFile = open(activity_file, 'r')
lines = dbFile.read().split("\n")
lines = list(set(lines))

# remove POST_COMMENT
total_count = delete_count = 0
for line in lines:
    if 'POST_COMMENT ' in line:
        [type_id, owner_id, post_id, comment_id] = line.split(" ")
        if removeWallComment(access_token, owner_id, comment_id) == True:
            delete_count += 1
        total_count += 1
print "POST_COMMENT: %d of %d was removed" % (delete_count, total_count)

# remove POST
total_count = delete_count = 0
for line in lines:
    if 'POST ' in line:
        [type_id, owner_id, post_id] = line.split(" ")
        if removeWall(access_token, owner_id, post_id) == True:
            delete_count += 1
        total_count += 1
print "POST: %d of %d was removed" % (delete_count, total_count)

# remove PHOTO_COMMENT
total_count = delete_count = 0
for line in lines:
    if 'PHOTO_COMMENT ' in line:
        [type_id, owner_id, comment_id] = line.split(" ")
        if removePhotoComment(access_token, owner_id, comment_id) == True:
            delete_count += 1
        total_count += 1
print "PHOTO_COMMENT: %d of %d was removed" % (delete_count, total_count)

# remove PHOTO
total_count = delete_count = edit_count = 0
for line in lines:
    if 'PHOTO ' in line:
        [type_id, owner_id, photo_id] = line.split(" ")
        if removePhoto(access_token, owner_id, photo_id) == True:
            delete_count += 1
        total_count += 1
print "PHOTO: %d of %d was removed" % (delete_count, total_count)

# remove VIDEO_COMMENT
total_count = delete_count = 0
for line in lines:
    if 'VIDEO_COMMENT ' in line:
        [type_id, owner_id, video_id, comment_id] = line.split(" ")
        if removeVideoComment(access_token, owner_id, comment_id) == True:
            delete_count += 1
        total_count += 1
print "VIDEO_COMMENT: %d of %d was removed" % (delete_count, total_count)

# remove VIDEO
total_count = delete_count = edit_count = 0
for line in lines:
    if 'VIDEO ' in line:
        [type_id, owner_id, video_id] = line.split(" ")
        if removeVideo(access_token, owner_id, video_id) == True:
            delete_count += 1
        total_count += 1
print "VIDEO: %d of %d was removed" % (delete_count, total_count)

# remove TOPIC_COMMENT
total_count = delete_count = 0
for line in lines:
    if 'TOPIC_COMMENT ' in line:
        [type_id, group_id, topic_id, comment_id] = line.split(" ")
        if removeTopicComment(access_token, group_id, topic_id, comment_id) == True:
            delete_count += 1
        total_count += 1
print "TOPIC_COMMENT: %d of %d was removed" % (delete_count, total_count)

# remove TOPIC
total_count = delete_count = edit_count = 0
for line in lines:
    if 'TOPIC ' in line:
        [type_id, group_id, topic_id] = line.split(" ")
        if removeTopic(access_token, group_id, topic_id) == True:
            delete_count += 1
        total_count += 1
print "TOPIC: %d of %d was removed" % (delete_count, total_count)


# remove NOTE_COMMENT
total_count = delete_count = 0
for line in lines:
    if 'NOTE_COMMENT ' in line:
        [type_id, user_id, note_id, comment_id] = line.split(" ")
        if removeNoteComment(access_token, note_id, comment_id) == True:
            delete_count += 1
        total_count += 1
print "NOTE_COMMENT: %d of %d was removed" % (delete_count, total_count)

# remove NOTE
total_count = delete_count = edit_count = 0
for line in lines:
    if 'NOTE ' in line:
        [type_id, user_id, note_id] = line.split(" ")
        if removeNote(access_token, note_id) == True:
            delete_count += 1
        total_count += 1
print "NOTE: %d of %d was removed" % (delete_count, total_count)
