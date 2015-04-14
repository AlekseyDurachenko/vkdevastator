#!/usr/bin/python2
# -*- coding: utf-8 -*-
#
# Copyright 2015, Durachenko Aleksey V. <durachenko.aleksey@gmail.com>
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
import getopt, sys
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


def showUsage():
    print "== vkcreatelinks.py - v.0.1.0  =="
    print "Usage: "
    print "    vkcreatelinks.py --i activities.txt"

filename = None

try:
    options, remainder = getopt.getopt(sys.argv[1:], 'o:v', ['i='])
    for opt, arg in options:
        if opt == '--i':
            filename = arg
except:
    showUsage()
    exit(-1)

f = open(filename, 'r')
for line in f.readlines():
    items = line.strip().split()
    if items[0] == "POST_COMMENT":
        print "https://vk.com/wearyinside?w=wall%s_%s" % (items[1], items[2])
    elif items[0] == "POST":
        print "https://vk.com/wearyinside?w=wall%s_%s" % (items[1], items[2])
    #elif items[0] == "PHOTO_COMMENT":
    #    print "https://vk.com/photo%s_%s" % (items[2], items[1])
    #elif items[0] == "PHOTO":
    #    print "https://vk.com/photo%s_%s" % (items[2], items[1])
