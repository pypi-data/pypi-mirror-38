# encoding=UTF-8

#!/usr/bin/env python 

"""

   NAME
     util.py
 
   DESCRIPTION
     this file contains some import functions to validate, transform and run a workflow.
 
   NOTES
     1. This is a very first version just for the very initial design, so it's likely to change in the near future.
 
   MODIFIED (MM/DD/YY)
   huayang   05/28/18 - initial version 
   huayang   05/31/18 - modification for python convention and headers format suggestions
   huayang   04/06/18 - add make_decision func, modify execute_workflow accordingly
"""

from __future__ import print_function
import sys, json, os
from os.path import isfile, isdir, abspath, split, expandvars, expanduser
from time import time
from six import text_type, binary_type

try:
    from string import Template, _multimap
except ImportError:
    from collections import ChainMap as _multimap


__all__ = ['gen_service_category_dic', 'Workflow', 'register_fqsn', 'unregister_fqsn']


def _get_mapping_from_args(*args, **kws):
    if len(args) > 1:
        raise TypeError('Too many positional arguments')
    if not args:
        mapping = kws
    elif kws:
        mapping = _multimap(kws, args[0])
    else:
        mapping = args[0]             
    return mapping

class MyTemplate(Template):    
    def __init__(self, *args, **kws):        
        super(MyTemplate, self).__init__(*args, **kws)

    def safe_substitute(self, *args, **kws):
        mapping = _get_mapping_from_args(*args, **kws)
        mapping = {k:json.dumps(v) for k,v in mapping.items()}
        return super(MyTemplate, self).safe_substitute(mapping)

    def substitute(self, *args, **kws):
        mapping = _get_mapping_from_args(*args, **kws)
        mapping = {k:json.dumps(v) for k,v in mapping.items()}
        return super(MyTemplate, self).substitute(mapping)


# BASE_PATH = abspath(os.sep.join([os.path.dirname(abspath(__file__)), '..']))
# sys.path.append(BASE_PATH)
# SERVICE_META_REPO_PATH = abspath(os.sep.join([BASE_PATH, '..', 'metadata', '']))
# if not isdir(SERVICE_META_REPO_PATH):
#    os.makedirs(SERVICE_META_REPO_PATH)

from constant import SERVICE_META_REPO_PATH
from JobNode import JobNode
from my_token import calc
from log import myLogger
try:
    from lock import lock_method
    from aps_jobcontrol import read_databag
except ImportError:
    from .lock import lock_method
    from .aps_jobcontrol import read_databag


def gen_service_category_dic(service_meta_repo_path=SERVICE_META_REPO_PATH):
    dic = {
        root:filenames for root,dirs,filenames in os.walk(service_meta_repo_path) if filenames
    }
    service_category_dic = {}
    for root,filenames in dic.items():
        for filename in filter(lambda x: x.endswith('.json'), filenames):
            try:
                with open(root+os.sep+filename, 'r') as f:
                    # key = (root+os.sep+'.'.join(filename.split('.')[0:-1])).replace(SERVICE_META_REPO_PATH,'')
                    key = root.replace(SERVICE_META_REPO_PATH,'').replace(os.sep,'.')+'.'+'.'.join(filename.split('.')[0:-1])
                    key = key.lstrip('.')
                    service_category_dic[key] = json.load(f)
                
                for service_category in service_category_dic:   # remove illegal_service
                    service_dic = service_category_dic[service_category]
                    service_category_dic[service_category] = {
                        service_name:service for service_name,service in service_dic.items() if
                        'workflow_template_path' in service                            and
                        isinstance(service['workflow_template_path'], dict) # and
                        # exists(service['workflow_template_path'])              and
                        # isfile(service['workflow_template_path'])
                    }
                    service_category_dic = {    # remove empty_service_category
                        service_category:service_dic for service_category,service_dic in service_category_dic.items() 
                        if len(service_dic)>0
                    }
            except IOError:
                print('read service_meta_file:{0} failed'.format(root+os.sep+filename))
                raise
            except ValueError:
                print('service_meta_file:{0} is not a valid json file'.format(root+os.sep+filename))
                raise

    return service_category_dic

def gen_fqsn_list(fqsn=None):
    avalible_fqsn_list = []
    for service_category_name, service_dic in gen_service_category_dic().items():
        for service_name in service_dic.keys():
            avalible_fqsn_list.append(service_category_name+'.'+service_name)
    return [x for x in avalible_fqsn_list if x==fqsn] if fqsn is not None else avalible_fqsn_list


class Workflow(object):
    #  prev_nodes, action    ToDo!
    # def __init__(self, fqsn, version=None, wf_param=None, trace_id=None):
    def __init__(self, fqsn, version=None, wf_param=None, trace_id=None, debug=False):
        # assert fqsn.endswith('.template') and isfile(fqsn) or fqsn in gen_fqsn_list(), 'service:{0} does not exist'.format(fqsn)
        assert fqsn in gen_fqsn_list(), 'fqsn:{0} does not exist'.format(fqsn)
        self.name = fqsn
        self.version = version
        # self.wf_param = wf_param
        
        t = str(int(time()*1000000))
        self.id = (trace_id + '.' + t) if trace_id else t
        # self.logger = myLogger(self.name, int(time()*1000000), trace_id)     # 1535000043846496
        self.logger = myLogger(self.name, self.id, debug)
        self._template_path = self._template_path_from_fqsn()       # `/home/suzzy/workflow01.template`
        
        self.decision_expr, self.param = self.gen_jobnodes(wf_param)   # a dict of jobname:JobNodes, which can be run directly
        self.logger.info('\n%s' % self)

    def wf_param_to_dic(self, wf_param):
        if wf_param is None:
            return {}
        elif isinstance(wf_param, dict):
            return wf_param
        elif isinstance(wf_param, (text_type, binary_type)) and isfile(wf_param):
            try:
                with open(wf_param) as f:
                    return json.load(f)
            except IOError:
                self.logger.error('read wf_param_from_file:{0} failed'.format(wf_param))
                raise
            except ValueError:
                self.logger.error('wf_param_file:{0} is not a valid json file'.format(wf_param))
                raise
        elif type(wf_param) is int and wf_param>0:
            try:
                fetch_databag_retcode, databag_list = read_databag(wf_param, 'input')
                if fetch_databag_retcode==0:
                    return databag_list[0]  # maybe empty_dict, which means no_params provided/uploaded from user
                else:
                    self.logger.error('read_databag from JOBID(%s) failed' % wf_param)
                    raise Exception('read_databag from JOBID(%s) failed' % wf_param)
            except:
                raise
        else:
            raise Exception('invalid wf_param:%s' % wf_param)

    def to_dict(self):
        dic = {
            "id": self.id, # ?? need or not_need `id` here?
            # "prev_nodes": self.prev_nodes,
            # "action": self.action
            'name': self.name,
            # 'version': self.version,
            # 'wf_param': self.wf_param
        }
        if hasattr(self, 'start_time'):
            dic['start_time'] = getattr(self, 'start_time')
        if hasattr(self, 'end_time'):
            dic['end_time'] = getattr(self, 'end_time')
        if hasattr(self, 'status'):
            dic['status'] = getattr(self, 'status')
        # if hasattr(self, 'return_code'):
        #    dic['return_code'] = getattr(self, 'return_code')
        if hasattr(self, 'result'):
            dic['result'] = getattr(self, 'result')
        # else:
        dic['param'] = { name: job.to_dict(restore_action=True) for name,job in self.param.items() }
        if hasattr(self, 'decision_expr'):
            dic['decision_expr'] = getattr(self,'decision_expr')
        return dic

    def gen_jobnodes(self, wf_param):
        """
        fetch workflow_template_filepath from fqsn, 
        then read workflow_template_file's content, substitude all $var_name using wf_param_dict, 
        finally build the whole workflow dict(containing all executable JobNodes) from 'json' content
        Args:
        fqsn      (str): oracle.peo.db.add_datafile
        wf_param  (JOBID-int | wf_param_filepath-str,bytes,unicode | dict)
        Returns:
            dict<str,JobNode>: e.g. - { 'name1':JobNode1, 'name2':JobNode2, 'name3':JobNode3, 'name4':JobNode4 }
        Raises:
            Exception: IOError, KeyError, ValueError, AssertionError
        """
        wf_param = self.wf_param_to_dic(wf_param)   # prepare workflow's param_dict first
        expand = lambda x: expanduser(expandvars(x))
        # gen workflow from workflow_template & wf_param
        wf_content = ''
        try:
            with open(self._template_path) as f:
                wf_template = MyTemplate(expand(f.read()))
                wf_content = wf_template.substitute(** wf_param)
        except IOError:
            self.logger.error('read workflow_template_filepath:{0} failed'.format(self._template_path))
            raise
        except KeyError:
            self.logger.error('Not enough wf_params provided from wf_param_dic:{0}'.format(wf_param))
            raise

        '''
         try:
            with open(self._template_path) as f:
                wf_template = MyTemplate(expand(f.read()))
                while True:     # 将模板中定义的每个参数(如果其没有在运行时提供参数值，一律使用默认参数值''进行替换)
                    try:
                        wf_content = wf_template.substitute(** wf_param)
                        break
                    except KeyError as e:
                        # self.logger.error('Not enough wf_params provided from wf_param_dic:{0}'.format(wf_param))
                        self.logger.warning('Not enough wf_params provided from wf_param_dic:{0}, missing `{1}'.format(wf_param, e[0]))
                        wf_param[e[0]] = 0 if e[0]=='JOBID' else ''
                        # raise
        except IOError:
            self.logger.error('read workflow_template_filepath:{0} failed'.format(self._template_path))
            raise
        '''    
        # self.logger.info(wf_content)

        # after validation, convert workflow to dict
        jobname = ''
        try:
            dic = json.loads(wf_content)    # type='json'

            if 'param' in dic:
                if 'decision_expr' in dic:
                    from my_token import find_var
                    assert isinstance(dic['decision_expr'], (text_type, binary_type)) and \
                           len(dic['decision_expr'].strip()) > 0 and \
                           find_var(dic['decision_expr']).issubset(set(dic['param'].keys())), \
                           'invalid workflow_decision_expr(%s)' % dic['decision_expr']
                    decision_expr = dic['decision_expr']
                else:
                    # decision_expr = ' && '.join(dic['param'].keys()) a ==1 && b c d
                    decision_expr = ''.join([''.join(l) for l in zip(dic['param'].keys(), [' ==1 && ']*len(dic['param']) )])
                dic = dic['param']
            else:   # dic only contains a list of jobnodes
                assert 'decision_expr' not in dic, '`dicision_expr should exist together with `param'
                # decision_expr = ' && '.join(dic.keys())
                decision_expr = ' && '.join([''.join(l) for l in zip(dic.keys(), [' ==1 ']*len(dic) )])

            jobnames, jobs = dic.keys(), dic.values()
            assert len(dic)>0 and any([len(job['prev_nodes'])==0 for job in jobs]),    \
                "workflow is empty, or all JobNode's prev_nodes are not empty"
            assert all([set(job['prev_nodes']).issubset(jobnames) for job in jobs]) and \
                all([ jobname not in job['prev_nodes'] for jobname,job in dic.items() ]), \
                "at least one JobNode's prev_nodes is invalid"
            # ToDo: maybe need more workflow_content validation here?
            param = {
                jobname: JobNode.from_dict( dict(name=jobname, wf_id=self.id, **job_dic) ) for jobname,job_dic in dic.items()
            }
            return decision_expr, param
        except ValueError:
            self.logger.error('workflow`s content is not a valid json string\n{0}'.format(wf_content))
            raise
        except KeyError as e:
            self.logger.error('JobNode:({0}) missing attribute:"{1}"'.format(jobname, e[0]))
            raise

    def _template_path_from_fqsn(self):
        """
        fetch workflow_template_filepath from a service.category.json file using fqsn(e.g. 'oracle.peo.db.inst_restart')
        Args:
        fqsn (str): Fully_Qualified_Service_Name, e.g. oracle.peo.db.inst_restart
        Returns:
            workflow_template_filepath  (str): e.g. /u01/SRE/SELF_SERVICE/db/inst_restart.template
        Raises:
            Exception: IOError, ValueError, KeyError
        """
        try:
            l = [SERVICE_META_REPO_PATH]
            l.extend(self.name.split('.')[0:-2])
            service_meta_json_filepath = os.sep.join(l) + os.sep   # fqsn.split(os.sep)[0:-1]
            service_meta_json_filename = self.name.split('.')[-2] + '.json' # '.'.join(fqsn.split(os.sep)[-1].split('.')[0:-1]) + '.json'
            service_name = self.name.split('.')[-1]                         # fqsn.split(os.sep)[-1].split('.')[-1]
            with open(service_meta_json_filepath + service_meta_json_filename) as f:
                service_dic = json.load(f)
                if self.version is None:
                    if 'version' in service_dic[service_name]:
                        if len(service_dic[service_name]['workflow_template_path'])==1:
                            self.version = service_dic[service_name]['workflow_template_path'].keys()[0]
                        else:
                            self.version = service_dic[service_name]['version']
                    else:
                        assert len(service_dic[service_name]['workflow_template_path'])==1, \
                            'There are multiple workflow_template_path, which one should I choose?'
                        self.version = service_dic[service_name]['workflow_template_path'].keys()[0]
                        
                        print(self.version)
                wf_template_path = service_dic[service_name]['workflow_template_path'][self.version]
                assert isfile(wf_template_path), 'illegal wf_template_path:{0} fetched from {1}'.format(wf_template_path, self.name)
                self.logger.debug('wf_template_filepath: `%s' % wf_template_path)
                # if self.name.endswith('.template') wf_template_path = self.name 
                return wf_template_path
        except IndexError:
            self.logger.error('illegal Fully_Qualified_Service_Name given:{0}'.format(self.name))
            raise
        except IOError:
            self.logger.error('read service_meta_json_file:{0} failed'.format(service_meta_json_filepath+service_meta_json_filename))
            raise
        except ValueError:
            self.logger.error('service_meta_json_file:{0} is not a valid json file'.format(service_meta_json_filepath+service_meta_json_filename))
            raise
        except KeyError as e:
            if e[0] == 'workflow_template_path':
                self.logger.error('service:{0} does not contain workflow_template_path'.format(self.name))
            elif e[0] == 'version':
                self.logger.error('service:{0} does not contain item:`version`'.format(self.name))
            elif e[0] == self.version:
                self.logger.error('service:{0}, version:`{1}` does not registered'.format(self.name, self.version))
            else:
                self.logger.error('service:{0} does not exist in service_meta_json_file:{1}'.format(self.name, service_meta_json_filepath+service_meta_json_filename))
            raise

    def __str__(self):
        """
        To serilize a Workflow instance to a str.
        We can save a Workflow instance into DB/File, then load it using json.loads() method.
        """
        # return str(self.to_dict())
        return json.dumps(self.to_dict(), sort_keys=True, indent=4)
            
    def __repr__(self):
        return self.__str__()


def _mk_cascade_dirs(starting, cascade_dirs, stop_on_file_exists_err=True):
    assert isdir(starting), 'starting_path:%s is not a valid directory' % starting
    assert isinstance(cascade_dirs, (list,tuple)) and len(cascade_dirs)>0 and all([dir for dir in cascade_dirs]),   \
           'cascade_dirs:%s Must be a list/tuple of dir names' % cascade_dirs
    l = [starting]
    l.extend(cascade_dirs)
    for i in range(2, len(l)+1):
        try:
            os.mkdir(os.path.join(*l[0:i]))
        except OSError as e:
            if e[1] == 'File exists':
                if stop_on_file_exists_err:
                    raise e
                else:
                    pass
            else:
                raise e

# def register_fqsn(fqsn, wf_template, new_service_provider=False, new_service_category=False, desc=None, version=None):
def register_fqsn(fqsn, wf_template, desc=None, version=None, default_version=None):
    path = os.sep.join(fqsn.split('.')[0:-2])
    abs_path = os.path.join(SERVICE_META_REPO_PATH, path)
    service_category_json_file, service_name = fqsn.split('.')[-2:]
    service_category_json_file = os.sep.join([SERVICE_META_REPO_PATH, path, service_category_json_file+'.json'])
    if not isdir(abs_path):
        _mk_cascade_dirs(SERVICE_META_REPO_PATH, path.split(os.sep), stop_on_file_exists_err=False)
                
    @lock_method(lock_filename = service_category_json_file[:-4] + 'lock')
    def _register_smooth(version, default_version):
        assert isfile(wf_template), '`workflow_template_file:{0} does not exist'.format(wf_template)
        try:
            '''
            if not isdir(abs_path):
                _mk_cascade_dirs(SERVICE_META_REPO_PATH, path.split(os.sep), stop_on_file_exists_err=False)
                f = open(service_category_json_file, 'w')
                f.write('{}')
                f.close()
            '''
            if not isfile(service_category_json_file):
                f = open(service_category_json_file, 'w')
                f.write('{}')
                f.close()

            with open(service_category_json_file) as f:
                dic = json.loads( f.read() )
            if service_name in dic:         # register new service_version | override existing service_version for existing service
                assert version, '`Must provide service_template_file version'
                dic[service_name]['workflow_template_path'][version] = wf_template
                if default_version:
                    dic[service_name]['version'] = default_version
            else:                   # register a new service
                if version and default_version:
                    assert version == default_version, '`version` has to == `default_version` when register a new service'
                elif version:
                    default_version = version
                elif default_version:
                    version = default_version
                else:
                    version = default_version = 'default'
                dic[service_name] = {
                    'workflow_template_path':{
                        version: wf_template
                    },
                    'version': default_version
                }
            if desc:
                dic[service_name]['desc'] = desc

            with open(service_category_json_file, 'w') as f:
                f.write(
                    json.dumps(dic, sort_keys=True, indent=4)
                )
        except ValueError:
            print('service_category_json_file:{0} is not a valid json file'.format(service_category_json_file))
            raise            
        except IOError:
            print('write service_category_json_file:{0} when register service:{1} failed'.format(service_category_json_file, fqsn))
            raise
        print('register fqsn:{0} successful'.format(fqsn))

    _register_smooth(version, default_version)

    '''
    @lock_method(lock_filename = service_category_json_file[:-4] + 'lock')
    def _register(version):
        try:
            if new_service_provider:
                assert not isdir(abs_path), 'service_provider`s directory:{0} already exists'.format(abs_path)
                _mk_cascade_dirs(SERVICE_META_REPO_PATH, path.split(os.sep), stop_on_file_exists_err=False)
                f = open(service_category_json_file, 'w')
                f.write('{}')
                f.close()
            else:
                assert isdir(abs_path), 'service_provider`s directory:{0} does not exists'.format(abs_path)
                if new_service_category:
                    assert not isfile(service_category_json_file), 'service_category_json_file:{0} already exists'.format(service_category_json_file)
                    f = open(service_category_json_file, 'w')
                    f.write('{}')
                    f.close()
                else:
                    assert isfile(service_category_json_file), 'service_category_json_file:{0} does not exists'.format(service_category_json_file)

            assert isfile(wf_template), '`workflow_template_file:{0} does not exist'.format(wf_template)

            with open(service_category_json_file, 'r') as f:
                dic = json.loads( f.read() )
            if service_name in dic:         # register new service_version for existing service
                assert version, '`Must provide --version from cmd_line'
                dic[service_name]['workflow_template_path'][version] = wf_template
                dic[service_name]['version'] = version
            else:                   # register a new service
                version = version if version else 'default'
                dic[service_name] = {
                    'workflow_template_path':{
                        version: wf_template
                    },
                    'version': version if version else 'default'
                }
            if desc:
                dic[service_name]['desc'] = desc

            with open(service_category_json_file, 'w') as f:
                f.write(
                    json.dumps(dic, sort_keys=True, indent=4)
                )
        except ValueError:
            print('service_meta_json_file:{0} is not a valid json file'.format(service_category_json_file))
            raise            
        except IOError:
            print('write service_meta_json_file:{0} when register service:{1} failed'.format(service_category_json_file, fqsn))
            raise
        print('register fqsn:{0} successful'.format(fqsn))

    _register(version)
    '''

def unregister_fqsn(fqsn, version=None, default_version=None):
    path = os.sep.join(fqsn.split('.')[0:-2])
    service_category_json_file, service_name = fqsn.split('.')[-2:]
    service_category_json_file = os.sep.join([SERVICE_META_REPO_PATH, path, service_category_json_file+'.json'])
    
    @lock_method(lock_filename = service_category_json_file[:-4] + 'lock')
    def _unregister():
        try:
            assert isfile(service_category_json_file), 'service_category_json_file:{0} does not exists'.format(service_category_json_file)
            with open(service_category_json_file, 'r') as f:
                dic = json.loads( f.read() )
            
            assert service_name in dic, 'simple_service_name:{0} does not exist in {1}'.format(service_name, service_category_json_file)
            if version:
                version_dic = dic[service_name]['workflow_template_path']
                assert version in version_dic, 'service_version:{0} for fqsn:{1} does not exist in {2}'.format(version, fqsn, service_category_json_file)
                
                versions = version_dic.keys()
                versions.remove(version)
                if len(version_dic) == 1:
                    del dic[service_name]
                elif len(version_dic) == 2:
                    del version_dic[version]
                    dic[service_name]['version'] = versions[0]
                else:
                    assert default_version, 'Must specify correct `default_version as there would be at least two versions remain after unregister'
                    assert default_version in versions, 'default_version:{0} must exist in {1}'.format(default_version, versions)
                    del version_dic[version]
                    dic[service_name]['version'] = default_version
            else:
                del dic[service_name]

            with open(service_category_json_file, 'w') as f:
                f.write(
                    json.dumps(dic, sort_keys=True, indent=4)
                )
        except ValueError:
            print('service_meta_json_file:{0} is not a valid json file'.format(service_category_json_file))
            raise            
        except IOError:
            print('write service_meta_json_file:{0} when register service:{1} failed'.format(service_category_json_file, fqsn))
            raise
        print('unregister fqsn:{0} successful'.format(fqsn))

    _unregister()