import datetime
import time
from dateutil import tz
import dateutil.parser

class DatetimePlus(object):
    #取一个日期时间的时间部分
    @staticmethod
    def get_datetime_only_time(dt):
        dtstr = DatetimePlus.datetime_to_str(dt)[11:]
        result = DatetimePlus.timestr_to_datetime(dtstr)
        return result

    #取一个日期时间的日期部分
    @staticmethod
    def get_datetime_only_date(dt):
        dtstr = DatetimePlus.datetime_to_str(dt)[:10]
        result = DatetimePlus.datestr_to_datetime(dtstr)
        return result

    #字符串格式化成时间
    @classmethod
    def str_to_datetime(cls, datetimeStr):
        result = datetime.datetime.strptime(datetimeStr, '%Y-%m-%d %H:%M:%S')
        return result

    #字符串格式化成时间
    @classmethod
    def timestr_to_datetime(cls, datetimeStr):
        result = datetime.datetime.strptime(datetimeStr, '%H:%M:%S')
        return result

    #字符串格式化成时间
    @classmethod
    def datestr_to_datetime(cls, datetimeStr):
        result = datetime.datetime.strptime(datetimeStr, '%Y-%m-%d')
        return result

    #取当前时间格式化成字符串用作SQL
    @classmethod
    def get_nowdatetime_to_str(cls):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    #时间格式化成字符串可以用作SQL
    @classmethod
    def datetime_to_str(cls, timeValue):
        return timeValue.strftime('%Y-%m-%d %H:%M:%S')

    #取当前日期并格式化
    @classmethod
    def get_nowdate_to_str(cls):
        result = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        return result

    #获取当前时间的时间部分字符串
    @staticmethod
    def get_now_only_time_to_str():
        result = time.strftime('%H:%M:%S', time.localtime(time.time()))
        return result

    #取当前时间格式化为文件名使用
    @classmethod
    def get_now_datetime_to_filename(cls):
        result = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        return result

    #取当前时间格式化为文件名使用 到微秒
    @classmethod
    def get_now_datetime_to_filename_s(cls):
        result = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')
        return result

    #取当前时间格式化为文件夹使用 只要月
    @classmethod
    def get_now_datetime_to_filename_month(cls):
        result = datetime.datetime.now().strftime('%Y_%m')
        return result

    #加秒
    @classmethod
    def add_seconds(cls, sourceTime, second):
        curTime = datetime.timedelta(seconds=second)
        result = sourceTime + curTime
        return result

    #加分
    @classmethod
    def add_minutes(cls, sourceTime, minutes):
        curTime = datetime.timedelta(minutes=minutes)
        result = sourceTime + curTime
        return result

    #加天
    @classmethod
    def add_days(cls, sourceTime, days):
        curTime = datetime.timedelta(days=days)
        result = sourceTime + curTime
        return result

    #加小时
    @classmethod
    def add_hours(cls, sourceTime, hours):
        curTime = datetime.timedelta(hours=hours)
        result = sourceTime + curTime
        return result
    #加周
    @classmethod
    def add_weeks(cls, sourceTime, weeks):
        curTime = datetime.timedelta(weeks=weeks)
        result = sourceTime + curTime
        return result

    #取当前时间
    @classmethod
    def get_now_datetime(cls):
        return datetime.datetime.now()

    #获取两个时间相差的秒数
    @classmethod
    def get_diff_seconds(cls, t1, t2):
        if t1 > t2:
            result = (t1 - t2).seconds
        else:
            result = -(t2 - t1).seconds
        return result

    #获取两个时间相差的天
    @classmethod
    def get_diff_days(cls, t1, t2):
        if t1 > t2:
            result = (t1 - t2).days
        else:
            result = -(t2 - t1).days
        return result

    # 获取两个时间相差的分
    @classmethod
    def get_diff_minutes(cls, t1, t2):
        if t1 > t2:
            result = int((t1 - t2).seconds / 60)
        else:
            result = -int((t2 - t1).seconds / 60)
        return result

    #获取两个时间相差的年
    @classmethod
    def get_diff_yeas(cls, t1, t2):
        if t1 > t2:
            result = int((t1 - t2).days / 365)
        else:
            result = -int((t2 - t1).days / 365)
        return result

    @staticmethod
    def get_month_firstday_and_lastday(year=None, month=None):
        """
        :param year: 年份，默认是本年，可传int或str类型
        :param month: 月份，默认是本月，可传int或str类型
        :return: firstDay: 当月的第一天，datetime.date类型
                  lastDay: 当月的最后一天，datetime.date类型
        """
        if year:
            year = int(year)
        else:
            year = datetime.date.today().year

        if month:
            month = int(month)
        else:
            month = datetime.date.today().month

        import calendar
        # 获取当月第一天的星期和当月的总天数
        firstDayWeekDay, monthRange = calendar.monthrange(year, month)
        # 获取当月的第一天
        firstDay = datetime.date(year=year, month=month, day=1)
        lastDay = datetime.date(year=year, month=month, day=monthRange)
        return firstDay, lastDay

    #毫秒时间戳
    @staticmethod
    def get_time_stamp_millisecond():
        return int(round(time.time() * 1000))

    # 秒时间戳
    @staticmethod
    def get_time_stamp_second():
        return int(time.time())

    @staticmethod
    def time_stamp_to_datetime(timestamp):
        if isinstance(timestamp,(str)):
            s_len = len(timestamp)
            timestamp = int(timestamp)
        else:
            s_len = len(str(timestamp))
        if s_len == 10:
            timestamp = timestamp
        elif s_len == 13:
            timestamp = int(str(timestamp)[:-3])
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))
        return DatetimePlus.str_to_datetime(time_str)

    #UTC 字符串时间转换为中国时间
    @staticmethod
    def utc_str_to_datetime(utc_str):
        _time = dateutil.parser.parse(utc_str)

        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('PRC')  # CST
        _time.replace(tzinfo=from_zone)
        local = _time.astimezone(to_zone)
        return local

    # UTC 字符串时间转换为中国时间
    @staticmethod
    def utc_str_to_datetime_str(utc_str):
        _local = DatetimePlus.utc_str_to_datetime(utc_str)
        result = DatetimePlus.datetime_to_str(_local)
        return result

    @staticmethod
    def utc_to_datetime(utc):
        to_zone = tz.gettz('PRC')
        local = utc.astimezone(to_zone)
        return local

    #UTC时间转换为当前时区时间并去掉时区标志
    @staticmethod
    def utc_to_local(dt):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('PRC')  # CST
        dt.replace(tzinfo=from_zone)
        dt = dt.astimezone(to_zone)
        dt = dt.replace(tzinfo=None)
        return dt

    #当前时区时间转换为UTC时间
    @staticmethod
    def local_to_utc(dt):
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('PRC')  # CST
        dt.replace(tzinfo=to_zone)
        dt = dt.astimezone(from_zone)
        return dt

    @staticmethod
    def millisecond_timestamp_to_datetime(timestamp):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp / 1000)))

    @staticmethod
    def timestamp_to_datetime(timestamp):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

    # 把datetime转成字符串
    @staticmethod
    def datetime_toString(dt):
        return dt.strftime("%Y-%m-%d-%H")

    # 把字符串转成datetime
    @staticmethod
    def string_toDatetime(string):
        return datetime.strptime(string, "%Y-%m-%d-%H")

    #把字符串转成时间戳形式
    @staticmethod
    def string_toTimestamp(strTime):
        return time.mktime(DatetimePlus.string_toDatetime(strTime).timetuple())

    #把时间戳转成字符串形式
    @staticmethod
    def timestamp_toString(stamp):
        return time.strftime("%Y-%m-%d-%H", time.localtime(stamp))

    #把datetime类型转外时间戳形式
    @staticmethod
    def datetime_toTimestamp(dateTim):
        return time.mktime(dateTim.timetuple())

    @staticmethod
    def get_diff_secends_by_datetime_subtime(s_dt_time = datetime.datetime.now().time(),d_dt_time = datetime.datetime.now().time()):
        sum = s_dt_time.second + s_dt_time.minute * 60 + s_dt_time.hour * 3600
        d_sum = d_dt_time.second + d_dt_time.minute * 60 + d_dt_time.hour * 3600
        return sum - d_sum


if __name__ == '__main__':
    print(DatetimePlus.get_now_only_time_to_str())
    t1 = datetime.datetime.now()
    t2 = DatetimePlus.add_seconds(t1, -70)

    print('diffMinutes', DatetimePlus.get_diff_minutes(t1, t2))
    print('diffSeconds', DatetimePlus.get_diff_seconds(t1, t2))
    print('diffMinutes', DatetimePlus.get_diff_minutes(t2, t1))
    print('diffSeconds', DatetimePlus.get_diff_seconds(t2, t1))
    print('t1,t2',t1, t2)
    t2 = DatetimePlus.add_weeks(t1, -70)
    print('t1,t2',t1,t2)
    print('diffYears', DatetimePlus.get_diff_yeas(t1, t2))
    print('diffDays', DatetimePlus.get_diff_days(t1, t2))
    print('diffYears', DatetimePlus.get_diff_yeas(t2, t1))
    print('diffDays', DatetimePlus.get_diff_days(t2, t1))
    print('now',t1)
    print('add day', DatetimePlus.add_days(t1, 1))
    print('add week', DatetimePlus.add_weeks(t1, 1))
    print('add hour', DatetimePlus.add_hours(t1, 1))
    print('add minutes', DatetimePlus.add_minutes(t1, 1))
    print(DatetimePlus.timestr_to_datetime('21:23:59'))
    print(DatetimePlus.datestr_to_datetime('2019-08-03'))

    first,last = DatetimePlus.get_month_firstday_and_lastday(2017, 9)
    print(DatetimePlus.datetime_to_str(first))
    print(DatetimePlus.datetime_to_str(last))
    print('================')
    print((t1))
    print(DatetimePlus.get_datetime_only_date(t1))
    print(DatetimePlus.get_datetime_only_time(t1))