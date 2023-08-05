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
import sys
import os
import time
import json
import glob
import shlex
import socket
import traceback
import threading
import subprocess

from six import text_type, binary_type

from multiprocessing import Queue
try:
    from Queue import Empty
except ImportError:
    from queue import Empty


# BASE_PATH = os.path.abspath(os.sep.join([os.path.dirname(os.path.abspath(__file__)), '..']))
# sys.path.append(BASE_PATH)
from JobNode import JobNode
from my_token import calc
from Xprocess import TIME_FORMAT, Xprocess
from log import console
try:
    from wf_build import Workflow
except ImportError:
    from .wf_build import Workflow


__all__ = ['build_workflow_then_exec']


def topo_sort(job_list):
    """
    Classical topo_sort algorithm for DAG
    Args:
        job_list    (list[JobNode]): list of JobNode
    Returns:
        list[list[JobNode]]: for example - [ [JobNode1,JobNode2], [JobNode3], [JobNode4,JobNode5] ]
    Raises:
        Exception: N/A
    """

    result = []

    while len(job_list) > 0:
        each_round_selected_jobs = [ job for job in job_list if len(job.prev_nodes_copy)==0 ]
        result.append(each_round_selected_jobs)
        
        each_round_selected_names = [job.name for job in each_round_selected_jobs]
        job_list = [job for job in job_list if job.name not in each_round_selected_names]

        for name in each_round_selected_names:
            for job in job_list:
                if name in job.prev_nodes_copy:
                    job.prev_nodes_copy.remove(name)
                    
    return result


def import_module(import_str): 
    """dynamic import a module. 
    """ 
    __import__(import_str) 
    return sys.modules[import_str] 

'''
主线程在make_decision时,
如因identifier不存在 / 或其属性不存在而运行抛异常退出，
退出前已经fork出来正在运行中的子进程/子线程，
因为其默认daemon=False，
所以仍能在前台正常运行直到运行正常结束？

主线程在为topo排序的下一轮的每个Node执行make_decision时，
上一轮topo排序的每个Node都已经执行完毕了，所以不存在这个担心。
'''

def make_decision(jobnode, workflow):
    """
    decide whether a JobNode should be started according to user_defined 'decision_expr' at run time
    Args:
    jobnode    (JobNode): a JobNode instance
    workflow   (dict): for example - { 'name1':JobNode1, 'name2':JobNode2, 'name3':JobNode3, 'name4':JobNode4 }
    Returns:
        bool - a jobnode's decision_expr evaluation result
    Raises:
        Exception: ValueError, my_token.TokenError
    """
    if not hasattr(jobnode, 'decision_expr'):
        return True
    else:
        #for prev in jobnode.prev_nodes:
        #    if not hasattr(workflow[prev], 'result'):
        #        workflow[prev].result = {'return_code': 'N/A'}
        context = {
            prev: workflow[prev].result['return_code'] for prev in jobnode.prev_nodes
        }
        try:
            should_I_start = calc(jobnode.decision_expr, context)
        except AssertionError:  # at least one of prev_nodes's doesn't start(return_code=='N/A') while need it's return_code to calc the decision_expr
            should_I_start = False
        if not should_I_start:
            jobnode.result = {'return_code': 'N/A'} 
        return should_I_start


def _cmd_result_to_dic(result):
    # (exit_code, stdout_str)
    ret = {
        'return_code': result[0] ^ 1
    }
    stdout_list = [line for line in result[1].split(b'\n') if len(line.strip())>0]
    output =   b'\n'.join([line[8:] for line in stdout_list if line.startswith(b'[OUTPUT]')])
    # stderr_list = [line for line in result[1][1].split('\n') if len(line.strip())>0]
    err_msg =  b'\n'.join([line[9:] for line in stdout_list if line.startswith(b'[ERR_MSG]') ])
    err_code = b'\n'.join([line[10:] for line in stdout_list if line.startswith(b'[ERR_CODE]')])
    if output:
        ret['output'] = output.decode('utf-8')
    if err_msg:
        ret['err_msg'] = err_msg.decode('utf-8')
    if err_code:
        ret['err_code'] = err_code.decode('utf-8')

    return ret
    
        
def _JobNode_result_to_dic(result):
    """
    Args:
    result    (0 | 1 | (0|1, stdout_str) | {'return_code':0|1, ...}): JobNode execution result
    Returns:
        dict<str,JobNode>: for example - { 'name1':JobNode1, 'name2':JobNode2, 'name3':JobNode3, 'name4':JobNode4 }
    Raises:
        Exception: AssertionError
    """
    condition1 = result in (0,1)
    condition2 = isinstance(result, tuple) and len(result)==2 and result[0] in (0,1) and isinstance(result[1], (text_type, binary_type)) 
    condition3 = isinstance(result, dict) and 'return_code' in result and result['return_code'] in (0,1)
    
    assert condition1 + condition2 + condition3 == 1 , 'illegal type of JobNode_execution_result'
    if condition1:  # py_func only.
        return {
            "return_code": result ^ 1
        }
    elif condition2:   # script(executable_cmd) only, after called a executable_script, apscli would draw info from original script's total output
        return _cmd_result_to_dic(result)
    else:  # py_func only.
        result['return_code'] = result['return_code'] ^ 1
        return result


def _run_func_in_process(job):
    for path in set( os.environ.get('PYTHONPATH', '').split(':') ).union( set(job.action['path']) ):
        if path not in sys.path:
            sys.path.append(path)
    # return getattr(import_module(job.action['module'][0:-3]), job.action['function'])
    return getattr(import_module(job.action['module']), job.action['function'])


def _run_cmd_in_thread(job, real_time_print=True):
    
    if 'env' in job.action:
        new_env = dict(os.environ, **{str(k): str(v) for k,v in job.action['env'].items()}) # leave unknown vars unchanged
    else:   
        new_env = os.environ.copy()

    try:
        cmd = shlex.split(job.action['cmd'])[0]
        cmd_params = shlex.split(job.action['cmd'])[1:]

        for k,v in job.param.items():
            cmd_params.extend( (('-{}' if len(k)==1 else '--{}').format(k), v) )      # ToDo! discussion with Liqin, pay attention here!
        cmd_param_str = ' '.join(map('"{}"'.format, cmd_params))
        print( 'cmd_param_str({0}):{1}'.format(job.name, cmd_param_str) )

        def _glob(l):
            l1 = [glob.glob(x) for x in l]
            for i in range(len(l1)):
                if len(l1[i])==0:
                    l1[i] = [l[i]]
            return l1

        from os.path import expandvars, expanduser
        expand = lambda x: expanduser(expandvars(x))
        l = _glob( [expand(x) for x in ([cmd] + shlex.split(cmd_param_str))] )
        print( 'l({0}):{1}'.format(job.name, l) )

        job.status = 'starting'
        job.start_time = time.strftime(TIME_FORMAT, time.localtime())

        cmds_list = [item for subl in l for item in subl]
        print('cmds_list:%s' % cmds_list)
        
        # subp = subprocess.Popen(cmds_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False, env=new_env)    # l.flatten(); use cmd_args_list not cmd_args_str as shell=False to avoid injection
        subp = subprocess.Popen(['stdbuf', '-oL'] + cmds_list, stdout=subprocess.PIPE, shell=False, env=new_env, close_fds='posix' in sys.builtin_module_names)
        
        subp_stdout = []

        def _print_subp_stdout():
            for line in iter(subp.stdout.readline, b''):
                print(line.decode('utf-8'))
                sys.stdout.flush()
                subp_stdout.append(line)
            subp.stdout.close()

        if real_time_print:
            t = threading.Thread(target=_print_subp_stdout)
            t.daemon = True  # 'daemon' means this thread is a background_thread, so this thread dies with the program(when main_thread quit()), or else program will wait for this thread to finish, then exit.
            t.start()
        else:
            _print_subp_stdout()

        return_code = subp.wait()  # return_code = subp.returncode
        ret = _JobNode_result_to_dic( (return_code, b''.join(subp_stdout)) )
        print('subp({0}).ret={1}'.format(job.name, ret))
        job.status = 'success' if ret['return_code']==1 else 'failure'        
    except Exception:
        job.status = 'exception'
        ret = {'return_code':0, 'exception':traceback.format_exc(), 'err_code':'apscli_run_cmd_exception'}
        # print(traceback.format_exc())
        print('apscli_run_cmd_exception:\n%s' % cmds_list)
    finally:
        job.result = ret
        job.end_time = time.strftime(TIME_FORMAT, time.localtime())


def execute_workflow(jobnodes, queue=None):
    """
    function to run a workflow with DAG form
    Args:
        jobnodes (dict): a dict of JobNodes(those represent a workflow)
    Returns:
        dict<str,JobNode>, each JobNode with result/status/start_time/end_time... filled in
    Raises:
        Exception: N/A
    """

    if queue is None:
        queue = Queue()

    for each_round_selected_jobs in topo_sort(jobnodes.values()):  # a list of JobNode -> a list of list of JobNode
        each_round_threads = [
            Xprocess(
                name=job.name,
                jobnode=job, 
                queue=queue,
                #target=getattr(import_module(job.action['module'][0:-3]), job.action['function']), kwargs=job.param
                target = _run_func_in_process,
                args=(job,)
            ) if job.action['type']=='api' else threading.Thread(#by default, t.daemon is False, which means all child_threads created from t have `daemon=False by default 
                name=job.name,
                target = _run_cmd_in_thread, 
                args=(job,)
            )
            for job in each_round_selected_jobs if make_decision(job, jobnodes)
        ]

        for t in each_round_threads:
            # log.debug('starting plugin: path=') /root/Terrafrom/archive_tf/tf_1/.terraform/plugins/linux_amd64/terraform-provider-aws_v1.5.0_x4
            t.start()
        for t in each_round_threads:
            t.join()    # current_thread blocked here, waiting for t finish.
        
        while True:
            try:
                jobnode = queue.get(block=False)
                jobnodes[jobnode.name] = jobnode
            except Empty:
                break
    
    return jobnodes


def _wf_return_code_calc(wf):
    assert hasattr(wf, 'decision_expr') and hasattr(wf, 'param'), 'can`t calc wf_return_code without `decision_expr and `param'

    # from my_token import find_var
    # all_decision_jobname = find_var(wf.decision_expr)
    context = {
        # jobname: wf.param[jobname].result['return_code'] for jobname in all_decision_jobname
        jobname: wf.param[jobname].result['return_code'] for jobname in wf.param
    }
    try:
        return int(calc(wf.decision_expr, context)) # constraint to only `True or `False
    except AssertionError:  # at least one node of workflow doesn't start(return_code=='N/A') while need it's return_code to calc the workflow's return_code
        return 0 


def build_workflow_then_exec(fqsn, version=None, wf_param=None, debug=False, post_exec=None, trace_id=None):

    wf = Workflow(fqsn, version, wf_param, trace_id, debug)  # may raise exception, but will be caught by Xprocess

    wf.logger.debug('now executing workflow:%s on %s\n' % (fqsn, socket.getfqdn()))
    wf.status = 'starting'
    wf.start_time = time.strftime(TIME_FORMAT, time.localtime())
    
    try:
        execute_workflow(wf.param)
        wf.result = {
            'return_code': _wf_return_code_calc(wf),  # ^ run_in_sub_process,
            # 'output': { name: job.to_dict() for name,job in wf.param.items() }
        }
        wf.status = 'success' if wf.result['return_code'] == 1 else 'failure'
        # wf.status = 'success' if wf.return_code == 1 else 'failure'
    except:
        wf.result = {'return_code':0, 'exception':traceback.format_exc(), 'err_code':'apscli_run_nested_workflow_exception'}
        wf.status = 'exception'
    wf.end_time = time.strftime(TIME_FORMAT, time.localtime())
    '''
    wf.result = {
        'return_code': int(
            all(
                [ hasattr(wf.param[jobname],'result') and wf.param[jobname].status=='success' for jobname in wf.param ]
            )
        ) ^ run_in_sub_process,
        'param': {
            name: job.to_dict() for name,job in wf.param.items()
        }
    }
    '''

    # jobnodes_not_success = [
    #     node for jobname,node in workflow.items() if hasattr(node,'result') and node.status in ('failure','exception')
    # ]
    # if jobnodes_not_success:
    #     nodes_with_err_msg = [node for node in jobnodes_not_success if 'err_msg' in node.result]
    #     if nodes_with_err_msg:
    #         workflow_result['err_msg'] = {
    #             node.name: node.result['err_msg'] for node in nodes_with_err_msg
    #         }
    #     nodes_with_err_code = [node for node in jobnodes_not_success if 'err_code' in node.result]
    #     if nodes_with_err_code:
    #         workflow_result['err_code'] = {
    #             node.name: node.result['err_code'] for node in nodes_with_err_code
    #         }

    # if debug:
    #     if console not in wf.logger.handlers:
    #         wf.logger.addHandler(console)
    # else:
    #     wf.logger.removeHandler(console)

    wf.logger.info('\n%s' % wf)

    if console not in wf.logger.handlers:
        wf.logger.addHandler(console)

    from inspect import isfunction
    # return post_exec(wf.result) if isfunction(post_exec) else wf.result
    return post_exec(wf.to_dict()) if isfunction(post_exec) else wf.to_dict()

