"""
This is an optional file that defined app level settings such as:
- database settings
- session settings
- i18n settings
This file is provided as an example:
"""
import os

# try import private settings
try: from . settings_private import *
except: pass

# Uses the private settings to create the DB URI.
# For a local DB, it would be better to use a MySQL database, to have the same
# set up as in the cloud, but in a pinch, sqlite will do.
# A better yet idea would be to keep in the cloud a "testing" database, kept in
# mysql on the same db server as the production db, and to use that for
# development.  In that way, what you find in databases/sql.log can also give you
# suggestions for the operations you have to do in production to update the
# production database.
TESTING_DB_URI = "sqlite://storage.db"

# This is the URL of MySQL as accessed from Google Appengine
GAE_DB_URI = "google:MySQLdb://ken:slugKen1919!@/notes_db?unix_socket=/cloudsql/kenneth-183-notes-app:us-west2:kenneth-notes-app".format(
    DB_USER="ken",
    DB_NAME="notes_db",
    DB_PASSWORD="slugKen1919!",
    DB_CONNECTION="kenneth-183-notes-app:us-west2:kenneth-notes-app"
)

# db settings
APP_FOLDER = os.path.dirname(__file__)
# DB_FOLDER:    Sets the place where migration files will be created
#               and is the store location for SQLite databases
DB_FOLDER = os.path.join(APP_FOLDER, 'databases')
DB_URI = 'sqlite://storage.db'
DB_POOL_SIZE = 1

# session settings
SESSION_TYPE = 'database'
SESSION_SECRET_KEY = '<my secret key>'
MEMCACHE_CLIENTS = ['127.0.0.1:11211']
REDIS_SERVER = 'localhost:6379'

# single sign on Google (will be used if provided)
OAUTH2GOOGLE_CLIENT_ID = None
OAUTH2GOOGLE_CLIENT_SECRET = None

# single sign on Google (will be used if provided)
OAUTH2FACEBOOK_CLIENT_ID = None
OAUTH2FACEBOOK_CLIENT_SECRET = None

# enable PAM
USE_PAM = False

# enable LDAP
USE_LDAP = False
LDAP_SETTING = {
    'mode': 'ad',
    'server': 'my.domain.controller',
    'base_dn': 'ou=Users,dc=domain,dc=com'}

# i18n settings
T_FOLDER = os.path.join(APP_FOLDER, 'translations')

