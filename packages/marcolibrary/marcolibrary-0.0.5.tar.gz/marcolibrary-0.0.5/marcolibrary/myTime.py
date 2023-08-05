from datetime import datetime
import time
##print  int(datetime.now().strftime("%s%f"))/1000


def getTime13 ():

    aaa = int(datetime.now().strftime("%s%f"))/1000
##    print aaa
    return aaa

def from13ToData(daConvertire):
    import datetime

    ccc = datetime.datetime.fromtimestamp(daConvertire/1000).strftime('%H:%M:%S')
    return ccc

def getDATE ():
    import datetime
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M")

def getDATE10():
    import datetime
    return datetime.datetime.now().strftime("%s")

def from10toDate(now10):
    import datetime
    return  datetime.datetime.fromtimestamp(float(now10)).strftime("%Y-%m-%d %H:%M")

# import datetime
#
# now = datetime.datetime.now()
#
# print
# print "Current date and time using str method of datetime object:"
# print str(now)
#
# print
# print "Current date and time using instance attributes:"
# print "Current year: %d" % now.year
# print "Current month: %d" % now.month
# print "Current day: %d" % now.day
# print "Current hour: %d" % now.hour
# print "Current minute: %d" % now.minute
# print "Current second: %d" % now.second
# print "Current microsecond: %d" % now.microsecond
#
# print
# print "Current date and time using strftime:"
# print now.strftime("%Y-%m-%d %H:%M")
#
# print
# print "Current date and time using isoformat:"
# print now.isoformat()
