import os
import ConfigParser
    
CONFIG_FILE = os.path.join(os.getenv("HOME"), '.itunesconnect.cfg')

def configure():
    config = ConfigParser.ConfigParser()
    config.add_section("Database")
    config.set("Database", 'host', 'localhost')
    config.set("Database", 'dburl', 'localhost')
    config.set("Database", 'db', 'email_statistics')
    config.set("Database", 'user', 'postgres')
    config.set("Database", 'password', '')
    if os.path.exists(CONFIG_FILE):
        config.readfp(open(CONFIG_FILE))
    return config

def configure_security():
    config = ConfigParser.ConfigParser()
    config.add_section("Security")
    config.set("Security", 'dbhost', 'localhost')
    config.set("Security", 'dburl', 'localhost')
    config.set("Security", 'db', 'security')
    config.set("Security", 'dbuser', 'postgres')
    config.set("Security", 'dbpassword', '')
    if os.path.exists(CONFIG_FILE):
        config.readfp(open(CONFIG_FILE))
    return config


def configure_itunes():
    config = ConfigParser.ConfigParser()
    config.add_section("iTunes")
    config.set("iTunes", 'user', 'ios-stats@tippr.com')
    config.set("iTunes", 'password', 'Tippr2011')
    

def configure_reports():
    cfg = ConfigParser.ConfigParser()
    cfg.readfp(open(CONFIG_FILE))
    
    to = cfg.get("Reports", "to").split(",")
    return (to)

def smtp_config():
    cfg = ConfigParser.ConfigParser()
    cfg.readfp(open(CONFIG_FILE))
    
    smtp = cfg.get("Smtp", "smtp")
    usr = cfg.get("Smtp", "username")
    pwd = cfg.get("Smtp", "password")
    fromEmail = cfg.get("Smtp", "from")
    
    return (smtp, usr, pwd, fromEmail)

def configure_log():
    smtp, usr, pwd, fromEmail = smtp_config()
    
    cfg = ConfigParser.ConfigParser()
    cfg.readfp(open(CONFIG_FILE))
    toEmail = cfg.get("Logging", "to")
    file = cfg.get("Logging", "file")
    
    '''
    mailHandler = logging.handlers.SMTPHandler(mailhost=smtp, fromaddr=fromEmail,
                                               toaddrs=toEmail, subject='Email Statistic - Error log',
                                               credentials=(usr, pwd), secure=tuple())
    mailHandler.setLevel(logging.ERROR)
    mailHandler.setFormatter(fmt)
    log.addHandler(mailHandler)
    '''
    
