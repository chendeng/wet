from renren import Renren
from sina import Sina
from douban import Douban
from twitter import get_twitter_status
from lib import *
from conf import *

def pub2renren(status):
    renren = Renren(renren_user, renren_passwd)
    renren.login()
    renren.update(status)
    
def pub2sina(status, pic=''):
    sina = Sina(sina_user, sina_passwd)
    sina.login()
    sina.update(status, pic)

def pub2douban(status):
    douban = Douban(douban_user, douban_passwd)
    douban.login()
    douban.update(status)


def main():
    from time import sleep
    prevtime = load_prev_time(twitter_user)
    statuses = get_twitter_status(twitter_user, prevtime)
    for status, pubdate in statuses:
        if status.startswith('.') or status.startswith('@'):
            continue
        print pubdate, status
        if sina_user and sina_passwd:
            try:
                pub2sina(status)
                save_prev_time(twitter_user, pubdate)
            except Exception, e:
                log('pub2sina error: %s' % str(e))
        
        if douban_user and douban_passwd:
            try:
                pub2douban(status)
                save_prev_time(twitter_user, pubdate)
            except Exception, e:
                log('pub2douban error: %s' % str(e))
        
        if renren_user and renren_passwd:
            try:
                pub2renren(status)
                save_prev_time(twitter_user, pubdate)
            except Exception, e: 
                log('pub2renren error: %s' % str(e))
        sleep(10)


if __name__ == '__main__':
    main()
