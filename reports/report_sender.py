'''
Created on 02/11/2011

@author: usuario
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import StringIO
from reports.report_utils import CSVWriter
from reports.itunes_reports import *
from appdailysales.configuration import configure, configure_reports
import appdailysales.persistence as p


def send_csv_email(to, subject, csv, name, content='This email was sent automatically.\r\n\r\nTippr Team'):
    from appdailysales.smtp import send_email
    send_email(to, subject, content, {name: csv})

def send_iterable_report(reportClass, conn, to):
    out = StringIO.StringIO()
    repo = reportClass(conn, CSVWriter(out))
    
    for r in repo:
        r.write_row()

    send_csv_email(to, repo.subject(), out.getvalue(), repo.attachment_name())

def main():
    config = configure()
    conn = p.open_connection(config)
    
    to = configure_reports()

    itunes_reports = [SalesReport, MTDReport, MonthlyRollupReport]

    for report in itunes_reports:
        send_iterable_report(report, conn, to)

    conn.close()
    
if __name__ == '__main__':
    main()
