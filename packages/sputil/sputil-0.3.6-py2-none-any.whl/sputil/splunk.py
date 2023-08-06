# -*- coding: utf-8 -*-

'''
Created on 2018. 9. 12.
@author: jason96
'''
from base import SplunkBase, SPINDEX
from splunklib import results
import requests
import json
import uuid


class SPException(Exception):

    def __init__(self, message):
        super(SPException, self).__init__(message)


class Indexer(SplunkBase):

    def __init__(self):
        super(Indexer, self).__init__()
        if SPINDEX not in self.service.indexes:
            self.service.indexes.create(SPINDEX)

    def index(self, index, doc, sourcetype='json', host='local'):
        if index in self.service.indexes:
            target = self.service.indexes[index]
            return target.submit(doc, sourcetype=sourcetype, host=host)
        else:
            raise SPException('No index specified.')


class Searcher(SplunkBase):

    def __init__(self):
        super(Searcher, self).__init__()

    def search_results_list(self, response):
        results_list = []
        reader = results.ResultsReader(response)
        for result in reader:
            if isinstance(result, dict):
                results_list.append(result)
        return results_list

    def search(self, spl):
        kwargs = {"count": 0}
        oneshotsearch_results = self.service.jobs.oneshot(spl, **kwargs)
        return self.search_results_list(oneshotsearch_results)


class ITSIManager(SplunkBase):
    '''
    This class is based on version 3.1.0(ITSI)
    http://docs.splunk.com/Documentation/ITSI/3.1.0/RESTAPI/ITSIRESTAPIreference
    http://docs.splunk.com/Documentation/ITSI/3.1.0/RESTAPI/ITSIRESTAPIschema
    '''

    def __init__(self):
        super(ITSIManager, self).__init__()
        base_uri = 'https://%s:8089/servicesNS/nobody/SA-ITOA/itoa_interface'
        self.base_uri = base_uri % (self.config['splunk_ip'],)

    def get_uuid(self,):
        return str(uuid.uuid1()).replace('-', '')[:24]

    def get_services(self,):
        self.itsi_uri = ('%s/%s') % (self.base_uri, 'service',)
        req = requests.get(self.itsi_uri,
                           auth=(self.config['splunk_id'],
                                 self.config['splunk_password']),
                           verify=False)
        return json.loads(req.content)
    
    def get_kpi_ids(self):
        self.itsi_uri = ('%s/%s') % (self.base_uri, 'service',)
        req = requests.get(self.itsi_uri,
                           auth=(self.config['splunk_id'],
                                 self.config['splunk_password']),
                           verify=False)
        tag_kpi_ids = {}
        for service in json.loads(req.content):
            for kpi in service['kpis']:
                tag_kpi_ids[str(kpi['title'])] = kpi['_key']
        return tag_kpi_ids

    def add_kpi_base_search_metrics(self, title, metrics):
        kpi_base = None
        for kpi_base_search in self.get_kpi_base_searches():
            if kpi_base_search['title'] == title:
                kpi_base = kpi_base_search
        if kpi_base is not None:
            kpi_base['metrics'] = metrics
            self.itsi_uri = ('%s/%s/%s') % (self.base_uri,
                                            'kpi_base_search',
                                            kpi_base['_key'])
            req = requests.put(self.itsi_uri,
                               auth=(self.config['splunk_id'],
                                     self.config['splunk_password']),
                               data=json.dumps(kpi_base),
                               verify=False)
            return json.loads(req.content)
        else:
            return None

    def get_kpi_base_searches(self):
        self.itsi_uri = ('%s/%s') % (self.base_uri, 'kpi_base_search',)
        req = requests.get(self.itsi_uri,
                           auth=(self.config['splunk_id'],
                                 self.config['splunk_password']),
                           verify=False)
        return json.loads(req.content)

    def del_kpi_base_search(self, title):
        # fields='title''&'filter='\{"title":"bar"\}' -X DELETE
        self.itsi_uri = ('%s/%s') % (self.base_uri, 'kpi_base_search',)
        post_data = {}
        post_data['fields'] = 'title'
        post_data['filter'] = {"title": title}
        requests.delete(self.itsi_uri, auth=(self.config['splunk_id'],
                                             self.config['splunk_password']),
                        data=json.dumps(post_data),
                        verify=False)

    def add_kpi_base_search(self, title, desc=''):
        self.itsi_uri = ('%s/%s') % (self.base_uri, 'kpi_base_search',)
        post_data = {}
        post_data['title'] = title
        post_data['description'] = desc
        req = requests.post(self.itsi_uri,
                            auth=(self.config['splunk_id'],
                                  self.config['splunk_password']),
                            data=json.dumps(post_data),
                            verify=False)
        return json.loads(req.content)

    def fill_kpi(self, kpi, base_title, base_id, base_spl,
                 metric_title, metric_id, service_id, unit):

        uuid = self.get_uuid()
        kpi['base_search'] = base_spl
        kpi['base_search_id'] = base_id
        kpi['base_search_metric'] = metric_id
        kpi['cohesive_ad'] = '{sensitivity: 8}'
        kpi['cohesive_anomaly_detection_is_enabled'] = False
        kpi['description'] = metric_title
        kpi['enabled'] = 1
        kpi['entity_alias_filtering_fields'] = None
        kpi['entity_breakdown_id_fields'] = "host"
        kpi['entity_id_fields'] = "host"
        kpi['entity_statop'] = "avg"
        kpi['kpi_base_search'] = base_spl
        kpi['metric_qualifier'] = ""
        kpi['search'] = base_spl
        sagg = "%s | `aggregate_raw_into_single_value(avg, %s, 5)` |" + \
            " `assess_severity(%s, %s)` " % (base_spl, metric_title,
                                             service_id, uuid)
        kpi['search_aggregate'] = sagg
        salert = "%s | `aggregate_raw_into_service(avg, %s)` |" + \
            " `assess_severity(%s, %s, true, true)` eval kpi=\"%s\", " + \
            " urgency=\"5\", alert_period=\"1\", serviceid=\"%s\" | " + \
            " `assess_urgency` " % (base_spl, metric_title,
                                    service_id, uuid,
                                    metric_title, service_id)
        kpi['search_alert'] = salert
        kpi['search_alert_earliest'] = "5"
        kpi['search_alert_entities'] = ""
        kpi['search_buckets'] = ""
        sentities = "%s | `aggregate_raw_into_single_value(avg, %s, 5)` |" + \
            " `assess_severity(%s, %s)` " % (base_spl, metric_title,
                                             service_id, uuid)
        kpi['search_entities'] = sentities
        kpi['search_occurrences'] = 1
        scompare = "%s | `aggregate_raw_and_compare(avg, %s, 5)` |" + \
            " `assess_severity(%s, %s)` " % (base_spl, metric_title,
                                             service_id, uuid)
        kpi['search_time_compare'] = scompare
        sseries = "%s | " + \
            "`aggregate_raw_into_service_time_series(avg, %s, 5)` |" + \
            " `assess_severity(%s, %s)` " % (base_spl, metric_title,
                                             service_id, uuid)
        kpi['search_time_series'] = sseries
        kpi['search_time_series_aggregate'] = sseries
        kpi['search_time_series_entities'] = sseries
        kpi['search_type'] = "shared_base"
        kpi['sec_grp'] = "default_itsi_security_group"
        kpi['service_id'] = "0ed0273b-3fe8-4cdd-8328-651984c3ff45"
        kpi['service_title'] = base_title
        kpi['source'] = ""
        kpi['target'] = ""
        kpi['threshold_field'] = metric_title
        kpi['time_variate_thresholds'] = False
        kpi['title'] = metric_title
        kpi['trending_ad'] = "{sensitivity: 8}"
        kpi['type'] = base_spl
        kpi['base_search'] = "kpis_primary"
        kpi['tz_offset'] = None
        kpi['unit'] = unit
        kpi['urgency'] = "5"
        kpi['_key'] = uuid
        kpi['_owner'] = "nobody"
