import web
from appdailysales.date_utils import date_to_iso8601
from ws_utils import render_json, db
from mimerender import mimerender
from security import validate_key
from decimal import *

sales_mappings = {
    '/stats/(.+)/apps': 'PublisherApps',
    '/stats/(.+)/apps/(.+)': 'AppStats'
}

def exists_publisher(pub):
    if pub:
        r = db.query('select count(1) as total from itunes where publisher_name = $pub', vars=dict(pub=pub))
        return r[0].total > 0
    else:
        return False
    
    
    

def exists_appid(appid):
    if appid:
        r = db.query('select count(1) as total from itunes where title = $appid', vars=dict(appid=appid))
        return r[0].total > 0
    else:
        return False
    
def defaultint(ix):
    if not ix:
        return 0
    return int(ix)        
        
    
def build_app_data(r):
    return {
        'date'      : date_to_iso8601(r.begin_date),
        'developer' : r.developer,
        'title'     : r.title,
        'version'   : r.version,
        'downloads' : defaultint(r.downloads),
        'updates'   : defaultint(r.updates),
        'publisher' : r.publisher_name
    }


class PublisherApps(object):
    '''
    Class for rendering templates.

    Usage example::

        >>> t = Template('somefile')
        >>> document = t.render(variables={'ID': 1234})

    Rendered document is always returned as a unicode string.
    '''
    
    
    @mimerender(
        default='json', 
        json=render_json
    )
    @validate_key
    
    
    def GET(self, pub):
        
        def get_date_params():
            params = web.input()
            start_date = params.get('start-date')
            end_date = params.get('end-date') 
        
            if start_date and end_date:
                return start_date, end_date
            else:
                return None, None
        
                        
        if exists_publisher(pub):
            
            start_date, end_date = get_date_params()
            
            if start_date and end_date:
                vars = {'pub': pub, 'start_date': start_date, 'end_date': end_date} 
                
                
                rs = db.query('''select begin_date,
                            developer,
                            title,    
                            version,
                            publisher_name,
                            (select sum(units) from itunes it2 where it2.type_identifier = '1' and it1.developer = it2.developer and it1.title = it2.title and it1.begin_date=it2.begin_date) as downloads,
                            (select sum(units) from itunes it2 where it2.type_identifier = '7' and it1.developer = it2.developer and it1.title = it2.title and it1.begin_date=it2.begin_date) as updates
                        from itunes it1
                     where publisher_name=$pub and begin_date>=$start_date and end_date<=$end_date
                    group by it1.begin_date, it1.developer, it1.title, it1.version, it1.publisher_name''', vars)
                
                
            return dict(appstats=[build_app_data(r) for r in rs])
            
        else:
            raise web.NotFound('Invalid publisher name')
        
        
        
        
        
        
class AppStats(object):
    @mimerender(
        default='json', 
        json=render_json
    )
    @validate_key
    def GET(self, pub, app_id=None):
        
        if exists_publisher(pub):
            
            if exists_appid(app_id):
                vars = {'pub': pub, 'app_id': app_id} 
                    
                rs = db.query('''select begin_date,
                        developer,
                        title,    
                        version,
                        publisher_name,
                        (select sum(units) from itunes it2 where it2.type_identifier = '1' and it1.developer = it2.developer and it1.title = it2.title and it1.begin_date=it2.begin_date) as downloads,
                        (select sum(units) from itunes it2 where it2.type_identifier = '7' and it1.developer = it2.developer and it1.title = it2.title and it1.begin_date=it2.begin_date) as updates
                    from itunes it1
                 where publisher_name=$pub and begin_date < now() and title = $app_id
                group by it1.begin_date, it1.developer, it1.title, it1.version, it1.publisher_name''', vars)
                
                return dict(appstats=[build_app_data(r) for r in rs])
            
            else:
                raise web.NotFound('Invalid App Id')  
            
        else:
            raise web.NotFound('Invalid publisher name')        
        

