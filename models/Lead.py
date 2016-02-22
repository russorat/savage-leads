from elasticsearch import Elasticsearch
import config
import json

class Lead(object):
  es = Elasticsearch(config.ES_HOSTS)

  def __init__(self,data = None):
    self.id = None
    if data:
      for key,val in data.items():
        self.__dict__[key] = val

  def __getitem__(self,name):
    return self.__dict__[name]

  @property
  def id(self):
    return self._id

  @id.setter
  def id(self,val):
    self._id = val

  def delete(self):
    self.es.delete(index='leads',
      doc_type='leads',
      id=self.id
    )
    self.id=None

  def update(self,data):
    for key,val in data.items():
      self.__dict__[key] = val

  def save(self):
    lead_body = json.dumps(self.__dict__)
    if self.id :
      self.es.update(index='leads',
        doc_type='leads',
        id=self.id,
        body='{ "doc" : %s }'%(lead_body)
      )
    else :
      results = self.es.create(index='leads',
        doc_type='leads',
        id='%s-%s'%(self.owner_id,self.email),
        body=lead_body
      )
      if results['created']:
        self.id = results['_id']
      else:
        raise 'Failed to create new lead.'

  @staticmethod
  def get(user_id,email):
    results = Lead.es.get(
      index='leads',
      doc_type='leads',
      id='%s-%s'%(user_id,email),
      ignore=404
    )
    if results and results['found'] :
      return Lead.from_es_hit(results)
    return None

  @staticmethod
  def get_leads(user_id):
    results = Lead.es.search(
      index='leads',
      doc_type='leads',
      q='owner_id:"%s"'%user_id,
      size=1000,
      sort='last_name:ASC,first_name:ASC'
    )
    retVal = []
    if results and results['hits']['total'] > 0 :
      for hit in results['hits']['hits']:
        retVal.append(Lead.from_es_hit(hit))
    return retVal

  @staticmethod
  def from_es_hit(hit):
    lead = Lead()
    lead.id = hit['_id']
    for key,val in hit['_source'].items():
      if '_id' != key:
        lead.__dict__[key] = val
    return lead
