from elasticsearch import Elasticsearch
import config

class User(object):
  es = Elasticsearch(config.ES_HOSTS)

  def __init__(self):
    self._id = None
    self._email = None
    self._fields = ['email','first_name','last_name']
    self._deleted_fields = []

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

  @property
  def fields(self):
    self._fields.sort()
    return self._fields

  @fields.setter
  def fields(self,new_fields):
    self._fields = new_fields

  def add_field(self,new_field):
    self._fields += new_field

  @property
  def deleted_fields(self):
    self._deleted_fields.sort()
    return self._deleted_fields

  @deleted_fields.setter
  def deleted_fields(self,deleted_fields):
    if 'email' in deleted_fields:
      deleted_fields.remove('email')
    self._deleted_fields = deleted_fields

  def remove_field(self,deleted_field):
    if deleted_field != 'email':
      self._deleted_fields.append(deleted_field)

  def get_undeleted_fields(self):
    if self.deleted_fields and len(self.deleted_fields) > 0:
      return sorted(list(set(self.fields) - set(self.deleted_fields)))
    return self.fields

  def __repr__(self):
    return '<User %r>' % (self.email)

  def save(self):
    print self.fields
    body = '{ "email": "%s", \
              "fields": "%s", \
              "deleted_fields": "%s" }'%(self.email,
                                         ','.join(self.fields),
                                         ','.join(self.deleted_fields))
    if self.id :
      self.es.update(index='users',
        doc_type='users',
        id=self.id,
        body='{ "doc" : %s }'%body
      )
    else :
      results = self.es.create(index='users',
        doc_type='users',
        body=body
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
    user.fields = hit['_source']['fields'].split(',')
    user.deleted_fields = hit['_source']['deleted_fields'].split(',')
    return user
