# -*- coding: UTF-8 -*-
# work on the centos because I modify itchat's login src
import itchat
from itchat.content import TEXT
import time
import re
import datetime
def isWeekend(year,month,day):
    day=datetime.datetime(year,month,day).isoweekday()
    if day==6 or day==7:
        return True
    else:
        return False
def searchRecentBus(start,end):
    '''
    z:张江校区
    h:邯郸校区
    f:枫林校区
    j:江湾校区
    A：两辆校车
    B:三辆校车
    :param start:起点
    :param end: 终点
    :return:最近的一班校车时间
    '''
    z2h_time=['0715','0800','0840','0900','1000','1150B','1215','1240','1415','1520','1600','1610','1620','1640','1700','1720','1830','2110']
    z2h_time_weekend=['0920','1730']
    h2z_time=['0710','0740','0800','0830','0900','1000','1150','1230','1245','1430','1530','1615','1720B','1830','2020A','2030','2100','2120B']
    h2z_time_weekend=['0830','1630']
    f2z_time=['0700','0730','0900','1215','1330','1630','1900']
    z2f_time=['0750','1215','1500','1700','1900']
    j2h_time=['0710','0720','0730','0740','0750','0800','0815','0830','0845','0900B','0915','0930','1000','1030','1110','1140','1200','1215','1230','1240','1300','1330','1400','1500B','1515','1530','1600','1630','1655','1700','1710','1730','1800B','1900','2000','2030','2100','2120','2145','2210']
    j2h_time_weekend=['0740','0800','0820','0840','0900','0920','0940','1020','1730B','2040','2120','2210']
    h2j_time=['0730','0740','0800','0830B','0900','0930','1000','1020','1100','1130','1145','1200','1230','1300','1330','1400','1430','1500','1530','1600','1615','1620','1630','1700','1715','1725','1735','1745','1800','1830','2000','2020','2030','2050','2100','2120','2140','2200','2215','2230']
    h2j_time_weekend=['0820','0840','0900','0920','0940','1700B','2015','2100','2145','2230']
    f2h_time=['0710','0720','0815','0915','1100','1145','1215','1300','1400','1430','1530','1600','1655','1710','1725','1820','2020','2115','2150']
    f2h_time_weekend=['0900','1730']
    h2f_time=['0655','0710','0815','0915','1015','1100','1230','1300','1400','1530','1600','1655','1710','1800','1930','2020B','2125B']
    h2f_time_weekend=['0800','1630']
    h2z_all=z2h_all="详情可查看：http://www.bxs.fudan.edu.cn/answer.php?answer=138.jpg"
    f2z_all=z2f_all="详情可查看：http://www.bxs.fudan.edu.cn/answer.php?answer=137.jpg"
    j2h_all=h2j_all="详情可查看：http://www.bxs.fudan.edu.cn/answer.php?answer=139.jpg"
    f2h_all=h2f_all="详情可查看：http://www.bxs.fudan.edu.cn/answer.php?answer=136.jpg"
    bus_all="所有校车：https://mp.weixin.qq.com/s/14J8dupUACPUJayCRdbEmw"
    notify='有车'
    bus_time=None
    all=None
    year=int(time.strftime("%Y",time.localtime()))
    month=int(time.strftime("%m",time.localtime()))
    day=int(time.strftime("%d",time.localtime()))
    if start == 'z'and end=='h' and not isWeekend(year,month,day):
        bus_time =z2h_time
        all=z2h_all
    if start == 'z'and end=='h' and isWeekend(year,month,day):
        bus_time =z2h_time_weekend
        all=bus_all
    if start=='h'and end=='z'and not isWeekend(year,month,day):
        bus_time=h2z_time
        all=h2z_all
    if start=='h'and end=='z'and isWeekend(year,month,day):
        bus_time=h2z_time_weekend
        all=bus_all
    if start=='f'and end=='z'and not isWeekend(year,month,day):
        bus_time=f2z_time
        all=f2z_all
    if start=='z'and end=='f' and not isWeekend(year,month,day):
        bus_time=z2f_time
        all=z2f_all
    if start=='f'and end=='z'and isWeekend(year,month,day):
        return '该方向双休日没车',None,None,bus_all
    if start=='z'and end=='f' and isWeekend(year,month,day):
        return '该方向双休日没车',None,None,bus_all

    now=int(time.strftime("%H%M",time.localtime()))
    next_bus_count=None
    next_next_bus_count=None
    nextBus = None
    nextNextBus=bus_time[-1]
    if len(nextNextBus)==5:
        if nextNextBus[4]=='A':
            next_next_bus_count='三辆'
        if nextNextBus[4]=='B':
            next_next_bus_count='两辆'
    else:
        next_next_bus_count='一辆'
    for i in bus_time:
        if len(i)==5:
            if i[4]=='A':
                next_bus_count='三辆'
            if i[4]=='B':
                next_bus_count='两辆'
            i=i[0:4]
        else:
            next_bus_count='一辆'
        if(int(i)>now):
            nextBus=i
            break
    if(nextBus==None):
        notify='没车'
        nextBus='最后一班（{}）：'.format(next_next_bus_count)+str(int(nextNextBus[0:2]))+':'+nextNextBus[2:4]
        nextNextBus='最后一班（{}）：'.format(next_next_bus_count)+str(int(nextNextBus[0:2]))+':'+nextNextBus[2:4]
    else:
        temp=nextBus
        if next_bus_count == '三辆':
            temp += 'A'
        if next_bus_count == '两辆':
            temp += 'B'
        if next_bus_count == '一辆':
            pass
        if temp==bus_time[-1]:
            nextBus = '下一班（{}）：'.format(next_bus_count) + str(int(nextBus[0:2])) +':'+ nextBus[2:4]
            nextNextBus = '下下一班没了，最后一班（{}）：'.format(next_next_bus_count) + str(int(nextNextBus[0:2]))+':' + nextNextBus[2:4]
        else:
            temp=nextBus
            if next_bus_count=='三辆':
                temp+='A'
            if next_bus_count=='两辆':
                temp+='B'
            if next_bus_count=='一辆':
                pass
            index=bus_time.index(temp)+1
            nextNextBus=bus_time[index]
            if len(nextNextBus) == 5:
                if nextNextBus[4] == 'A':
                    next_next_bus_count = '三辆'
                if nextNextBus[4] == 'B':
                    next_next_bus_count = '两辆'
            else:
                next_next_bus_count = '一辆'
            nextBus = '下一班（{}）：'.format(next_bus_count) + str(int(nextBus[0:2])) +':'+ nextBus[2:4]
            nextNextBus = '下下一班（{}）：'.format(next_next_bus_count) + str(int(nextNextBus[0:2])) +':'+ nextNextBus[2:4]
    return notify,nextBus,nextNextBus,all

@itchat.msg_register([TEXT])
def msg_receive(msg):
     '''
     :param msg:
     :return:
     '''
     if re.match(u'.*校车.*',msg['Content']):
         msg.user.send('想查询最近一班校车？请回复help进行查询。')
     if msg['Content']=='help':
         help=('z:张江校区'+'\n'+
                'h:邯郸校区'+'\n'+
                'f:枫林校区'+'\n'+
                'j:江湾校区'+'\n'+'例如：查询张江到邯郸的最近一班校车，则回复：zh'+'\n')
         msg.user.send(help)
     if msg['Content'] in ['zh','hz','fz','zf','jh','hj','fh','hf']:
        start=msg['Content'][0]
        end=msg['Content'][1]
        notify,nextBus,nextNextBus,all=searchRecentBus(start,end)
        msg.user.send(notify+'\n'+nextBus+'\n'+nextNextBus+'\n'+all)

# itchat.auto_login(hotReload=True)
# itchat.run()
itchat.auto_login(enableCmdQR=2,picDir='/root/QR.png',hotReload=False)
itchat.run()
