import sys
import os.path

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import web
app = web.application([], globals())

from sales import *


for url, handler in sales_mappings.iteritems():
    app.add_mapping(url, handler)
    
    
app.add_mapping('/doc/(.*)', 'static')

class static:
    def GET(self, file):

        root = os.path.dirname(os.path.dirname(__file__)) + '/doc/_build/html/'
        
        try:
            f = open(root + file, 'r')
            return f.read()
        except:
            return web.NotFound()    
    
    

if __name__ == "__main__":
    app.run()
