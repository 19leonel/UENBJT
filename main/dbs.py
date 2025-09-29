from urllib.parse import urlparse, parse_qsl
from dotenv import load_dotenv
import os
import dj_database_url

db={}
load_dotenv()

# Replace the DATABASES section of your settings.py with this
tmpPostgres = urlparse(os.getenv("DATABASE_URL"))
def dbPostgreSQL():
    db = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': tmpPostgres.path.replace('/', ''),
        'USER': tmpPostgres.username,
        'PASSWORD': tmpPostgres.password,
        'HOST': tmpPostgres.hostname,
        'PORT': 5432,
        'OPTIONS': dict(parse_qsl(tmpPostgres.query)),
    }
    return db

def db1(dir):
    d = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(dir, 'db.sqlite3'),
    }
    return d
