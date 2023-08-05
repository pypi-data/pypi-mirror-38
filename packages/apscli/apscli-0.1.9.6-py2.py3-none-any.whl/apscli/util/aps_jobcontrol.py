'''
This file's author is Pengfei(pengfei.qiao@oracle.com), thanks for his hard work.
'''

content_type = "application/json"
apsuser = "perfapi"
apspwd = "perfDB321"
httptimeout = 20
sleepseconds = 5

# import urllib2
try:
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request
    
import base64
import ssl
import json
import re
import time 

import logging

log = logging.getLogger(__name__)

domain_base_url = {
    "SAAS":"https://pdit-tools-vip.oracleoutsourcing.com/CSIJC",
    "PAAS":"https://pdit-tools-vip.oracleoutsourcing.com/CSIJC-PAAS",
    "EIS":"https://eis-tools.us.oracle.com/CSIJC",
    "DIS":"https://dis-tools.us.oracle.com/CSIJC",
    "PAAS_QA":"https://opcinfra-tools.us.oracle.com/CSIJC"
}

domain='SAAS'

subfixurl = 'api/v1/jobs'
subfixurl_inputdatabag = 'api/databag?JOBID={0}&DATABAG_TYPE=INPUT_DATABAG'
subfixurl_outputdatabag = 'api/databag?JOBID={0}&DATABAG_TYPE=OUTPUT_DATABAG'

LOCAL_URL = {'runjob': '{0}/{1}'.format(domain_base_url[domain], subfixurl),
            'input'  : '{0}/{1}'.format(domain_base_url[domain], subfixurl_inputdatabag),
            'output' : '{0}/{1}'.format(domain_base_url[domain], subfixurl_outputdatabag),
            'setjob' : '{0}/{1}'.format(domain_base_url[domain], subfixurl)}


def get(url):
    '''
    Script to submit GET request

    Args:
        url : (str) REST API URL
    Returns:
        response (dict)
    Raises:    
    '''
    try:
        output_url=url
        request = Request(output_url)
        base64string = base64.b64encode('%s:%s' % (apsuser, apspwd))
        request.add_header("Authorization", "Basic %s" % base64string)  

        result = None
        try:
            https_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            result = urlopen(request,context=https_context)
        except AttributeError:
            result = urlopen(request)

        obj=json.loads(result.read())
        return 0, obj

    except Exception as e:
        log.error('Failed to send get: '+str(e))
        raise


def post(url, inputdata):
    '''
    Script to post JSON data to REST API

    Args:
        url : (str) REST API URL
        inputdata : (dict) data in JSON format
    Returns:
        response (dict)
    Raises:    
    '''

    try:
        output_url=url
        req = Request(output_url , json.dumps(inputdata), {'Content-Type': content_type})
        base64string = base64.b64encode('%s:%s' % (apsuser, apspwd))
        req.add_header("Authorization", "Basic %s" % base64string)

        f = None
        try:
            https_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            f = urlopen(req,timeout=httptimeout,context=https_context)
        except AttributeError:
            f = urlopen(req,timeout=httptimeout)

        response = json.loads(f.read())
        f.close()

        return 0, response

    except Exception as e:
        log.error('Failed to send a POST request: '+str(e))
        raise
        

def read_databag(jobid, type):
    """read databag data by parsing databag via REST API
    Args:
        jobid : (int) job id
        type  : (str) input|output
    Returns:
        exec_status (int):  0: success, 1: fail
        databag_data(list):  the content of data bag
    Raises:
        Exception:

    Note:
        1. The return type is list, for output databag, meaning each writting databag, the databag will append a new member
    """

    try:
        log.debug("Reading {0} databag of the JC job {1}...".format(type, jobid))

        # construct request data
        if type not in ('input', 'output'):
            log.error('Please input correct type (%s)' % '|'.join(('input', 'output')))
            return 1, None

        if not str(jobid).isdigit():
            log.error('Please input correct jobid.')
            return 1, None

        local_url = LOCAL_URL[type].format(jobid)

        log.debug("URL to read databag: \n {0}".format(local_url))

        # submit and get status / job_id
        retval, result = get(local_url)

        log.debug("return databag:")
        log.debug(result)

        if result['status'] == 'OK':
            databag_data = result['data'] ['databags']
            return 0, databag_data
        elif result['status'] == 'SRVEXCEPTION':
            # log.warning("Failed to read " + type + " databag for the job {0} with unhandled or server side exception".format(jobid))
            log.debug("Failed to read " + type + " databag for the job {0} with unhandled or server side exception".format(jobid))
            return 0, [{}]   # user doesn't upload any databag_json_file
        else:
            log.error("Databag data status is not 'OK'.")
            return 1, None

    except:
        log.error('Failed to read databag for jobid {0}'.format(str(jobid)))
        raise


def write_output_databag(jobid, outputdatabag):
    '''
    Write data into output databag

    Args:
        jobid : (int) job id
        outputdatabag  : (dict) data to write
    Returns:
        exec_status (int):  0: success, 1: fail
    Raises:

    Note:
        1. you can write output databag into a same Job more than 1 time. 
        With each write, output_databag will add it as a member of list
    '''
    try:
        log.debug("Writting output databag for the JC job {0}...".format(jobid))

        # Validate input arguments
        if not str(jobid).isdigit():
            log.error('Please input correct jobid.')
            return 1

        if not outputdatabag or not isinstance(outputdatabag, dict):
            log.error('Please input correct databag in dict.')
            return 1

        # construct request data
        submit_data = outputdatabag

        log.debug("The data to submit: \n {0}".format(json.dumps(submit_data)))

        # submit and get status / job_id
        retval, result = post(LOCAL_URL['output'].format(jobid), submit_data)

        log.debug("Response payload:")
        log.debug(result)

        if retval == 0 and result['status'] == 'OK':
            log.debug("{0}.".format(result['data']))
            log.debug("Writing outputdatabag for the job {0} completed.".format(jobid))
            return 0
        elif retval == 0 and result['status'] == 'ERROR':
            log.error("Failed to write output databag for the job {0} with error {1}".format(jobid, result['data']))
            return 1
        elif retval == 0 and result['status'] == 'SRVEXCEPTION':
            log.error("Failed to write output databag for the job {0} with unhandled or server side exception".format(jobid))
            return 1                
        else:
            log.error("Failed to write output databag for the job {0}.".format(jobid))
            return 1

    except:
        log.error('Writting output databag failed!')
        raise