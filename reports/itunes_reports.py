'''
Created on 01/11/2011
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from reports.report_utils import IterableDataReport

from datetime import datetime
from appdailysales.date_utils import subtract_date

class SalesReport(IterableDataReport):
    headers = ['Date', 'Developer', 'Title', 'Version', 'Downloads', 'Updates']
    
    query = '''
        select begin_date,
            developer,
            title,    
            version,
            (select sum(units) from itunes it2 where it2.type_identifier = '1' and it1.developer = it2.developer and it1.title = it2.title and it1.begin_date=it2.begin_date) as downloads,
            (select sum(units) from itunes it2 where it2.type_identifier = '7' and it1.developer = it2.developer and it1.title = it2.title and it1.begin_date=it2.begin_date) as updates
        from itunes it1
         where begin_date < now() 
        group by it1.begin_date, it1.developer, it1.title, it1.version
        order by developer, title, begin_date
    '''

    def subject(self):
        return 'iTunes Connect Sales Report - %s' % self.today()
    
    def attachment_name(self):
        return 'sales-report-%s.csv' % self.today()
    

class MTDReport(IterableDataReport):
    headers = ['Developer', 'Title', 'Version', 'Last Month Downloads', 'MTD Downloads', ' Last Month Updates', 'Updates']
    
    query = '''
        select 
            developer, 
            title, 
            version, 
            mtd_downloads(title, version, extract(month from (now() - interval '1 month'))::integer, extract(year from (now() - interval '1 month'))::integer) as LastMonthDowmloads,
            mtd_downloads(title, version, extract(month from now())::integer, extract(year from now())::integer) as MTDDowmloads,
            mtd_updates(title, version, extract(month from (now() - interval '1 month'))::integer, extract(year from (now() - interval '1 month'))::integer) as LastMonthUpdates,
            mtd_updates(title, version, extract(month from now())::integer, extract(year from now())::integer) as MTDUpdates
        from itunes
        WHERE
            extract(month from begin_date) = extract(month from now())
        group by
            developer, title, version
        order by
            developer, title, version
    '''

    def subject(self):
        return 'iTunes Connect MTD Report - %s' % self.today()
    
    def attachment_name(self):
        return 'mtd-report-%s.csv' % self.today()
    
class MonthlyRollupReport(IterableDataReport):
    
    currentMonth = datetime.now().month
    currentYear = datetime.year
    
    headers = ['Developer', 'Title', 'Version']
    
    for i in range(12):
        my_header = str(subtract_date(datetime.today(), month=1).year) + '/' +str(subtract_date(datetime.today(), month=1).month) 
        headers.append(my_header + ' Downloads')
        headers.append(my_header + ' Updates')
        
        
    query = '''
        select 
            developer, 
            title, 
            version, 
            mtd_downloads(title, version, extract(month from now())::integer, extract(year from now())::integer) as MTDDowmloads,
            mtd_updates(title, version, extract(month from now())::integer, extract(year from now())::integer) as MTDUpdates
    '''
    
    
    for i in range(12):
        if i > 0:
            my_query = ''' 
             ,mtd_downloads(title, version, extract(month from (now() - interval '1 month'))::integer, extract(year from (now() - interval '1 month'))::integer) as 
            '''
            my_query += my_header[i+5]
            query += my_query
            
            
    query += '''
         from itunes
        WHERE
            extract(month from begin_date) = extract(month from now())
        group by
            developer, title, version
        order by
            developer, title, version    
     '''       
                
    def subject(self):
        return 'iTunes Connect MTD Report - %s' % self.today()
    
    def attachment_name(self):
        return 'mtd-report-%s.csv' % self.today()    

UPDATE_TYPE = 7
INSTALL_TYPE = 1

from datetime import date
from dateutil.relativedelta import *
from dateutil.rrule import *

class LastMonthsReport(IterableDataReport):
    @property
    def query(self):
        query = 'select developer, title, version, %s from itunes i'
        subqueries = []
        for date in self.months():
            name = date.strftime("%b/%Y")
            subqueries.append(self._build_selection(name + ' Updates', date, UPDATE_TYPE))
            subqueries.append(self._build_selection(name + ' Installs', date, INSTALL_TYPE))
        sql = query % ", ".join(subqueries)
        return sql

    @property
    def headers(self):
        header = ['Developer', 'Title', 'Version'] 
        for month in self.months():
            name = month.strftime("%b/%Y")
            header.append(name + ' Updates')
            header.append(name + ' Installs')
        return header

    def months(self):
        return rrule(MONTHLY, dtstart=date.today() - relativedelta(months=12), count=12)

    def subject(self):
        return 'Last Months Report - %s' % self.today()
    
    def attachment_name(self):
        return 'lastmonths-report-%s.csv' % self.today()    

    def _build_selection(self, name, date, type):
        sql = """(select sum(units) 
        from itunes 
        where id = i.id 
        and type_identifier = '%s'
        and date_trunc('month', begin_date) = date_trunc('month', TIMESTAMP '%s')) \"%s\""""
        return sql % (type, date, name)

