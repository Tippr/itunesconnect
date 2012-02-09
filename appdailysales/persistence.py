import psycopg2

def open_connection(config):
    from_conf = lambda k : config.get("Database", k)
    data = dict([(k, from_conf(k)) for k in ['host', 'db', 'user', 'password']])
    return psycopg2.connect("host=%(host)s dbname=%(db)s user=%(user)s password=%(password)s" % data)

def insert(cursor, table, fields, data, returns=None):
    sql = "insert into " + table + "(" + ", ".join(fields) + ") " + \
            "values(" + ", ".join(["%s"] * len(fields)) + ")"
    if returns:
        sql += ' returning ' + ",".join(returns)
    cursor.execute(sql, [data[f] for f in fields])

def update(cursor, table, fields, data, where=None):
    sql = "update " + table + " set " + \
            ', '.join([ '%(field)s=%(place)s' % dict(field=f, place="%s") for f in fields])
    params = [data[f] for f in fields]
    if where:
        sql += " " + where[0]
        params += where[1]
    cursor.execute(sql, params)
