#!/u01/SRE/PYTHON_BASE/python/bin/python
# encoding=utf-8


"""
 
   NAME
     apscli.py
 
   DESCRIPTION
     this file is a simple demo, just to show how the workflow engine works. There are two user defined workflow files(
   workflow01.json and workflow02.json) at the same directory.  The demo starts and run the two workflows one by one.
 
   NOTES
     1. Console output for each workflow contains three parts:
       a. a list of JobNode each converted from a Python dict
       b. topo_sorted_result for a.
       c. executing_result for a.
 
   MODIFIED (MM/DD/YY)
   huayang   05/28/18 - initial version 
   huayang   05/31/18 - modification to fit python convention and headers format suggestions
"""

import json, sys, os, re, argparse
from os.path import dirname, abspath, exists, join, isfile

class MyArgParser(argparse.ArgumentParser):
    def _get_option_tuples(self, option_string):
        result = []

        # option strings starting with two prefix characters are only
        # split at the '='
        chars = self.prefix_chars
        if option_string[0] in chars and option_string[1] in chars:
            if '=' in option_string:
                option_prefix, explicit_arg = option_string.split('=', 1)
            else:
                option_prefix = option_string
                explicit_arg = None
            for option_string in self._option_string_actions:
                if option_string == option_prefix:
                    action = self._option_string_actions[option_string]
                    tup = action, option_string, explicit_arg
                    result.append(tup)

        # single character options can be concatenated with their arguments
        # but multiple character options always have to have their argument
        # separate
        elif option_string[0] in chars and option_string[1] not in chars:
            option_prefix = option_string
            explicit_arg = None
            short_option_prefix = option_string[:2]
            short_explicit_arg = option_string[2:]

            for option_string in self._option_string_actions:
                if option_string == short_option_prefix:
                    action = self._option_string_actions[option_string]
                    tup = action, option_string, short_explicit_arg
                    result.append(tup)
                elif option_string == option_prefix:
                    action = self._option_string_actions[option_string]
                    tup = action, option_string, explicit_arg
                    result.append(tup)

        # shouldn't ever get here
        else:
            self.error(_('unexpected option string: %s') % option_string)

        # return the collected option tuples
        return result

from constant import CONF_DIR, SERVICE_VERSION_CALCULATE_PATH
#BASE_PATH = dirname(abspath(__file__))
#SERVICE_VERSION_CALCULATE_PATH = abspath(os.sep.join([BASE_PATH, 'plugins', 'service_version_calculate', '']))
#LOG_DIR = os.sep.join([BASE_PATH, '..', 'logs', ''])
#if not exists(LOG_DIR):
#    os.makedirs(LOG_DIR)

# read .ini config 
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser

cf = ConfigParser()
cf.read(
    os.sep.join([abspath(CONF_DIR), 'apscli.ini'])
)

APSCLI_USED_CMDLINE_PARAMS = ('action', 'fqsn', 'version', 'ver_calc', 'debug', 'EM', 'wp', 'JOBID')

from util import aps_jobcontrol
from logging import DEBUG, getLogger
from log import file_handler
from JobNode import JobNode
# from log import myLogger

log = getLogger(__name__)
log.setLevel(DEBUG)
log.addHandler(file_handler)

def _all_service_version_calculate_scripts():
    return [x for x in os.listdir(SERVICE_VERSION_CALCULATE_PATH) if isfile(join(SERVICE_VERSION_CALCULATE_PATH,x))]


def gen_wf_template_version(cmdline_param_dic):
    from collections import Hashable
    if 'version' in cmdline_param_dic and cmdline_param_dic['version'] is not None and isinstance(cmdline_param_dic['version'], Hashable):
        version = cmdline_param_dic['version']
    elif 'ver_calc' in cmdline_param_dic and cmdline_param_dic['ver_calc'] in _all_service_version_calculate_scripts():
        from util.wf_runtime import _run_cmd_in_thread
        jobnode = JobNode.from_dict(
            {   # "id": 1,
                "wf_id": None,
                "name": "",
                "prev_nodes": [],
                "action": {
                    "type": "cmd",                                                    
                    "cmd": join(SERVICE_VERSION_CALCULATE_PATH, cmdline_param_dic['ver_calc']),
                    "env": {}
                },
                "param": {k:v for k,v in cmdline_param_dic.items() if k in ('fqsn',) or k not in APSCLI_USED_CMDLINE_PARAMS}
            })
        _run_cmd_in_thread(jobnode, real_time_print=False)
        jobnode = jobnode.to_dict()
        assert set(['status','result']) & set(jobnode.keys()) and \
            jobnode['status'] == 'success'                and \
            'output' in jobnode['result']                 and \
            jobnode['result']['output'], 'got invalid service_version after calculate'
        version = jobnode['result']['output']
        del cmdline_param_dic['ver_calc']
        log.info('service_version was set to:%s after calculate' % version)
        #from util.op_control import version_from_pod_name_using_sra_master_config
        #version_from_pod_name_using_sra_master_config(cmdline_param_dic)
    else:
        version = None
    return version


def gen_wf_param_dic(cmdline_param_dic):
    assert isinstance(cmdline_param_dic, dict), 'cmdline_param_dic should be a dict'
    assert 'wp' in cmdline_param_dic or 'JOBID' in cmdline_param_dic or 'EM' in cmdline_param_dic, 'need one from `wp / JOBID / EM'
    if 'wp' in cmdline_param_dic and cmdline_param_dic['wp']:
        wp = cmdline_param_dic['wp']
        from six import text_type, binary_type
        assert isinstance(wp, (text_type, binary_type)) and isfile(wp), 'wf_param should be a valid local_file_path'
        try:
            with open(wp) as f:
                return json.load(f)
        except IOError:
            log.error('read wf_param_from_file:{0} failed'.format(wp))
            raise
        except ValueError:
            log.error('wf_param_file:{0} is not a valid json file'.format(wp))
            raise
    elif 'JOBID' in cmdline_param_dic and cmdline_param_dic['JOBID']:
        JOBID = cmdline_param_dic['JOBID']
        assert type(JOBID) is int and JOBID>0, 'JOBID should be a valid JobControl JOBID'
        try:
            fetch_databag_retcode, databag_list = aps_jobcontrol.read_databag(JOBID, 'input')
            if fetch_databag_retcode==0:
                log.debug('databag_list[0] is:%s' % databag_list[0])
                databag = databag_list[0]  # maybe empty_dict, which means no_params provided/uploaded from user
                return dict(
                    # databag.items() + (jc_param.items() if isinstance(jc_param,dict) else [])
                    databag.items() + {k:v for k,v in cmdline_param_dic.items() if (k in ('JOBID',) or k not in APSCLI_USED_CMDLINE_PARAMS) and v is not None}.items()
                )
            else:
                log.error('read_databag from JOBID(%s) failed' % JOBID)
                raise Exception('read_databag from JOBID(%s) failed' % JOBID)
        except:
            raise
    elif 'EM' in cmdline_param_dic and cmdline_param_dic['EM']:
        EM = cmdline_param_dic['EM']
        return {k:v for k,v in cmdline_param_dic.items() if k not in APSCLI_USED_CMDLINE_PARAMS and v is not None}
    else: 
        return {k:v for k,v in cmdline_param_dic.items() if k not in APSCLI_USED_CMDLINE_PARAMS and v is not None}


def run():
    parent_parser = argparse.ArgumentParser(add_help=False)   
    parent_parser.add_argument('--debug', default=False, required=False, action='store_true', dest="debug", help='debug flag')
    # parent_parser.add_argument('--user', '-u', default=getpass.getuser(), help='username')                                                                                                                     

    p = MyArgParser()
    action_subparsers = p.add_subparsers(title="action", dest="action") 

    register_parser = action_subparsers.add_parser("register", help="regiester a service template", parents=[parent_parser])
    register_parser.add_argument('--fqsn', type=str, required=True, help='Fully Qualified Service Name')
    register_parser.add_argument('--wf_template', type=str, required=True, help='workflow_template_path')
    register_parser.add_argument('--desc', type=str, required=False, help='workflow_template usage description')
    register_parser.add_argument('--version', type=str, required=False, help='service_version')
    register_parser.add_argument('--default_version', type=str, required=False, help='default service_version')
    # register_parser.add_argument('--new_service_provider', action='store_true', default=False, help='new_service_provider')
    # register_parser.add_argument('--new_service_category', action='store_true', default=False, help='new_service_category')

    unregister_parser = action_subparsers.add_parser("unregister", help="unregiester a service template", parents=[parent_parser])
    unregister_parser.add_argument('--fqsn', type=str, required=True, help='Fully Qualified Service Name')
    unregister_parser.add_argument('--version', type=str, required=False, help='service_version')
    unregister_parser.add_argument('--default_version', type=str, required=False, help='default_service_version after unregister')

    list_parser = action_subparsers.add_parser("list", help="list a service template", parents=[parent_parser])
    list_parser.add_argument('--fqsn', type=str, required=False, help='Fully Qualified Service Name')
    # list_parser.add_argument('--version', type=str, required=False, help='service_version')

    run_parser = action_subparsers.add_parser("run", help="run a service template", parents=[parent_parser])
    run_parser.add_argument('--fqsn', type=str, required=True, help='Fully Qualified Service Name')
    # run_parser.add_argument('--version', type=str, required=False, help='service_version')
    
    exclusive_version_grp = run_parser.add_mutually_exclusive_group()
    exclusive_version_grp.add_argument('--version', type=str, help='service_version')
    exclusive_version_grp.add_argument('--ver_calc', type=str, help='service_version_calculate_script')

    exclusive_caller_grp = run_parser.add_mutually_exclusive_group()
    exclusive_caller_grp.add_argument('--wp', type=str, help='Apscli will fetch wf_params from a specified local json_file')
    exclusive_caller_grp.add_argument('--JOBID', type=int, help='Apscli will fetch wf_params from JobControl input_databag uploaded from user')
    exclusive_caller_grp.add_argument('--EM', action='store_true', help='Apscli will fetch wf_params from cmd_line_params provided by user')

    parsed, unknown_list = p.parse_known_args()
    log.debug('parsed_args:%s' % parsed)
    log.debug('unknown_args_list:%s' % unknown_list)
    unknown_kv_dic = {}
    # unknown_switch_list = []

    def _arg_name(item):
        return item.startswith("-")  and len(item)==2 and item[1]!="-" or item.startswith("--") and len(item)>2
    def _arg_value(item):
        return not item.startswith("-")

    for (idx, item) in enumerate(unknown_list):
        if _arg_name(item):
            #if item[1:] in ('J',) or len(item)>2 and item[2:] in ('JOBID','wp'):
            #    _prompt()
            #    sys.exit(1)
            #else:
            if idx < len(unknown_list)-1 and _arg_value(unknown_list[idx+1]):
                    unknown_kv_dic[ item.lstrip('-').lstrip('--') ] = unknown_list[idx+1]
            else:
                # unknown_switch_list.append(item)
                _prompt()
                sys.exit(1)
        else:
            pass

    cmdline_param_dic = dict(parsed._get_kwargs() + list(unknown_kv_dic.items()))
    log.debug(cmdline_param_dic)

    action, fqsn, debug_flag = cmdline_param_dic['action'], cmdline_param_dic['fqsn'], cmdline_param_dic['debug']

    if action=='run':
        from util.wf_runtime import build_workflow_then_exec
        try:
            wf = build_workflow_then_exec(
                fqsn, 
                version = gen_wf_template_version(cmdline_param_dic),
                wf_param = gen_wf_param_dic(cmdline_param_dic),
                debug = debug_flag,
            )
            
            jobnodes_not_success = [
                node for jobname,node in wf['param'].items() if 'result' in node and node['status'] in ('failure','exception')
            ]
            if cmdline_param_dic['JOBID'] and jobnodes_not_success:
                aps_jobcontrol.write_output_databag(cmdline_param_dic['JOBID'],
                    {
                        'Error_Message':{
                            node['name']: {
                                "Error_Code":node['result'].get('err_code', 'N/A'), 
                                "Error_Msg":node['result'].get('err_msg', 'N/A')
                            } for node in jobnodes_not_success
                        }
                    }
                )
            sys.exit(wf['result']['return_code'] ^ 1)                    
        except:
            raise
    elif action=='register':
        from util.wf_build import register_fqsn 
        register_fqsn(
            fqsn, 
            cmdline_param_dic['wf_template'], 
            desc=cmdline_param_dic['desc'],
            version=cmdline_param_dic['version'],
            default_version=cmdline_param_dic['default_version']
        )
    elif action=='unregister':
        from util.wf_build import unregister_fqsn
        unregister_fqsn(
            fqsn, 
            version=cmdline_param_dic['version'],
            default_version=cmdline_param_dic['default_version']
        )
    elif action=='list':
        from util.wf_build import gen_service_category_dic
        avalible_service_list = []
        for service_category_name, service_dic in sorted(gen_service_category_dic().items()):
            avalible_service_list.extend(
                [
                    ('%-50s' % (service_category_name+'.'+service_name)) + 
                    ('%-80s' % service_dic[service_name]['workflow_template_path'][version]) + 
                    ('%-10s' % version) +
                    ('%-2s' % '<-' if ('version' in service_dic[service_name] and service_dic[service_name]['version']==version or 'version' not in service_dic[service_name] or len(service_dic[service_name]['workflow_template_path'])==1) else '') + os.linesep+'-'*150
                    # ('%-10s' % str(service_dic[service_name].get('version','N/A')))
                    # '\n' + service_dic[service_name]['desc']
                    for service_name in service_dic.keys() 
                    for version in service_dic[service_name]['workflow_template_path']
                    if isinstance(service_dic[service_name]['workflow_template_path'], dict)
                ]
            )
        if fqsn:
            avalible_service_list = [x for x in avalible_service_list if fqsn==re.split('\s+',x)[0]]
        # _prompt()
        print('All Available Services:\n'+'-'*150)
        print(('%-50s' % 'Fully_Qualified_Service_Name') + ('%-80s' % 'Service_Template') + ('%-10s' % 'Version') +  ('%-10s' % 'Default') + os.linesep)
        print('-'*150)
        print(os.linesep.join(avalible_service_list)+os.linesep)
    else:
        pass
    # args = p.parse_args()
    # #jobid_list = sorted(list(set(args.jobid.split(','))))
    # #verbose = args.verbose
    # DEBUG = args.debug
    # print(args)


def _prompt():
    prompt_msg = '''\nApscli support 4 sub-commands:\n
1) ./apscli.py register            regiester a service template
2) ./apscli.py unregister          unregiester a service template
3) ./apscli.py list                list available service template
4) ./apscli.py run                 run a specified service template by fqsn

For each sub-command, use `./apscli.py [sub-command] -h` for Usage

Cmd_line parameters: `%s are kept for internal use by Apscli, pls don't use them as user_script's parameters(except `JOBID).
\n\n''' % ','.join(APSCLI_USED_CMDLINE_PARAMS)
    print(prompt_msg)


if __name__ == '__main__':
#    # no workflow_param provided
#    condition1 = len(sys.argv)==3 and sys.argv[1] == '--wt' or \
#                 len(sys.argv)==4 and sys.argv[1] == '--wt' and sys.argv[3] == '--po', \
#                 '--wt [template_path] is required, --po is optional' 
#    # workflow_param provided thru local_param_file
#    condition2 = len(sys.argv)==6 and sys.argv[1] == '--wt' and sys.argv[3] == '--wp' and sys.argv[4] in ('--version',) or \
#                 len(sys.argv)==7 and sys.argv[1] == '--wt' and sys.argv[3] == '--wp' and sys.argv[5] in ('--version',) and sys.argv[6] == '--po', \
#                 '--wt [template_path] is required, --wp [wf_param] is required, --po is optional'
#    # workflow_param provided thru JC --JOBID <JOBID>
#    condition3 = len(sys.argv)>=5 and sys.argv[1] == '--wt' and sys.argv[3]  == '--JOBID' or \
#                 len(sys.argv)>=6 and sys.argv[1] == '--wt' and sys.argv[3]  == '--JOBID' and sys.argv[5] == '--po', \
#                 '--wt [template_path] is required, --JOBID [JOBID] is required, --po is optional'
#    # workflow_param provided thru EM --EM
#    condition4 = len(sys.argv)>=4 and sys.argv[1] == '--wt' and sys.argv[3]== '--EM' or \
#                 len(sys.argv)>=5 and sys.argv[1] == '--wt' and sys.argv[3]== '--EM' and sys.argv[4] == '--po', \
#                 '--wt [template_path] is required, -EM is required, --po is optional'
#
#    # no workflow_param provided
#    fqsn_condition1 = len(sys.argv)==3 and sys.argv[1] == '--fqsn' or \
#                      len(sys.argv)==4 and sys.argv[1] == '--fqsn' and sys.argv[3] == '--po',  \
#                      '--fqsn [fully qualified service name] is required, --po is optional'
#    # workflow_param provided thru local_param_file
#    fqsn_condition2 = len(sys.argv)>=5 and sys.argv[1] == '--fqsn' and sys.argv[3] == '--wp' or \
#                      len(sys.argv)>=6 and sys.argv[1] == '--fqsn' and sys.argv[3] == '--wp' and sys.argv[5] in ('--po', '--version'),  \
#                      '--fqsn [fully qualified service name] is required, --wp [wf_param] is required, --po is optional'
#    # workflow_param provided thru JC --JOBID <JOBID>
#    fqsn_condition3 = len(sys.argv)>=5 and sys.argv[1] == '--fqsn' and sys.argv[3]  == '--JOBID' or \
#                      len(sys.argv)>=6 and sys.argv[1] == '--fqsn' and sys.argv[3]  == '--JOBID' and sys.argv[5] == '--po',  \
#                      '--fqsn [fully qualified service name] is required, --JOBID [JOBID] is required, --po is optional'
#    # workflow_param provided thru JC --JOBID <JOBID>
#    fqsn_condition4 = len(sys.argv)>=4 and sys.argv[1] == '--fqsn' and sys.argv[3]== '--EM' or \
#                      len(sys.argv)>=5 and sys.argv[1] == '--fqsn' and sys.argv[3]== '--EM' and sys.argv[5] == '--po',  \
#                      '--fqsn [fully qualified service name] is required, --EM is required, --po is optional'
#    
#
#    condition0 = ( len(sys.argv)==2 and sys.argv[1] in ('-h','--help'), '' )
#    if not (condition0[0] or condition1[0] or condition2[0] or condition3[0] or condition4[0] or fqsn_condition1[0] or fqsn_condition2[0] or fqsn_condition3[0] or fqsn_condition4[0]):
#        _prompt()
#        sys.exit(1)
#    
#    if condition0[0]:
#        avalible_service_list = []
#        for service_category_name, service_dic in sorted(gen_service_category_dic().items()):
#            avalible_service_list.extend(
#                [
#                    ('%-50s' % (service_category_name+'.'+service_name)) + 
#                    ('%-80s' % service_dic[service_name]['workflow_template_path'][version]) + 
#                    ('%-10s' % version)
#                    # ('%-10s' % str(service_dic[service_name].get('version','N/A')))
#                    # '\n' + service_dic[service_name]['desc']
#                    for service_name in service_dic.keys() 
#                    for version in service_dic[service_name]['workflow_template_path']
#                    if isinstance(service_dic[service_name]['workflow_template_path'], dict)
#                ]
#            )
#        _prompt()
#        print('All Available Services:\n'+'-'*150)
#        print(('%-50s' % 'Fully_Qualified_Service_Name') + ('%-80s' % 'Service_Template') + ('%-10s' % 'Version') + '\n')
#        print('-'*150)
#        print('\n'.join(avalible_service_list)+'\n')
#    elif condition1[0] or condition2[0]:
#        run_from_file()
#    elif condition3[0]:
#        run_from_jobid()
#    elif condition4[0]:
#        run_from_em_agent()
#    elif fqsn_condition1[0] or fqsn_condition2[0]:
#        run_from_file(wt='fqsn')
#    elif fqsn_condition3[0]:
#        run_from_jobid(wt='fqsn')
#    else:
#        run_from_em_agent(wt='fqsn')
    run()