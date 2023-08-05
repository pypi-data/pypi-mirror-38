# encoding=utf-8

import json, logging, os, time, traceback, re, base64, random

import tornado.ioloop
from tornado.gen import coroutine,sleep
from tornado.web import RequestHandler, Application, authenticated
from tornado.escape import json_encode, json_decode

from logging import getLogger, DEBUG
from log import daemon_file_handler

log = getLogger(__name__)
log.setLevel(DEBUG)
log.addHandler(daemon_file_handler)


# HTTP_BASIC_AUTH
def check_credentials(user, pwd):
    from hashlib import md5
    try:
        return user=='user' and pwd=='pwd'
    except Exception as e:
        log.error(e)
        return False


class Base(RequestHandler):

    def http_basic_auth(self, auth_func, realm='Restricted'):
        auth_header = self.request.headers.get('Authorization', None)
        if auth_header is None:
            return False
        else:
            auth_mode, auth_base64 = auth_header.split(' ', 1)
            usr, pwd = base64.b64decode(auth_base64.encode('ascii')).decode('ascii').split(':')
            self.visitor = usr
            return auth_mode == 'Basic' and auth_func(usr, pwd)

    def prepare(self):
        if self.http_basic_auth(check_credentials):
            if "Content-Type" in self.request.headers and self.request.headers["Content-Type"].startswith("application/json"):
                try:
                    self.dic = json_decode(self.request.body) #json.loads(self.request.body)
                    # self.service, self.devices = self.dic['service'], self.dic['devices']
                    self.service, self.trace_id = self.dic['service'], self.dic['trace_id']
                except Exception as e:
                    from traceback import format_exc
                    self.set_status(400)
                    self.finish('Expecting Json data: %s' % format_exc())
        else:
            self.set_status(401)
            self.set_header('WWW-Authenticate', 'Basic realm="%s"' % "Restricted")
            self.finish('Unauthorized Access')
        
        return super(Base, self).prepare()
    
    def resp(self, httpcode, dic):
        self.set_status(httpcode)
        self.set_header('Content-Type', 'application/json; charset=utf-8')
        self.write(json.dumps(dic, ensure_ascii=False, indent=4))
        self.finish()
    
    def on_finish(self):
        return super(Base, self).on_finish()

class BasicAuthHandler(RequestHandler):
    
    def http_basic_auth(self, auth_func, realm='Restricted'):
        auth_header = self.request.headers.get('Authorization', None)
        if auth_header is None:
            return False
        else:
            auth_mode, auth_base64 = auth_header.split(' ', 1)
            usr, pwd = base64.b64decode(auth_base64.encode('ascii')).decode('ascii').split(':')
            self.visitor = usr
            return auth_mode == 'Basic' and auth_func(usr, pwd)

    def prepare(self):
        if not self.http_basic_auth(check_credentials):
            self.set_status(401)
            self.set_header('WWW-Authenticate', 'Basic realm="%s"' % "Restricted")
            self.finish('Unauthorized Access')


from socket import getfqdn
from apscli import gen_wf_template_version, gen_wf_param_dic, APSCLI_USED_CMDLINE_PARAMS
from util.wf_runtime import build_workflow_then_exec

from concurrent.futures import ThreadPoolExecutor
# from multiprocessing import cpu_count
# executor = ThreadPoolExecutor(cpu_count())
executor = ThreadPoolExecutor(max_workers=100)

def _run(fqsn, cmdline_param_dic, trace_id=None):
    try:
        # service_version_add_if_absent(svc['param'])
        return build_workflow_then_exec(
            fqsn,
            # version = svc['param']['version'] if 'version' in svc else None,
            # wf_param = {k:svc['param'][k] for k in svc['param'] if k not in APSCLI_USED_CMDLINE_PARAMS},
            version = gen_wf_template_version(cmdline_param_dic),
            wf_param = gen_wf_param_dic(cmdline_param_dic),
            # run_in_sub_process = False
            trace_id = trace_id
        )
    except Exception as e:
        log.exception('Err when execute: %s in _run()' % fqsn)
        # return {"output":str(e), "return_code":1} # ToDo here: `info` -> `Err_Code` ??
        from traceback import format_exc
        return {
            'fqsn': fqsn,
            'param': cmdline_param_dic,
            'result': {
                'err_code':'apscli_remote_call_exception',
                'exception': format_exc(),
                'return_code': 0
            }, 
            'status': 'exception'
        }

class fqsn(Base):
    @coroutine
    def post(self, action):

        if action == 'run':
            # if getfqdn() in self.devices:
            self.resp(200, (yield executor.submit(_run, self.service['fqsn'], self.service['cmdline_param_dic'], self.trace_id)))
            # else:
            # self.resp(200, {'info': u'target_hostname dont contain this host:%s' % getfqdn(),'code':0})
        else:
            self.resp(200, {'info': u'un_supported fqsn action:%s' % action,'code':0})


class My404Handler(RequestHandler):
    # Override prepare() instead of get() to cover all possible HTTP methods.
    def prepare(self):
        self.set_status(404)
        self.finish()


app = Application([
    (r'/api/fqsn/(run)', fqsn),
], debug=True, default_handler_class=My404Handler)


if __name__ == "__main__": 
    app.listen(8080, address='0.0.0.0')
    loop = tornado.ioloop.IOLoop.current()
    loop.start()
    
