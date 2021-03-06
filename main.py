# -*- coding: UTF-8 -*-
# work on the centos because I modify itchat's login src
import itchat
from itchat.content import TEXT
import time
import re
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

start_date = datetime.datetime(2020, 10, 12)
day = datetime.timedelta(days=1)
duty_dict = {"高佳楠": [start_date + i * day for i in range(7)], "俞杰": [start_date + i * day for i in range(7, 14)],
             "李谨慎": [start_date + i * day for i in range(14, 21)], "周振涛": [start_date + i * day for i in range(21, 28)],
             "龚恩磊": [start_date + i * day for i in range(28, 35)]}


def isWeekend(year, month, day):
    day = datetime.datetime(year, month, day).isoweekday()
    if day == 6 or day == 7:
        return True
    else:
        return False


def searchRecentBus(start, end):
    """
    z:张江校区
    h:邯郸校区
    f:枫林校区
    j:江湾校区
    A：两辆校车
    B:三辆校车
    :param start:起点
    :param end: 终点
    :return:最近的一班校车时间
    """
    z2h_time = ['0700', '0715', '0800', '0840', '0900', '1000', '1150B', '1215', '1240', '1415', '1520', '1600', '1610',
                '1620', '1640', '1700', '1720', '1830', '2110']
    z2h_time_weekend = ['0920', '1730']
    h2z_time = ['0710', '0740', '0800', '0830', '0900', '1000', '1150', '1230', '1245', '1430', '1530', '1615', '1720B',
                '1830', '2020A', '2030', '2100', '2120B']
    h2z_time_weekend = ['0830', '1630']
    f2z_time = ['0700', '0730', '0900', '1215', '1330', '1630', '1900']
    z2f_time = ['0750', '1215', '1500', '1700', '1900']
    j2h_time = ['0710', '0720', '0730', '0740', '0750', '0800', '0815', '0830', '0845', '0900B', '0915', '0930', '1000',
                '1030', '1110', '1140', '1200', '1215', '1230', '1240', '1300', '1330', '1400', '1500B', '1515', '1530',
                '1600', '1630', '1655', '1700', '1710', '1730', '1800B', '1900', '2000', '2030', '2100', '2120', '2145',
                '2210']
    j2h_time_weekend = ['0740', '0800', '0820', '0840', '0900', '0920', '0940', '1000', '1020', '1050', '1220', '1730B',
                        '2040', '2120', '2210']
    h2j_time = ['0730', '0740', '0800', '0830B', '0900', '0930', '1000', '1020', '1100', '1130', '1145', '1200', '1230',
                '1300', '1330', '1400', '1430', '1500', '1530', '1600', '1615', '1620', '1630', '1700', '1715', '1725',
                '1735', '1745', '1800', '1830', '2000', '2020', '2030', '2050', '2100', '2120', '2140', '2200', '2215',
                '2230']
    h2j_time_weekend = ['0820', '0840', '0900', '0920', '0940', '1150', '1630', '1700B', '2015', '2100', '2145', '2230']
    f2h_time = ['0710', '0720', '0815', '0915', '1100', '1145', '1215', '1300', '1400', '1430', '1530', '1600', '1655',
                '1710', '1725', '1820', '2020', '2115', '2150']
    f2h_time_weekend = ['0900', '1730']
    h2f_time = ['0655', '0710', '0815', '0915', '1015', '1100', '1230', '1300', '1400', '1530', '1600', '1655', '1710',
                '1800', '1930', '2020B', '2125B']
    h2f_time_weekend = ['0800', '1630']
    h2z_all = z2h_all = "详情可查看：https://mp.weixin.qq.com/s/suzK9K8DB9ZbUJQ9nN2E6A"
    f2z_all = z2f_all = "详情可查看：https://mp.weixin.qq.com/s/suzK9K8DB9ZbUJQ9nN2E6A"
    j2h_all = h2j_all = "详情可查看：https://mp.weixin.qq.com/s/suzK9K8DB9ZbUJQ9nN2E6A"
    f2h_all = h2f_all = "详情可查看：https://mp.weixin.qq.com/s/suzK9K8DB9ZbUJQ9nN2E6A"
    bus_all = "所有校车：https://mp.weixin.qq.com/s/suzK9K8DB9ZbUJQ9nN2E6A"
    notify = '有车'
    bus_time = None
    all = None
    year = int(time.strftime("%Y", time.localtime()))
    month = int(time.strftime("%m", time.localtime()))
    day = int(time.strftime("%d", time.localtime()))
    if start == 'z' and end == 'h' and not isWeekend(year, month, day):
        bus_time = z2h_time
        all = z2h_all
    if start == 'z' and end == 'h' and isWeekend(year, month, day):
        bus_time = z2h_time_weekend
        all = bus_all
    if start == 'h' and end == 'z' and not isWeekend(year, month, day):
        bus_time = h2z_time
        all = h2z_all
    if start == 'h' and end == 'z' and isWeekend(year, month, day):
        bus_time = h2z_time_weekend
        all = bus_all
    if start == 'f' and end == 'z' and not isWeekend(year, month, day):
        bus_time = f2z_time
        all = f2z_all
    if start == 'z' and end == 'f' and not isWeekend(year, month, day):
        bus_time = z2f_time
        all = z2f_all
    if start == 'f' and end == 'z' and isWeekend(year, month, day):
        return '该方向双休日没车', None, None, bus_all
    if start == 'z' and end == 'f' and isWeekend(year, month, day):
        return '该方向双休日没车', None, None, bus_all
    if start == 'j' and end == 'h' and not isWeekend(year, month, day):
        bus_time = j2h_time
        all = j2h_all
    if start == 'j' and end == 'h' and isWeekend(year, month, day):
        bus_time = j2h_time_weekend
        all = bus_all
    if start == 'h' and end == 'j' and not isWeekend(year, month, day):
        bus_time = h2j_time
        all = h2j_all
    if start == 'h' and end == 'j' and isWeekend(year, month, day):
        bus_time = h2j_time_weekend
        all = bus_all
    if start == 'f' and end == 'h' and not isWeekend(year, month, day):
        bus_time = f2h_time
        all = f2h_all
    if start == 'f' and end == 'h' and isWeekend(year, month, day):
        bus_time = f2h_time_weekend
        all = bus_all
    if start == 'h' and end == 'f' and not isWeekend(year, month, day):
        bus_time = h2f_time
        all = h2f_all
    if start == 'h' and end == 'f' and isWeekend(year, month, day):
        bus_time = h2f_time_weekend
        all = bus_all

    now = int(time.strftime("%H%M", time.localtime()))
    next_bus_count = None
    next_next_bus_count = None
    nextBus = None
    nextNextBus = bus_time[-1]
    if len(nextNextBus) == 5:
        if nextNextBus[4] == 'A':
            next_next_bus_count = '三辆'
        if nextNextBus[4] == 'B':
            next_next_bus_count = '两辆'
    else:
        next_next_bus_count = '一辆'
    for i in bus_time:
        if len(i) == 5:
            if i[4] == 'A':
                next_bus_count = '三辆'
            if i[4] == 'B':
                next_bus_count = '两辆'
            i = i[0:4]
        else:
            next_bus_count = '一辆'
        if (int(i) > now):
            nextBus = i
            break
    if (nextBus == None):
        notify = '没车'
        nextBus = '最后一班（{}）：'.format(next_next_bus_count) + str(int(nextNextBus[0:2])) + ':' + nextNextBus[2:4]
        nextNextBus = '最后一班（{}）：'.format(next_next_bus_count) + str(int(nextNextBus[0:2])) + ':' + nextNextBus[2:4]
    else:
        temp = nextBus
        if next_bus_count == '三辆':
            temp += 'A'
        if next_bus_count == '两辆':
            temp += 'B'
        if next_bus_count == '一辆':
            pass
        if temp == bus_time[-1]:
            nextBus = '下一班（{}）：'.format(next_bus_count) + str(int(nextBus[0:2])) + ':' + nextBus[2:4]
            nextNextBus = '下下一班没了，最后一班（{}）：'.format(next_next_bus_count) + str(
                int(nextNextBus[0:2])) + ':' + nextNextBus[2:4]
        else:
            temp = nextBus
            if next_bus_count == '三辆':
                temp += 'A'
            if next_bus_count == '两辆':
                temp += 'B'
            if next_bus_count == '一辆':
                pass
            index = bus_time.index(temp) + 1
            nextNextBus = bus_time[index]
            if len(nextNextBus) == 5:
                if nextNextBus[4] == 'A':
                    next_next_bus_count = '三辆'
                if nextNextBus[4] == 'B':
                    next_next_bus_count = '两辆'
            else:
                next_next_bus_count = '一辆'
            nextBus = '下一班（{}）：'.format(next_bus_count) + str(int(nextBus[0:2])) + ':' + nextBus[2:4]
            nextNextBus = '下下一班（{}）：'.format(next_next_bus_count) + str(int(nextNextBus[0:2])) + ':' + nextNextBus[2:4]
    return notify, nextBus, nextNextBus, all


@itchat.msg_register([TEXT])
def msg_receive(msg):
    """
    :param msg:
    :return:
    """
    if re.match(u'.*校车.*', msg['Content']):
        msg.user.send('想查询最近一班校车？请回复help进行查询。')
    if msg['Content'] == 'help':
        help = ('z：张江校区' + '\n' +
                'h：邯郸校区' + '\n' +
                'f：枫林校区' + '\n' +
                'j：江湾校区' + '\n' + '例如：查询张江到邯郸的最近一班校车，则回复：zh；查询所有班次，则回复：all' + '\n')
        msg.user.send(help)
    if msg['Content'] == 'all':
        msg.user.send("所有校车班次：https://mp.weixin.qq.com/s/suzK9K8DB9ZbUJQ9nN2E6A")
    if msg['Content'] in ['zh', 'hz', 'fz', 'zf', 'jh', 'hj', 'fh', 'hf']:
        start = msg['Content'][0]
        end = msg['Content'][1]
        notify, nextBus, nextNextBus, all = searchRecentBus(start, end)
        msg.user.send(notify + '\n' + nextBus + '\n' + nextNextBus + '\n' + all)
    if msg['Content'] in ['zj', 'jz', 'fj', 'jf']:
        msg.user.send('该路线暂未安排校车。')
    if msg['Content'] == '值日':
        now = datetime.datetime.now().strftime('%Y-%m-%d')
        dupy_people = on_duty()
        if dupy_people == "":
            msg.user.send('Error.')
        else:
            info = "今天是{}，值日人为：【{}】，麻烦打扫卫生间和客厅，辛苦啦❤️".format(now, dupy_people)
            msg.user.send(info)


def on_duty():
    now = datetime.datetime.now()
    dist = ((now - start_date).days) % 35
    for k, v in duty_dict.items():
        if start_date + dist * day in v:
            print(k)
            return k
    return ""


def test():
    now = datetime.datetime.now()
    now = datetime.datetime(2020, 10, 31, 10, 00, 59)
    for i in range(-20, 70):
        dt = now + day * i
        print(dt)
        dist = ((dt - start_date).days) % 35
        for k, v in duty_dict.items():
            if start_date + dist * day in v:
                print(k)


group_user_name = None


def send_duty():
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    dupy_people = on_duty()
    info = None
    if dupy_people == "":
        info = "Error."
    else:
        info = "今天是{}，值日人为：【{}】，麻烦打扫卫生间和客厅，辛苦啦❤️".format(now, dupy_people)
    itchat.send_msg(info, toUserName=group_user_name)


def get_rooms():
    for room in itchat.get_chatrooms(update=True)[0:]:
        UserName = room['UserName']
        NickName = room['NickName']
        # print('UserName:{}'.format(UserName))
        # print('NickName:{}'.format(NickName))
        if NickName == "test":
            global group_user_name
            print(group_user_name)
            group_user_name = UserName
            break
    # BackgroundScheduler: 适合于要求任何在程序后台运行的情况，当希望调度器在应用后台执行时使用。
    scheduler = BackgroundScheduler()
    # 采用非阻塞的方式

    # 采用固定时间间隔（interval）的方式，每隔3秒钟执行一次
    scheduler.add_job(send_duty, 'cron', hour="21", minute="59")
    # 这是一个独立的线程
    scheduler.start()


def main():
    # 阿里云需要hotReload=False
    itchat.auto_login(enableCmdQR=2, picDir='QR.png', hotReload=False)
    get_rooms()
    itchat.run()


if __name__ == '__main__':
    # test()
    main()
