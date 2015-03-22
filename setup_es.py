from elasticsearch import Elasticsearch
import json
import sys,time
es = Elasticsearch()

if len(sys.argv) > 1 and sys.argv[1] == '--clear':
  es.indices.delete(index='leads', ignore=400)
  es.indices.delete(index='logins', ignore=400)
  es.indices.delete(index='users', ignore=400)
  time.sleep(1)


#Create each index
es.indices.create(index='leads', ignore=400)
es.indices.create(index='logins', ignore=400)
es.indices.create(index='users', ignore=400)

#apply mappings if needed
mapping = """{
  "template": "",
  "settings": {
    "index.analysis.analyzer.default.stopwords": "_none_",
    "index.refresh_interval": "5s",
    "index.analysis.analyzer.default.type": "standard",
    "index.number_of_shards": "1",
    "index.number_of_replicas": "1"
  },
  "mappings": {
    "_default_": {
      "dynamic_templates": [{
        "string_fields": {
          "mapping": {
            "type": "multi_field",
            "fields": {
              "raw": {
                "index": "not_analyzed",
                "search_analyzer": "keyword",
                "ignore_above": 256,
                "type": "string"
              },
              "{name}": {
                "index": "analyzed",
                "omit_norms": true,
                "type": "string"
              }
            }
          },
          "match_mapping_type": "string",
          "match": "*"
        }
      }],
      "_all": {
        "enabled": true
      }
    }
  }
}"""
json_mapping = json.loads(mapping)
#Apply leads Mapping
json_mapping['template'] = 'leads*'
leads_mapping = json.dumps(json_mapping)
es.indices.put_template(name='leads',body=leads_mapping)

#apply users mapping
json_mapping['template'] = 'users*'
users_mapping = json.dumps(json_mapping)
es.indices.put_template(name='users',body=users_mapping)

#apply logins mapping
json_mapping['template'] = 'logins*'
logins_mapping = json.dumps(json_mapping)
es.indices.put_template(name='logins',body=logins_mapping)
