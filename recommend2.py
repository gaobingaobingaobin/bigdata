__author__ = 'LiGe'
#encoding:utf-8
import csv
from numpy import *
from read_file1 import csv_to_list


def RBF(user_item,user,d,user_item_time,alpha=0.02):
    interres=list(set(user_item[user]).intersection(set(user_item[d])))
    sum=0
    t1=0
    t2=0
    simi=0.0
    for item in interres:
        for line in user_item_time[user]:
            if line[0]==item:
                t1=line[1]
                break
        for line in user_item_time[d]:
            if line[0]==item:
                t2=line[1]
                break
        sum=sum+1/(1+alpha*abs(float(t1)-float(t2)))
        simi=float(sum)/float(math.sqrt(len(user_item[user])*len(user_item[d])))
    return simi


def pearsSim(user, user_item,user_item_time):
    score=list()
    for d in user_item:
        if d==user:continue
        sim=RBF(user_item,user,d,user_item_time,alpha=0.02)
        score.append((sim,d))
    return sorted(score, key=lambda jj:jj[0], reverse=True)[:120]


def sim(k,item,user_item,user_item_time,fre,alpha=0.02):#求物品与物品的相似度,考虑了时间维度,找出有两种物品的用户，然后计算其距离，采用的是基于项目相似性的计算
    count=0
    score=0
    t1=0.0
    t2=0.0
    for line in user_item:
        flag1=0
        flag2=0
        score=0
        if k in user_item[line]:
            if item in user_item[line]:
                for item_time in user_item_time[line]:
                    if item_time[0]==k:
                        t1=item_time[1]
                        flag1=1
                    if item_time[0]==item:
                        t2=item_time[1]
                        flag2=1
                    if flag1 and flag2:
                        break
                score=1/(1+alpha*abs(float(t1)-float(t2)))
        count=count+score
    count=count/math.sqrt(fre[k]*fre[item])
    return count


def interest_distribution(user,user_item,user_item_time,item_fre,h=0.4):#对用户未读项的分布的计算
    #user_item_interest_socre=dict()
    item_interest_score=list()
    for item in item_fre:#记住，一定是按照顺序放入list中的，是按照同一种顺序放入的
        if item not in user_item[user]:#对未知项进行评分估计
            count=0.0
            for k in user_item[user]:
                distance=1-sim(k,item,user_item,user_item_time,item_fre)
                #print distance
                count=count+math.exp(-float(distance*distance)/float(2*h*h))
            count=count/(len(user_item[user])*math.sqrt(2*math.pi)*h)
            item_interest_score.append((item,count))
    return item_interest_score

def create_feature(user,recos,user_item):
    union_item=dict()
    local_user_item=dict()
    for line in recos:
        for data in user_item[line[1]]:
            if data not in union_item:
                union_item[data]=1
            else:
                union_item[data]=union_item[data]+1
    for line in user_item[user]:
        if line not in union_item:
            union_item[line]=1
        else:
            union_item[line]=union_item[line]+1
    for line in recos:
        local_user_item[line[1]]=user_item[line[1]]
    local_user_item[user]=user_item[user]
    return union_item,local_user_item


def recommend1():
    j=0
    csvfile = file('csv_result12.csv', 'wb')
    writer=csv.writer(csvfile)
    user_item,user_item_time,ignore_user=csv_to_list()
    predict=list()
    print ignore_user
    print len(ignore_user)
    for user in user_item:
        if user not in ignore_user:
            recos=pearsSim(user,user_item,user_item_time)#求解相似用户
            item_fre,local_user_item=create_feature(user,recos,user_item)
            item_score=interest_distribution(user,local_user_item,user_item_time,item_fre,h=0.4)
            number=len(user_item[user])
            if number>20:
                number=20
            final_result=sorted(item_score, key=lambda jj:jj[1], reverse=True)[:(number/10)+1]
            for line in final_result:
                    writer.writerow((user,line[0]))
                    j=j+1
        print j

    csvfile.close()
    return predict

if __name__=='__main__':
    predict=recommend1()




