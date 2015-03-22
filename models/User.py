from elasticsearch import Elasticsearch

class User(object):
  es = Elasticsearch()

  def __init__(self):
    self._id = None
    self._email = None

  def is_authenticated(self):
    return True

  def is_active(self):
    return True

  def is_anonymous(self):
    return False

  def get_id(self):
    return self.id

  @property
  def id(self):
    return self._id

  @id.setter
  def id(self,val):
    self._id = val

  @property
  def email(self):
    return self._email

  @email.setter
  def email(self,val):
    self._email = val

  def __repr__(self):
      return '<User %r>' % (self.email)

  def save(self):
    if self.id :
      self.es.update(index='users',
        doc_type='users',
        id=self.id,
        body='{ "doc" : { "email": "%s" } }'%self.email
      )
    else :
      results = self.es.create(index='users',
        doc_type='users',
        body='{ "email": "%s" }'%self.email
      )
      if results['created']:
        self.id = results['_id']
      else:
        raise 'Failed to create new user.'

  def delete(self):
    self.es.delete(index='users',
      doc_type='users',
      id=self.id
    )
    self.id=None

  @staticmethod
  def query_all():
    results = User.es.search(
      index='users',
      doc_type='users',
      size=10000
    )
    retVal = []
    if results and results['hits']['total'] > 0 :
      hits = results['hits']['hits']
      for hit in hits:
        retVal.append(User.from_es_hit(hit))
    return retVal

  @staticmethod
  def get(user_id):
    results = User.es.get(
      index='users',
      doc_type='users',
      id=user_id
    )
    if results :
      return User.from_es_hit(results)
    return None

  @staticmethod
  def get_from_email(the_email):
    results = User.es.search(
      index='users',
      doc_type='users',
      q='email:"%s"'%the_email
    )
    if results and results['hits']['total'] > 0 :
      return User.from_es_hit(results['hits']['hits'][0])
    return None

  @staticmethod
  def from_es_hit(hit):
    user = User()
    user.id = hit['_id']
    user.email = hit['_source']['email']
    return user
