"""
GET haolearticle/_search
{
  "query": {
    "match": {
      "title":"老婆妹妹"
    }
  },
   "_source":["id", "title"]
}

GET haolearticle/_search
{
    "query":{
        "multi_match": {
            "query":"别打我的主意",
            "type": "most_fields",
            "fields": [ "title", "content_html" ]
        }
    },
    "_source":["id", "title"]
}

GET haolearticle/_search
{
  "query": {
    "match_phrase": {
        "content_html" : {
            "query" : "非常
        }
    }
  },
  "_source":["id", "title"]
}
"""
from elasticsearch import Elasticsearch

es = Elasticsearch(["111.229.61.201:9200"])
body = {
    "query": {
        "match_phrase": {
            "content_html": {
                "query": "非常刺激"
            }
        }
    },
    "_source": ["id", "title",  "platform"],
    "size": 10,
}
results = es.search(index='haolearticle', body=body)
print(results.get('hits'))
