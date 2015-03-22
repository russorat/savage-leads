from elasticsearch import Elasticsearch
import uuid
import hashlib

class Login(object):
  es = Elasticsearch()

  def __init__(self,e=None,s=uuid.uuid4().hex,p=None):
    self._id = None
    self._email = e
    self._salt = s
    self._password = p

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
  def salt(self):
    return self._salt

  @property
  def password(self):
    return self._password

  @password.setter
  def password(self,unhashed_pass):
    if self.salt:
      first_hash = hashlib.sha512(b'%s'%unhashed_pass).hexdigest()
      self._password = hashlib.sha512(b'%s%s'%(first_hash,self.salt)).hexdigest()
      first_hash = None
    else:
      raise 'Cannot set password without a salt'

  def set_pass_from_hashed_pass(self,hashed_pass):
    if self.salt:
      self._password = hashlib.sha512(b'%s%s'%(hashed_pass,self.salt)).hexdigest()
      first_hash = None
    else:
      raise 'Cannot set password without a salt'

  def __repr__(self):
      return '<Login %r>' % (self.email)

  def save(self):
    if self.id :
      self.es.update(index='logins',
        doc_type='logins',
        id=self.id,
        body='{ "doc" : { "email":"%s", "salt":"%s", "password":"%s" } }'%(self.email,self.salt,self.password)
      )
    else :
      results = self.es.create(index='logins',
        doc_type='logins',
        body='{ "email":"%s", "salt":"%s", "password":"%s" }'%(self.email,self.salt,self.password)
      )
      if results['created']:
        self.id = results['_id']
      else:
        raise 'Failed to create new login.'

  def check_password(self,check_against_hashed):
    return (hashlib.sha512(b'%s%s'%(check_against_hashed,self.salt)).hexdigest() == self.password)

  def delete(self):
    self.es.delete(index='logins',
      doc_type='logins',
      id=self.id
    )
    self.id=None

  @staticmethod
  def try_login(email,hashed_pass):
    results = Login.es.search(
      index='logins',
      doc_type='logins',
      size=10000,
      q='email:"%s"'%email
    )
    if(results and results['hits']['total'] > 0):
      for hit in results['hits']['hits']:
        possible_login = Login.from_es_hit(hit)
        if possible_login.check_password(hashed_pass):
          return True
    return False

  @staticmethod
  def from_es_hit(hit):
    login = Login(hit['_source']['email'],
                  hit['_source']['salt'],
                  hit['_source']['password'])
    login.id = hit['_id']
    return login
