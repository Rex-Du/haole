import time

import MySQLdb
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

"""
PUT haolearticle
{
  "settings":{
    "number_of_shards": 3,   
    "number_of_replicas": 1	,
    "analysis":{   
      "analyzer":{
        "ik":{
          "tokenizer":"ik_max_word"
        }
      }
    }
  },
  "mappings":{
    "article":{
      "properties":{
        "id":{
          "type":"keyword"
        },
        "title":{
          "type":"text"
        },
        "status":{
            "type":"keyword"
            },
        "platform":{
          "type":"keyword"
        },
                "content_html":{
          "type":"text"
        }
      }
    }
  }
}
"""
body = {
    "settings": {
        "number_of_shards": 3,
        "number_of_replicas": 1,
        "analysis": {
            "analyzer": {
                "ik": {
                    "tokenizer": "ik_max_word"
                }
            }
        }
    },
    "mappings": {
        "article": {
            "properties": {
                "id": {
                    "type": "keyword"
                },
                "title": {
                    "type": "text"
                },
                "status": {
                    "type": "keyword"
                },
                "platform": {
                    "type": "keyword"
                },
                "content_html": {
                    "type": "text"
                }
            }
        }
    }
}


def create_index():
    es = Elasticsearch(['111.229.61.201:9200'])
    es.indices.delete(index='haolearticle')
    print('done')
    es.indices.create(index='haolearticle', body=body)
    print('done2')


def query_data_from_mysql():
    print('mysql start ...')
    start_time = time.time()
    conn = MySQLdb.connect(host='localhost', database='haolearticle', user='root', passwd='rootroot', port=3306, charset="utf8")
    cursor = conn.cursor()

    cursor.execute("select id, title, content_html, platform, status from home_article")

    results = cursor.fetchall()
    data = list()
    for result in results:
        # print(result)
        data.append({'id': result[0], 'title': result[1], 'content_html': result[2], 'platform': result[3],
                     'status': result[4]})
    print(f'mysql end {data.__len__()}, cost: {time.time() - start_time}')
    return data


def put_data_to_es(data):
    print('es start ....')
    start_time = time.time()
    # es = Elasticsearch(['localhost:9200'])
    es = Elasticsearch(['111.229.61.201:9200'])
    actions = list()
    for d in data:
        action = {
            "_index": "haolearticle",
            "_type": "article",
            "_source": d
        }
        actions.append(action)
    bulk(es, actions)
    print(f'es end cost: {time.time() - start_time}')


if __name__ == '__main__':
    data = query_data_from_mysql()
    put_data_to_es(data)
    # create_index()