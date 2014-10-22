#encoding:utf-8
import time
import datetime
from latest_new import map_time


def cmp_time(t1,t2):
    time1 = t1.split(':')
    time2 = t2.split(':')
    if int(time1[0]) > int(time2[0]):
        return 1
    elif int(time1[0]) < int(time2[0]):
        return -1
    elif int(time1[1]) > int(time2[1]):
         return 1
    elif int(time1[1]) < int(time2[1]):
        return -1
    else:
        return 0

def format_time(t1):
    #2012-12-3 0:0:0
    t1=t1.replace('年','-')
    t1=t1.replace('月','-')
    t1=t1.replace('日',' ')
    if t1.find(':')<0:
        t1=t1+'00:00'
    t1=t1+':00'
    s = t1
    d = datetime.datetime.strptime(s,"%Y-%m-%d  %H:%M:%S")
    return d

def draw_time(news_time):
    #2012-12-3 0:0:0
    day_news = {}
    day_late = {}
    day_early = {}
    day = -1
    for news_num, t1 in news_time.items():
        if t1=='NULL':
            continue
        date_list = str(format_time(t1)).split()# 格式 2014-02-24  14:41:00
        y_m_d = date_list[0].split('-')
        if int(y_m_d[0])!=2014:
            continue
        if int(y_m_d[1])!=3:
            continue
        day = int(y_m_d[2])
        time = date_list[1]
        day_news.setdefault(day, set()).add(news_num)
        # day_late.setdefault(day,'')
        current = day_late.get(day)
        if current is not None:
            if cmp_time(current,time) < 0:
                day_late[day] = time
        else:
            day_late[day] = time

        early = day_early.get(day)
        if early is not None:
            if cmp_time(early,time) > 0:
                day_early[day] = time
        else:
            day_early[day] = time

    return day_news, day_late, day_early




if __name__=='__main__':
    latest_time,news_time=map_time()
    day_news, day_late, day_early = draw_time(news_time)
    print 'every day\'s news:'
    print day_news
    print
    print 'every day\'s earliest issue time:'
    print day_early
    print
    print 'every day\'s latest issue time:'
    print day_late


    # print day_news.keys()
    # print day_late.keys()
    # print day_early.keys()
