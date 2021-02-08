def cocoa_date_to_human_date(cocoatime) :
    cocoatime = int(cocoatime)
    from datetime import datetime

    unix = datetime(1970, 1, 1)  # UTC
    cocoa = datetime(2001, 1, 1)  # UTC

    delta = cocoa - unix  # timedelta instance

    timestamp = datetime.fromtimestamp(cocoatime) + delta

    value = (timestamp.strftime('%Y-%m-%d %H:%M:%S'))

    return value

def dictionary_encoding_utf_8(dictionary):
    temp = {k: str(v).encode("utf-8") for k,v in dictionary.items()}
    return temp