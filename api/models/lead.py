from elasticsearch import Elasticsearch,RequestsHttpConnection,NotFoundError
from flask import url_for
import config
import json

class Lead(object):
  es = Elasticsearch(config.ES_HOSTS,connection_class=RequestsHttpConnection)

  @staticmethod
  def create_lead(lead_data):
    try:
      results = Lead.es.create(index='leads',
        doc_type='leads',
        body=lead_data
      )
      if results['created']:
        return { 'status': 'success',
                 'message': '',
                 'created_id': results['_id'] }
      else:
        return { 'status': 'failure',
                 'message': 'failed to create new lead.',
                 'created_id': '' }
    except Exception as e:
      print e
      return { 'status': 'failure',
               'message': 'unknown error',
               'created_id': '' }

  @staticmethod
  def delete_lead(lead_id):
    try :
      Lead.es.delete(index='leads',
        doc_type='leads',
        id=lead_id
      )
      return { 'status': 'success', 'message': '' }
    except NotFoundError as e:
      return { 'status': 'failure', 'message': 'id not found' }
    except Exception as e:
      print e
      return { 'status': 'failure', 'message': 'unknown error' }

  @staticmethod
  def get_lead(lead_id):
    try:
      results = Lead.es.get(
        index='leads',
        doc_type='leads',
        id='%s'%(lead_id),
        ignore=404
      )
      if results and results['found'] :
        return {'status':'success','message':'','results':[Lead.from_es_hit(results)]}
      return {'status':'success','message':'','results':[]}
    except NotFoundError as e:
      return { 'status': 'failure', 'message': 'id not found', 'results': [] }
    except Exception as e:
      print e
      return { 'status': 'failure', 'message': 'unknown exception', 'results': [] }

  @staticmethod
  def get_leads(size,page,search):
    try:
      results = Lead.es.search(
        index='leads',
        doc_type='leads',
        size=size,
        q=search or "*",
        sort='last_name:ASC,first_name:ASC'
      )
      retVal = []
      if results and results['hits']['total'] > 0 :
        for hit in results['hits']['hits']:
          retVal.append(Lead.from_es_hit(hit))
      return {'status':'success','message':'','results':retVal}
    except Exception as e:
      print e
      return {'status':'failure','message':'unknown error','results':[]}

  @staticmethod
  def from_es_hit(hit):
    lead = {}
    lead['id'] = hit['_id']
    for key,val in hit['_source'].items():
      lead[key] = val
    lead['uri'] = url_for('get_lead', lead_id=lead['id'], _external=True)
    return lead
