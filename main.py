#!/usr/bin/env python
#coding: utf8
import os
import sys
if '__file__' in globals():
    path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(path)
import conf
from lib import *
from time import sleep, gmtime
from pub2all import pub2all

def twitter2all():
    from twitter import get_twitter_status
    
    prevtime = load_prev_time(conf.twitter_user)
    statuses = get_twitter_status(conf.twitter_user, prevtime)
    
    for status, pubdate in statuses:
        if status[0] in conf.exclude:
            continue
        print pubdate, status
        if pub2all(status):
            save_prev_time(conf.twitter_user, pubdate)
            sleep(10)
        
def feeds2all():
    from rss import get_rss_entries
    
    lasttimes = loadfrom('rss_lasttimes')
    if lasttimes is None:
        lasttimes = {}
        
    for format_, url in conf.feeds:
        lasttime = lasttimes.get(url, None)
        if lasttime is None:
            lasttimes[url] = gmtime()
            dumpto('rss_lasttimes', lasttimes)
            continue
        
        statuses = get_rss_entries(url, lasttime)
        maxtime = lasttime
        
        for status, publishtime in statuses:
            status = format_ % status
            print publishtime, status

            if pub2all(status):
                if maxtime < publishtime:
                    maxtime = publishtime
                sleep(10)
            
        lasttimes[url] = maxtime
        dumpto('rss_lasttimes', lasttimes)

if __name__ == '__main__':
    twitter2all()
    feeds2all()
