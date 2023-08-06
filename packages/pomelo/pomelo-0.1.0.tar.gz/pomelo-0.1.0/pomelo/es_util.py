from elasticsearch import Elasticsearch

class ESUtil(object):
    def __init__(self,url,timeout = 200):
        self.es_url = url
        self.timeout = timeout
        self.es = Elasticsearch(self.es_url,timeout = self.timeout)
    
    '''
        从elasticsearch中聚合nginx日志
        默认是最近7天的，间隔3h聚合数据
    '''
    def aggs_nginx(self,msg_filter,dt_range = "7d",interval = "3h",index_name = 'logstash-*'):
        data = {
            "stored_fields": ["@timestamp","request"], 
            "query" : {
                "bool": {
                    "must" : {
                        "match":{"message":msg_filter}
                    },
                    "filter": {
                        "range":{
                            "@timestamp":{"gt":"now-" + dt_range}
                        }
                    }
                }
            },
            "aggs" : {
                "histo1" : {
                    "date_histogram" : {
                        "field" : "@timestamp",
                        "interval" : interval,
                        "time_zone":"+08:00"
                    }, 
                    "aggs": { 
                        "by_requests": { 
                            "terms":{
                                "field" : "@timestamp"
                            }
                        }
                    }
                }
            }
        }
        res = self.es.search(
            index = index_name,
            body = data
        )
        x_lab = []
        x_val = []
        for hit in res['aggregations']['histo1']['buckets']:
            x_lab.append(hit['key_as_string'].replace('T',' ').replace('+08:00',''))
            x_val.append(hit['doc_count'])
        return x_lab,x_val