import ssl, json, base64, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from inspect import isfunction
from functools import partial
try:
    from urllib2 import urlopen, Request
    PY_VERSION=2
except ImportError:
    from urllib.request import urlopen, Request
    PY_VERSION=3


def url_2_http_request(url, content_type='application/json', data=None, headers=None, user=None, pwd=None):
    
    if headers is None:
        headers = {}
    
    if user and pwd:
        base64string = base64.b64encode('%s:%s' % (user, pwd))
        headers['Authorization'] = "Basic %s" % base64string

    headers['content-type'] = content_type

    if data is None:    # get
        return Request(url, headers)
    else:               # post
        if content_type=='application/json':
            return Request(url, json.dumps(data), headers)
        else:
            raise NotImplementedError


def post_json_request(url, data, user=None, pwd=None, resp_handler=json.loads, timeout_secs=None):
    """send HTTP request for GET/POST/PATCH
    Args:
        url       (string): url
        timeout_secs (int): (default=5) http timeout_secs
    Returns:
        response (dict)
    Raises:
        Exception: urllib2 errors
    """
    req = url_2_http_request(url, data=data, headers=None, user=user, pwd=pwd)

    if PY_VERSION==2:
        f=None
        try:
            f = urlopen(req, timeout=timeout_secs,
                context=ssl.SSLContext(ssl.PROTOCOL_SSLv23) if req.get_full_url().startswith('https://') else None
            )
            return resp_handler(f.read()) if isfunction(resp_handler) else f.read()
        except Exception as e:
            return str(e)
        finally:
            if f is not None:
                f.close()
    else:
        from urllib.request import HTTPSHandler, build_opener, install_opener
        try:
            opener = build_opener(HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_SSLv23)))
            install_opener(opener)
            resp = opener.open(req, timeout=timeout_secs)
            return resp_handler(resp.read().decode('utf-8')) if isfunction(resp_handler) else resp.read().decode('utf-8')
        except Exception as e:
            return str(e)


'''
def handle_urls_in_parallel(url_handler, urls, max_workers=None, *args, **kwargs):
    assert isfunction(url_handler), '`url_handler must be a user_defined_function to handler a url'
    results = {}
    # We can use a with statement to ensure threads are cleaned up promptly
    with ThreadPoolExecutor(max_workers=max_workers if max_workers else len(urls)) as executor:
        # Start the load operations and mark each future with its URL
        dic = {executor.submit(url_handler, url, *args, **kwargs): url for url in urls}
        # submit(url_handler, url, *args, )
        for fu in as_completed(dic.keys()):
            try:
                results[dic[fu]] = fu.result()
            except Exception as exc:
                import traceback
                traceback.print_exc()
                results[dic[fu]] = sys.exc_info()[1:2] # 'Exception: %s' % exc

    return results
'''

def handle_urls_in_parallel(url_handler, urls, max_workers=None, *args, **kwargs):
    assert isfunction(url_handler), '`url_handler must be a user_defined_function to handler a url'
    urls = list(set(urls))
    results = {}
    # We can use a with statement to ensure threads are cleaned up promptly
    with ThreadPoolExecutor(max_workers=max_workers if max_workers else len(urls)) as executor:
        # Start the load operations and mark each future with its URL
        dic = {executor.submit(url_handler, url, *args, **kwargs): url for url in urls}
        # submit(url_handler, url, *args, )
        for fu in as_completed(dic.keys()):
            try:
                results[dic[fu]] = fu.result()
            except Exception as exc:
                import traceback
                traceback.print_exc()
                results[dic[fu]] = sys.exc_info()[1:2] # 'Exception: %s' % exc
    
    return results

post_json_requests_in_parallel = partial(handle_urls_in_parallel, post_json_request)


def dispatch_jobs(urls, fqsn, trace_id, wf_param=None, auth_user=None, auth_pwd=None, concurrent_policy='all'):
    if wf_param is None:
        wf_param = {}
    assert isinstance(wf_param, dict), 'wf_param should be a dict'
    data = {
        'service': {"fqsn": fqsn, "cmdline_param_dic": wf_param}, 
        'trace_id': trace_id
    }
    if concurrent_policy == 'all':
        return post_json_requests_in_parallel(urls, data=data, user=auth_user, pwd=auth_pwd)
        '''return {
            'return_code': all([all_resp[url]['status']=='success' for url in all_resp]) ^ 0,
            'output': all_resp 
        }'''
    elif concurrent_policy == 'single_max':
        return {max(urls): post_json_request(max(urls), data, auth_user, auth_pwd)}
        '''return {
            'return_code': resp['status']=='success' ^ 0,
            'output': {max(urls): resp}
        }'''
    elif concurrent_policy == 'single_min':
        return {min(urls): post_json_request(min(urls), data, auth_user, auth_pwd)}
        '''return {
            'return_code': resp['status']=='success' ^ 0,
            'output': {min(urls): resp}
        }'''
    elif concurrent_policy == 'rolling':
        return {url: post_json_request(url, data, auth_user, auth_pwd) for url in urls}
        '''return {
            'return_code': all([all_resp[url]['status']=='success' for url in all_resp]) ^ 0,
            'output': all_resp
        }'''
    else:
        raise ValueError('concurrent_policy can be only {all|single_max|single_min|rolling}')


'''
def fetch_urls_in_parallel(urls, resp_handler, max_workers=None):

    results = {}
    # We can use a with statement to ensure threads are cleaned up promptly
    with ThreadPoolExecutor(max_workers=max_workers if max_workers else len(urls)) as executor:
        # Start the load operations and mark each future with its URL
        dic = {executor.submit(_send_request, Request(url), resp_handler): url for url in URLS}
        for fu in as_completed(dic.keys()):
            try:
                results[dic[fu]] = fu.result()
            except Exception as exc:
                results[dic[fu]] = 'Exception: %s' % exc

    return results

def post_with_basic_http_auth(url, input_data, user='j', pwd='j', timeout_secs=5):
    """send POST request to REST API with JSON data
    Args:
        url          (str): REST API URL
        input_data  (dict): data in JSON format
        timeout_secs (int): (default=5) http timeout_secs
    Returns:
        tuple(exec_status, response)
            exec_status (bool): True for success, False for fail
            response    (dict)
    Raises:
        Exception: urllib2 errors
    """
    try:
        req = Request(url, json.dumps(input_data), {'Content-Type': "application/json"})
        base64string = base64.b64encode('%s:%s' % (user, pwd))
        req.add_header("Authorization", "Basic %s" % base64string)

        return _send_request(req, json.load, timeout_secs)
    except:
        # log.warn("Failed to send POST request!\n{0}".format(sys.exc_info()[1:2]))
        raise
'''

if __name__ == '__main__':
    URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/'
    ]

    URLS1 = ['http://127.0.0.1:8080/api/fqsn/run',
        'http://127.0.0.1:8080/api/fqsn/run',
        'http://127.0.0.1:8080/api/fqsn/run',
        'http://127.0.0.1:8080/api/fqsn/run',
        'http://127.0.0.1:8080/api/fqsn/run'
    ]

    d = {
        "service": {
            "fqsn": "oracle.peo.self_healing.db01.workflow_02",
            "param": {
                "ver_calc": "op_ctrl.sh",
                "version": "20180730",
                "vm_id":1,
                "vm_name":"test01_vm",
                "ip":"1.1.1.1",
                "storage_name":"storage01",
                "vm_id":1,
                "p": "ppp",
                "e": "eee",
                "fqsn": "/mnt/d/Python_Project/git/aps-sre-selfservice/flow_engine/workflow02.template",
                "wf_param_filename": "/mnt/d/Python_Project/git/aps-sre-selfservice/flow_engine/workflow01.param.json",
                "s_name": "storage_01",
                "EM": True
            }
        },
        "devices":[
            "slcc31client01.us.oracle.com", "JIANG-PC.cn.oracle.com", "yyy"
        ]
    }

    print(
        json.dumps(
            post_json_requests_in_parallel(URLS, data=d, user='j', pwd='j'), 
            indent=4
        )
    )