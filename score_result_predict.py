__author__ = 'LiGe'
#encoding:utf-8
def predict_test(predict_user):
    f=open('test.txt','rb')
    datas=f.readlines()
    predict=list()
    total=0
    for line in datas:
        predict.append((line[0],line[1]))

    for item in predict:
        for line in predict_user:
            if item[0]==line[0]:
                if item[1]==line[1]:
                    total=total+1
    score=float(total)/float(len(predict_user))
    print score
