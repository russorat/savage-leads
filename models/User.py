from google.appengine.ext import ndb

class User(ndb.Model):
  id = ndb.StringProperty()
  email = ndb.StringProperty()
