#@PydevCodeAnalysisIgnore
import web 
import re
from datetime import datetime
from appdailysales.configuration import configure_security
    
conf = configure_security()

db = web.database(dbn='postgres',
        host=conf.get("Security", 'dbhost'),
        dburl=conf.get("Security", 'dburl'),
        user=conf.get("Security", 'dbuser'),
        pw=conf.get("Security", 'dbpassword'),
        db=conf.get("Security", 'db'))

VALID_KEY = re.compile('[a-zA-Z0-9_-]{1,255}')

def is_valid_key(key):
    if key and VALID_KEY.match(key) is not None:
        return True
    return False

def exist_key(key):
    r = db.select(tables=['keys'], where='key = $key', vars=dict(key=key))
    return len(r) > 0

def validate_key(fn):
    def new(*args):
        uri = web.ctx.env.get('REQUEST_URI')
        key = web.ctx.env.get('HTTP_X_API_KEY')
        log = lambda status: db.insert('access_log', description=uri, date=datetime.now(), key=key, status=status)
        if not is_valid_key(key):
            log('invalid key')
            web.badrequest()
        elif exist_key(key):
            log('access')
            return fn(*args)
        else:
            log('key not found')
            web.forbidden()
    return new

