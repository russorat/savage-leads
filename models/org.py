from google.appengine.ext import ndb

class Org(ndb.Model):
  id = ndb.StringProperty()
  name = ndb.StringProperty()
  members = ndb.StringProperty(repeated=True)
  member_emails = ndb.StringProperty(repeated=True)
