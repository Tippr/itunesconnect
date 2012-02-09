from datetime import date, timedelta

def get_week_days(year, week):
    d = date(year, 1, 1)
    if d.weekday() > 3:
        d = d+timedelta(7 - d.weekday())
    else:
        d = d - timedelta(d.weekday())
    dlt = timedelta(days = (week - 1) * 7)
    return d + dlt,  d + dlt + timedelta(days=6)

def current_start_date(freq, today = date.today()):
    if freq == 'week':
        return get_week_days(today.year, today.isocalendar()[1])[0]
    elif freq == 'month':
        return date(today.year, today.month, 1)
    elif freq == 'year':
        return date(today.year, 1, 1)
    else:
        return None

def current_daily(freq, from_date, to_date, today = date.today()):
    current_freq_start_date = current_start_date(freq, today)
    if current_freq_start_date and from_date <= current_freq_start_date <= to_date:
        return (max(current_freq_start_date, from_date), to_date)
    return (None, None)

def format_date(d):
    from time import mktime, strptime
    if len(d) == 15:
        ret= date.fromtimestamp(mktime(strptime(d, "%Y%m%dT%H:%MZ")))
    else:
        ret= d[:14] + 'Z'
    return ret
        
def format_dates(from_date, to_date):
    return (format_date(from_date), format_date(to_date))

def date_to_iso8601(dt):
    return dt.strftime('%Y%m%dT%H:%MZ') if dt else None




def subtract_date(date, year=0, month=0):
    year, month = divmod(year*12 + month, 12)
    if date.month <= month:
        year = date.year - year - 1
        month = date.month - month + 12
    else:
        year = date.year - year
        month = date.month - month
    return date.replace(year = year, month = month)


