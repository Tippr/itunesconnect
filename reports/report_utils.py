import csv
import datetime
from psycopg2.extras import DictCursor

class IterableDataReport(object):
    def __init__(self, connection, output):
        self.connection = connection
        self.output = output
    
    def __iter__(self):
        self.cursor = self.connection.cursor(cursor_factory=DictCursor)
        self.output.write_row(self.headers)
        self.cursor.execute(self.query)
        return self
    
    def write_row(self):
        self.output.write_row(self.row)
        
    def next(self):
        self.row = self.cursor.fetchone()
        if self.row:
            return self
        else:
            raise StopIteration()

    def today(self):
        return str(datetime.date.today())
        
class CSVWriter(object):
    def __init__(self, output):
        self.output = output
        self.writer = csv.writer(self.output)
        
    def write_row(self, row):
        self.writer.writerow(row)
