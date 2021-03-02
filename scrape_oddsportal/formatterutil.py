from datetime import datetime, time

def format_time(time_string, source):
    try:
        if (source == 'fs'):
            time_split = time_string.split(":")
            return (time(int(time_split[0]), int(time_split[1]), 0))
        elif (source == 'op'):
            time_split = time_string.split(":")
            return (time(int(time_split[0]), int(time_split[1]), 0))
        elif (source == 'fts'):
            try:
                return (datetime.utcfromtimestamp(int(time_string)).strftime('%H:%M:%S'))
            except:
                return (0)
    except Exception:
        return (datetime.now().strftime("%H:%M:%S"))

def format_date(date_string, source):
    try:
        if (source == 'fs'):
            return (datetime.strptime(date_string,'%d %b %Y').date())
        elif (source == 'op'):
            return (datetime.strptime(date_string,'%d %b %Y').date())
        elif (source == 'fts'):
            try:
                return (datetime.utcfromtimestamp(int(date_string)).strftime('%Y-%m-%d'))
            except:
                return (0)
    except Exception:
        return (datetime.today().date()) ## done like this since we have already imported datetime module from datatime package
