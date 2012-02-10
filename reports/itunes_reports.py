'''
Created on 01/11/2011
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from reports.report_utils import IterableDataReport

from datetime import datetime
from datetime import date
from appdailysales.date_utils import subtract_date

UPDATE_TYPE = '7'
INSTALL_TYPE = '1'

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
    
from dateutil.relativedelta import *
from dateutil.rrule import *

def join(s, d=", "):
    return d.join(s)

class MonthlyRollupReport(IterableDataReport):

    @property
    def query(self):
        sql = """
        select developer, title, version, %(grouped_data)s 
        from (select developer, title, version, %(subqueries)s from itunes i) raw_data 
        group by developer, title, version
        """ 
        subqueries = [self._build_selection(name, date, type) for date, name, type in self._dynamic_fields()]
        return sql % {
                'grouped_data': join(['sum("%s") "%s"' % (h[1], h[1]) for h in self._dynamic_fields()]),
                'subqueries'  : join(subqueries)}

    @property
    def headers(self):
        return ['Developer', 'Title', 'Version'] + [f[1] for f in self._dynamic_fields()]

    def subject(self):
        return 'Monthly Rollup Report - %s' % self.today()
    
    def attachment_name(self):
        return 'monthy-rollup-report-%s.csv' % self.today()    

    def _dynamic_fields(self):
        months = list(rrule(MONTHLY, dtstart=date.today() - relativedelta(months=12), count=12))
        months.reverse()
        fields = []
        for month in months:
            name = month.strftime("%b/%Y")
            fields.append((month, name + ' Updates', UPDATE_TYPE))
            fields.append((month, name + ' Installs', INSTALL_TYPE))
        return fields

    def _build_selection(self, name, date, type):
        sql = """(select sum(units) 
        from itunes 
        where id = i.id 
        and type_identifier = '%s'
        and date_trunc('month', begin_date) = date_trunc('month', TIMESTAMP '%s')) \"%s\""""
        return sql % (type, date, name)
