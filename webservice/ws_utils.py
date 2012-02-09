'''
Created on 08/11/2011

'''

import json
from datetime import date

dthandler = lambda obj: obj.isoformat() if isinstance(obj, date) else None
render_json = lambda **args: json.dumps(args, default=dthandler)
render_html = lambda template: lambda **args: web.template.frender(template)(args)

from web.webapi import HTTPError

class BadRequestWithMessage(HTTPError):
    message = "Bad request"
    
    def __init__(self, message=None):
        status = "400 Bad Request"
        headers = {'Content-Type': 'text/html'}
        HTTPError.__init__(self, status, headers, message or self.message)
    
import web
from web.db import DB
from appdailysales.configuration import configure
    
conf = configure()

db = web.database(dbn='postgres',
        host=conf.get("Database", 'host'),
        dburl=conf.get("Database", 'dburl'),
        user=conf.get("Database", 'user'),
        pw=conf.get("Database", 'password'),
        db=conf.get("Database", 'db'))
