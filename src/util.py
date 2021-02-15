def cocoa_date_to_human_date(cocoatime) :
    from datetime import datetime
    unix = datetime(1970, 1, 1)  # UTC
    cocoa = datetime(2001, 1, 1)  # UTC
    delta = cocoa - unix  # timedelta instance
    timestamp = datetime.fromtimestamp(int(cocoatime)) + delta
    value = (timestamp.strftime('%Y-%m-%d %H:%M:%S'))
    return value

def cocoa_date_to_human_date_nano(coredate):
        from time import localtime, strftime
        #2001-01-01 seconds(9) or nanoseconds(18)
        #iOS, OS X applications
        t = int(coredate)
        t1 = str(t)
        nano = t1[9:12]
        t_len = len(str(t))
        if t_len == 9 :
            local = localtime(t + 978307200)
        elif t_len == 18 :
            local = localtime((t / 1000000000) + 978307200)
        time_format= '%Y-%m-%d %H:%M:%S' + '.' + nano
        value = strftime(time_format, local)
        return value

def dictionary_encoding_utf_8(dictionary):
    temp = {k: str(v).encode("utf-8") for k,v in dictionary.items()}
    return temp

def unix_date_to_human_date(unixtime) :
    from datetime import datetime
    ts = int(unixtime)
    value = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return value

def timestamp():
    import datetime
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def log(message):
    log_file = open('log.txt', 'w', -1, 'utf-8')
    message = timestamp() + ' > ' + message
    print(message, file=log_file)

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    import sys
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '#' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def db_exsit() :
    import os
    db = os.getcwd() + '/analyze.db'
    if os.path.isfile(db) == True :
        print("The database file exists. Do you want it to be overwritten?")
        check = str(input("Y / N ? : "))
        if check == "Y" :
            os.remove(db)
            return True
        elif check == "N" :
            return False
        else :
            print("Input Error")