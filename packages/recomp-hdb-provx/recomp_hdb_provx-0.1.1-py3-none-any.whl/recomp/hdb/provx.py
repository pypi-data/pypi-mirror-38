# This Python file uses the following encoding: utf-8
""" Classes to ease communication with PrologHDB """

from datetime import datetime, timedelta
import logging
import requests

# Setup a logger
logger = logging.getLogger('recomp.provx')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter('%(asctime)s %(name)-10s %(levelname)-5s %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)


def strftime_prov(datetime_obj):
    '''Formats the datetime object according to the following format: "yyyy-MM-dd'T'HH:mm:ss.SSSZ".
    
    TODO: Make sure it follows the format imposed by the PROV specification.
    '''

    year, month, day, hour, minute, second = datetime_obj.timetuple()[:6]
    ms_delta = timedelta(microseconds=round(datetime_obj.microsecond / 1000.0) * 1000)
    ms_date = datetime(year, month, day, hour, minute, second) + ms_delta
    return ms_date.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


def get_prov_logger(provx_svc_url='', default_namespace='', namespaces=[]):
    return ProvLogger(provx_svc_url, default_namespace, namespaces)


def get_prov_client(provx_svc_url='', default_namespace='', namespaces=[]):
    return ProvClient(provx_svc_url, default_namespace, namespaces)


class _ProvBaseClass:

    def __init__(self, baseurl, default_namespace='', namespaces=[]):
        self._provx_svc_baseurl = baseurl
        self._default_namespace = default_namespace
        self._namespaces = namespaces


    def set_baseurl(self, baseurl):
        self._provx_svc_baseurl = baseurl


    def set_config(self, prov_baseref):
        self._provx_svc_baseurl = prov_baseref._provx_svc_baseurl
        self._default_namespace = prov_baseref._default_namespace
        self._namespaces = prov_baseref._namespaces



class ProvLogger(_ProvBaseClass):

    #
    # PROV statements
    #

    def entity(self, id=None, attributes=None):
        return self._put_op('entity', id, attributes)

    def set_entity(self, id, attributes=None):
        if id is None:
            raise Exception('Entity id cannot be None')

        return self._post_op('set', 'entity', id, attributes)

    def update_entity(self, id, attributes=None):
        if id is None:
            raise Exception('Entity id cannot be None')

        return self._post_op('update', 'entity', id, attributes)


    def used(self, activityId, entityId=None, time=None, attributes=None):
        return self.used_with_id(None, activityId, entityId=entityId, time=time, attributes=attributes)

    def used_with_id(self, id, activityId, entityId=None, time=None, attributes=None):
        # Arguments check
        if activityId is None:
            raise Exception('activityId cannot be None')

        # Preparing attributes for the call
        if attributes is None:
            attributes = {}

        attributes['prov:activity'] = activityId

        if entityId is not None:
            attributes['prov:entity'] = entityId
        if time is not None:
            attributes['prov:time'] = strftime_prov(time)

        return self._put_op('used', id, attributes)

    def set_used(self, id, activityId, entityId=None, time=None, attributes=None):
        if id is None:
            raise Exception('Usage id cannot be None')

        if activityId is None:
            raise Exception('activityId cannot be None')

        if attributes is None:
            attributes = {}

        attributes['prov:activity'] = activityId

        if entityId is not None:
            attributes['prov:entity'] = entityId
        if time is not None:
            attributes['prov:time'] = strftime_prov(time)

        return self._post_op('set', 'used', id, attributes)

    def update_used(self, id, activityId=None, entityId=None, time=None, attributes=None):
        if id is None:
            raise Exception('Usage id cannot be None')

        if attributes is None:
            attributes = {}

        if activityId is not None:
            attributes['prov:activity'] = activityId

        if entityId is not None:
            attributes['prov:entity'] = entityId

        if time is not None:
            attributes['prov:time'] = strftime_prov(time)

        return self._post_op('update', 'used', id, attributes)


    def hadMember(self, collectionId, entityId):
        if collectionId is None:
            raise Exception('CollectionId cannot be None')

        if entityId is None:
            raise Exception('EntityId cannot be None')

        attributes = { 'prov:collection' : collectionId, 'prov:entity' : entityId }

        return self._put_op('hadMember', None, attributes)


    def wasAssociatedWith(self, activityId, agent=None, plan=None, attributes=None):
        return self.wasAssociatedWith_with_id(None, activityId, agent=agent, plan=plan, attributes=attributes)

    def wasAssociatedWith_with_id(self, id, activityId, agent=None, plan=None, attributes=None):
        # Arguments check
        if activityId is None:
            raise Exception('activityId cannot be None')

        if id is None and agent is None and plan is None and attributes is None:
            raise Exception("At least one of 'id', 'agent', 'plan' and 'attributes' must be present.")

        # Preparing attributes for the call
        if attributes is None:
            attributes = {}

        attributes['prov:activity'] = activityId

        if agent is not None:
            attributes['prov:agent'] = agent

        if plan is not None:
            attributes['prov:plan'] = plan

        return self._put_op('wasAssociatedWith', id, attributes)

    def set_wasAssociatedWith(self, id, activityId, agent=None, plan=None, attributes=None):
        # Arguments check
        if id is None:
            raise Exception('Association id cannot be None')

        if activityId is None:
            raise Exception('activityId cannot be None')

        if id is None and agent is None and plan is None and attributes is None:
            raise Exception('At least one of id, agent, plan, attributes must be present.')

        # Preparing attributes for the call
        if attributes is None:
            attributes = {}

        attributes['prov:activity'] = activityId

        if agent is not None:
            attributes['prov:agent'] = agent

        if plan is not None:
            attributes['prov:plan'] = plan

        return self._post_op('set', 'wasAssociatedWith', id, attributes)

    def update_wasAssociatedWith(self, id, activityId, agent=None, plan=None, attributes=None):
        # Arguments check
        if id is None:
            raise Exception('Association id cannot be None')

        # Preparing attributes for the call
        if attributes is None:
            attributes = {}

        if activityId is not None:
            attributes['prov:activity'] = activityId

        if agent is not None:
            attributes['prov:agent'] = agent

        if plan is not None:
            attributes['prov:plan'] = plan

        return self._post_op('update', 'wasAssociatedWith', id, attributes)


    #def wasDerivedFrom(self, id, generated_entity, used_entity, activity=None, generation=None, usage=None, attributes=None):
    #    '''Logs wasDerivedFrom statement between the generated and used entities, and returns the derivation tuple (derivation_id, derivation_attributes) as stored by the prov service.
    #    
    #    The id may be None.
    #    '''
    #    pass
    #
    #
    #def wasDerivedFrom(self, generated_entity, used_entity, activity=None, generation=None, usage=None, attributes=None):
    #    return self.wasDerivedFrom(None, generated_entity, used_entity, activity, generation, usage, attributes)

    def wasGeneratedBy(self, entityId, activityId=None, time=None, attributes=None):
        return self.wasGeneratedBy_with_id(None, entityId, activityId=activityId, time=time, attributes=attributes)

    def wasGeneratedBy_with_id(self, id, entityId, activityId=None, time=None, attributes=None):
        # Arguments check
        if entityId is None:
            raise Exception('entityId cannot be None')

        # Preparing attributes for the call
        if attributes is None:
            attributes = {}

        attributes['prov:entity'] = entityId

        if activityId is not None:
            attributes['prov:activity'] = activityId

        if time is not None:
            attributes['prov:time'] = strftime_prov(time)

        return self._put_op('wasGeneratedBy', id, attributes)

    def set_wasGeneratedBy(self, id, entityId, activityId=None, time=None, attributes=None):
        if id is None:
            raise Exception('Generation id cannot be None')

        if entityId is None:
            raise Exception('entityId cannot be None')

        if attributes is None:
            attributes = {}

        attributes['prov:entity'] = entityId

        if activityId is not None:
            attributes['prov:activity'] = activityId

        if time is not None:
            attributes['prov:time'] = strftime_prov(time)

        return self._post_op('set', 'wasGeneratedBy', id, attributes)

    def update_wasGeneratedBy(self, id, entityId, activityId=None, time=None, attributes=None):
        if id is None:
            raise Exception('Generation id cannot be None')

        if attributes is None:
            attributes = {}

        if entityId is not None:
            attributes['prov:entity'] = entityId

        if activityId is not None:
            attributes['prov:activity'] = activityId

        if time is not None:
            attributes['prov:time'] = strftime_prov(time)

        return self._post_op('update', 'wasGeneratedBy', id, attributes)


    def wasInformedBy(self, informedId, informantId, attributes=None):
        return self.wasInformedBy_with_id(None, informedId, informantId, attributes)

    def wasInformedBy_with_id(self, id, informedId, informantId, attributes=None):
        # Arguments check
        if informedId is None:
            raise Exception('informedId cannot be None')

        if informantId is None:
            raise Exception('informantId cannot be None')

        # Preparing attributes for the call
        if attributes is None:
            attributes = {}

        attributes['prov:informed'] = informedId
        attributes['prov:informant'] = informantId

        return self._put_op('wasInformedBy', id, attributes)

    def set_wasInformedBy(self, id, informedId, informantId, attributes=None):
        if id is None:
            raise Exception('Communication id cannot be None')

        if informedId is None:
            raise Exception('informedId cannot be None')

        if informantId is None:
            raise Exception('informantId cannot be None')

        if attributes is None:
            attributes = {}

        attributes['prov:informed'] = informedId
        attributes['prov:informant'] = informantId

        return self._post_op('set', 'wasInformedBy', id, attributes)

    def update_wasInformedBy(self, id, informedId, informantId, attributes=None):
        if id is None:
            raise Exception('Communication id cannot be None')

        if attributes is None:
            attributes = {}

        if informedId is not None:
            attributes['prov:informed'] = informedId

        if informantId is not None:
            attributes['prov:informant'] = informantId

        return self._post_op('update', 'wasInfomedBy', id, attributes)


    #
    # ProvONE statements
    #

    def document(self, id=None, attributes=None):
        return self._put_op('document', id, attributes)

    def set_document(self, id, attributes=None):
        if id is None:
            raise Exception('Document id cannot be None')

        return self._post_op('set', 'document', id, attributes)

    def update_document(self, id, attributes=None):
        if id is None:
            raise Exception('Document id cannot be None')

        return self._post_op('update', 'document', id, attributes)


    def execution(self, id=None, startTime=None, endTime=None, attributes=None):
        '''Logs execution statement in the prov service and returns tuple (execution_id, execution_attributes) as stored by the provenance service.

        If id is None, the prov service will generate a unique id for the execution.
        If startTime is None, the current UTC datetime will be used (datetime.utcnow()).

        If set, both startTime and endTime should be datetime.datetime objects.

        If attributes is not None, it must be a dictionary with additional information about this execution.
        '''
        if attributes is None:
            attributes = {}

        if startTime is None:
            startTime = datetime.utcnow()
        attributes['prov:startTime'] = strftime_prov(startTime)

        if endTime is not None:
            attributes['prov:endTime'] = strftime_prov(endTime)

        return self._put_op('execution', id, attributes)

    def set_execution(self, id, startTime=None, endTime=None, attributes=None):
        '''TODO: Sets attributes of an existing execution.'''
        if id is None:
            raise Exception('Execution id cannot be None')

        if attributes is None:
            attributes = {}

        if startTime is None:
            startTime = datetime.utcnow()
        attributes['prov:startTime'] = strftime_prov(startTime)

        if endTime is not None:
            attributes['prov:endTime'] = strftime_prov(endTime)

        return self._post_op('set', 'execution', id, attributes)

    def update_execution(self, id, endTime=None, attributes=None):
        '''TODO: Update attributes of an existing execution.'''
        if id is None:
            raise Exception('Execution id cannot be None')

        if attributes is None:
            attributes = {}

        if endTime is not None:
            attributes['prov:endTime'] = strftime_prov(endTime)

        return self._post_op('update', 'execution', id, attributes)


    def hadInPort(self, usageId, portId):
        attributes = { 'prov:usage' : usageId, 'provone:port' : portId }
        return self._put_op('hadInPort', None, attributes)


    def hadOutPort(self, generationId, portId):
        attributes = { 'prov:generation' : generationId, 'provone:port' : portId }
        return self._put_op('hadOutPort', None, attributes)


    def program(self, id=None, attributes=None):
        return self._put_op('program', id, attributes)

    def set_program(self, id, attributes=None):
        if id is None:
            raise Exception('Program id cannot be None')

        return self._post_op('set', 'program', id, attributes)

    def update_program(self, id, attributes=None):
        if id is None:
            raise Exception('Program id cannot be None')

        return self._post_op('update', 'program', id, attributes)


    #
    # Internal operations
    #

    def _put_op(self, op_name, id, attributes):
        # If the prov service base URL is not set, do nothing.
        # TODO: Perhaps it is worth caching all these logs and send them once the base URL is set?
        #       To think about it.
        if self._provx_svc_baseurl is None:
            return (None, None)

        try:
            if id is None:
                r = requests.put(self._provx_svc_baseurl + '/' + op_name, json=attributes)
            else:
                r = requests.put(self._provx_svc_baseurl + '/' + op_name + '?id=' + id, json=attributes)

            if r.status_code == requests.codes.created:
                # A way to get the tuple with key (entity id) and value (entity attributes)
                return next(iter(r.json()[op_name].items()))
            else:
                logger.warn('Error when sending the provenance information of %s %s: (%d) %s', op_name, id, r.status_code, r.reason)
                logger.debug(r.text)
        except Exception as x:
            logger.error('Exception when sending provenance information: (%s) %s', type(x), x)


    def _post_op(self, op_type, op_name, id, attributes):
        # Basic arguments check
        if id is None:
            raise Exception('Identifier must be set for the %s %s operation', op_type, op_name)

        # If the prov service base URL is not set, do nothing.
        # TODO: Perhaps it is worth caching all these logs and send them once the base URL is set?
        #       To think about it.
        if self._provx_svc_baseurl is None:
            return (None, None)

        try:
            r = requests.post(self._provx_svc_baseurl + '/' + op_name + '?id=' + id + '&opType=' + op_type, json=attributes)
            if r.status_code == requests.codes.ok:
                return next(iter(r.json()[op_name].items()))
            else:
                logger.warn('Error updating the provenance information of %s %s: (%d) %s', op_name, id, r.status_code, r.reason)
                logger.debug(r.text)
        except Exception as x:
            logger.error('Exception when sending provenance information: (%s) %s', type(x), x)



class ProvClient(_ProvBaseClass):

    def document(self, id=None):
        try:
            if id is None:
                r = requests.get(self._provx_svc_baseurl + '/document')
            else:
                r = requests.get(self._provx_svc_baseurl + '/document?id=' + id)

            if r.status_code == requests.codes.ok:
                return r.json()['document']
            else:
                logger.warn('Error querying the provenance database: (%d) %s', r.status_code, r.reason)
                logger.debug(r.text)
        except Exception as x:
            logger.error('Exception when querying provenance database for document(s): (%s) %s', type(x), x)


    def query(self, query, inputs=None):
        # Basic arguments check
        if query is None or query.strip() == '':
            raise Exception('Query cannot be None nor empty.')

        # If the prov service base URL is not set, do nothing.
        if self._provx_svc_baseurl is None:
            raise Exception("Cannot query HDB: baseurl has not been set. Consider using the 'set_baseurl' operation")

        json_q = { 'query' : query }
        if inputs is not None:
            json_q['inputs'] = inputs

        try:
            r = requests.post(self._provx_svc_baseurl + '/query', json=json_q)
            if r.status_code == requests.codes.ok:
                return r.json()['result']
            else:
                logger.warn('Error querying the provenance database: your query = %s returned error = (%d) %s', json_q, r.status_code, r.reason)
                logger.debug(r.text)
        except Exception as x:
            logger.error('Exception when querying provenance database: (%s) %s', type(x), x)


    def query_document(self, query=None, id_var='DocId'):
        # If the prov service base URL is not set, do nothing.
        if self._provx_svc_baseurl is None:
            raise Exception("Cannot query HDB: baseurl has not been set. Consider using the 'set_baseurl' operation")

        json_q = {}
        if query is not None:
            json_q['query'] = query
        #if inputs is not None:
        #    json_q['inputs'] = inputs

        try:
            r = requests.post(self._provx_svc_baseurl + '/query/document?documentId=' + id_var, json=json_q)
            if r.status_code == requests.codes.ok:
                return r.json()['document']
            else:
                logger.warn('Error querying the provenance database: your query = %s returned error = (%d) %s', json_q, r.status_code, r.reason)
                logger.debug(r.text)
        except Exception as x:
            logger.error('Exception when querying provenance database: (%s) %s', type(x), x)
