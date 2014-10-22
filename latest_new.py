__author__ = 'LiGe'
#encoding:utf-8
#记录每个用户的最后浏览的时间，以及每个新闻的发布时间


def map_time():
    f=open('train_data.txt','r')
    datas=f.readlines()
    users=set()
    user_late_time=dict()
    #news_time=dict()
    for line in datas:
        line=line.strip()
        line=line.split('\t')
        #news_time[line[1]]=line[5]
        if line[0] not in users:
            users.add(line[0])
            user_late_time[line[0]]=line[2]
    return user_late_time
