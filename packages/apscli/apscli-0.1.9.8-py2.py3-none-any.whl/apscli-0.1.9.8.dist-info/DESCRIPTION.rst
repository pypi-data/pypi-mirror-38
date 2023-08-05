Apscli
------------------------------
A general purpose workflow engine, also an orchestration tool, written in Python - Python 2.7+ and 3.5+ are supported.


Description
------------------------------
Modern DataCenters often need run all kinds of operation/maintenance jobs, from allocating infrastructure resources(VMs, IPs, Storages...) to install&deploy 

software(Oracle, MySQL, JDK, Redis...). Some jobs run in parallel, however, other jobs which have strict dependency relationship, must run in sequence. 

Often, several different jobs need to be combined into one service to satisfy users' one requirement. How to combine different jobs together into a service? 

How to express dependency relationship between multiple jobs in one service?  One way is to hard-code by manually programing(python or shell scripts), case by case, 

which took a lot of time as each user's operation/maintenance logic is unique, we have to develop services for them one by one, so, you are kidding me. The other way 

however, is let user build his unique service by his own, in a way easy to understand & use: each time there is a new requirement, user express this operation/maintenance

logic by his own. This self-service way decouple jobs / scripts and using of jobs / scripts, which undoubtly provide our user great flexibility and make our scripts easy to 

maintain. Finally what we need is just building & maintaining a reusable common-script-lib, which contains numerous small scripts, each correspondes to one single job. 

On top of the common-lib, all kinds of services can be built & delivered, which are meaningful to our user and can be used directly by our user, each service contains a 

set of reusable jobs / scripts from users' point of view, and more important, service itself is also reusable. 


DAG is used to combine a set of jobs with dependency relationship together to illustrate user's maintenance/operation logic, and as a service / workflow, can be used 

or re-used multiple times by different users. 

To describe DAG, we choose JSON, and to run DAG, we developed Apscli, a general purpose workflow engine. So Apscli is an orchestration & automation tool for CloudOps, 

allowing users to build, change and execute operation as service safely and efficiently. It can manage existing service-providers as well as custom in-house solutions 

as long as the service-provider follows the standard input/output code rule. As a service framework, Apscli organize services in the form of FQSN - Fully Qualified 

Service Name, e.g. oracle.peo.db.inst_restart.

Apscli is now used inside Oracle Cloud Infrastructure. 


Installation
------------------------------
It is highly recommended that a Python virtual environment be used when installing apscli.

Please consult the `Installing packages using pip and virtualenv`__ guide from the Python Software Foundation for more information about virtual environments.

__ https://packaging.python.org/guides/installing-using-pip-and-virtualenv/

Once your virtual environment is active, apscli can be installed using pip.

::

    pip install apscli

Instructions for use
------------------------------
Supposing have a DAG-form workflow with 4 Nodes / Steps like below, each node corresponds to an operation / job, all 4 Nodes forms a diamand:

Node_a <create_vm>           -- top

Node_b<allocate_ip>          -- left

Node_c <allocate_storage>    -- right

Node_d <boot_vm>             -- bottom


Dependency: 'a' execute first, 'b' & 'c' execute after 'a', 'd' execute after 'b' & 'c'


Each node's operation as below:

.. code-block:: pycon

    # /home/suzzy/foo.py

    import time

    def create_vm(vm_id, vm_name):               # <Node_a>'s action is a python_function
        time.sleep(2)  
        return {
            'return_code': 0                     # 'return_code' is a MUST, 0 means success / 1 failure
        }

    def boot_vm(vm_id):                          # <Node_d>'s action is a python_function
        time.sleep(1)
        return {
            'return_code': 0,
            'output': 'vm:%s booted' % vm_id
        }


.. code-block:: pycon

    # /home/suzzy/allocate_ip.py                 # <Node_b>'s action is a python_script

    #!/usr/bin/env python

    import argparse
    import time
    import sys

    p = argparse.ArgumentParser()
    p.add_argument('--ip', type=str)        
    args = p.parse_args()
    time.sleep(5)
    print '[OUTPUT] ip: %s allocated' % args.ip  # line startswith `[OUTPUT]` will be capture by apscli.
    sys.exit(0)                                  # exit(0) means success


.. code-block:: shell

    # /home/suzzy/allocate_storage.sh            # <Node_c>'s action is a shell_script

    #!/bin/sh

    echo [INFO]$bar
    echo [ERR_MSG]err                            # line startswith `[ERR_MSG]` will be captured by apscli, Optional
    echo [OUTPUT]storage01                       # line startswith `[OUTPUT]`  will be captured by apscli, Optional
    exit 1                                       # exit_code: 0 or 1, 0 for success, 1 for failure, is a MUST


Below service definition file(vm_allocation.template) with 4 Nodes can be used to present above DAG diagram:

.. code-block:: javascript

    {
        "a":{
            "prev_nodes":[],
            "action":{                                                            
                "type": "api",                   <== 'api' means a python function is executed
                "function": "create_vm",         <== function_name            
                "module": "foo",                 <== module that contains above funtion
                "path": ["/home/suzzy/"]         <== path that module file exists
            },
            "param":{
                "vm_id":   $vm_id,               <== need two params here, per above function's definition: def create_vm(vm_id, vm_name)
                "vm_name": $vm_name
            }
        },
        "b":{
            "prev_nodes": ["a"],                 <== Node_b has dependency on Node_a
            "action":{
                "type": "cmd",                   <== 'cmd' means a local file with executable permission is executed                            
                "cmd": "/home/suzzy/allocate_ip.py",                           
                "env":{                          <== Environment variables this script needs to run
                    "PATH": "/usr/local/sbin:/usr/local/bin:$PATH"
                }
            },
            "param":{
                "ip": $ip                        <== as len('ip')>1, when calling this script, apscli will put double_dash '--' before param_name, namely `--ip`
            }
        },
        "c":{
            "prev_nodes":["a"],                  <== Node_c also has dependency on Node_a
            "action":{                                                          
                "type": "cmd",                                                    
                "cmd": "/home/suzzy/allocate_storage.sh",                          
                "env": {                         <== Environment variables this script needs to run
                    "bar": 100,                  
                    "PATH": "/usr/local/bin:/u01/SRA/bin:$PATH"
                }
            },
            "param":{
                "storage_name": $s_name          <== '--storage_name'
            }
        },
        "d":{
            "prev_nodes":["b", "c"],             <== Node_d has dependency on both Node_b and Node_c
            "action":{                                                          
                "type": "api",                                                    
                "function": "boot_vm",                           
                "module": "foo",
                "path":["/home/suzzy/"]
            },
            "param":{
                "vm_id": $vm_id
            },
            "decision_expr": "b==1 || c==1"      <== only execute when one of it's prev_nodes(Node_b,Node_c) executed && success
        }
    }

Finally, a JSON format param_file(vm_allocation.param.json) is used to substitute all variables in the service_template_file at runtime.

.. code-block:: javascript

    {
        "vm_id": 1,                              <== Node_a / Node_d params
        "vm_name": "testvm_01",                  <== Node_a params
        "ip": "10.6.1.110",                      <== Node_b params
        "s_name": "storage01"                    <== Node_c params
    }


Now all things done, let's use apscli to run this DAG-diagram / workflow & collect each Node's result:

A. By specifying the template_file corresponding to this service:

- ./apscli.py --wt /home/suzzy/vm_allocation.template --wp /home/suzzy/vm_allocation.param.json -debug

.. code-block:: javascript

    {
        "output": {
            "a": {
                "action": {
                    "function": "create_vm", 
                    "module": "foo", 
                    "path": ["/home/suzzy/"], 
                    "type": "api"
                }, 
                "end_time": "2018-08-20 15:41:26", 
                "prev_nodes": [], 
                "result": {
                    "info": "vm_id:1, vm_name:test01_vm created", 
                    "return_code": 1
                }, 
                "start_time": "2018-08-20 15:41:24", 
                "status": "success"
            }, 
            "b": {
                "action": {
                    "cmd": "/home/suzzy/allocate_ip.py", 
                    "env": {
                        "PATH": "/usr/local/sbin:..."
                    }, 
                    "type": "cmd"
                }, 
                "end_time": "2018-08-20 15:41:32", 
                "prev_nodes": [
                    "a"
                ], 
                "result": {
                    "output": " ip: 1.1.1.1 allocated", 
                    "return_code": 1
                }, 
                "start_time": "2018-08-20 15:41:26", 
                "status": "success"
            }, 
            "c": {
                "action": {
                    "cmd": "/home/suzzy/allocate_storage.sh", 
                    "env": {
                        "PATH": "/usr/local/bin:...", 
                        "bar": 100
                    }, 
                    "type": "cmd"
                }, 
                "end_time": "2018-08-20 15:41:27", 
                "prev_nodes": [
                    "a"
                ], 
                "result": {
                    "err_msg": "err", 
                    "output": "storage01", 
                    "return_code": 0
                }, 
                "start_time": "2018-08-20 15:41:26", 
                "status": "failure"
            }, 
            "d": {
                "action": {
                    "function": "boot_vm", 
                    "module": "actions", 
                    "path": [
                        "/home/suzzy/"
                    ], 
                    "type": "api"
                }, 
                "decision_expr": "b || c", 
                "end_time": "2018-08-20 15:41:33", 
                "prev_nodes": [
                    "c", "b"
                ], 
                "result": {
                    "info": "vm:1 booted", 
                    "return_code": 1
                }, 
                "start_time": "2018-08-20 15:41:32", 
                "status": "success"
            }
        }, 
        "return_code": 0
    }

B. By specifying the FQSN name corresponding to this service:

::

    Services are implemented & published by multiple service-providers in the form of service_template_files deployed on one target host, also one 

    service_template_file can corresponds to one FQSN name, e.g. `/home/suzzy/vm_allocation.template` above can be assigned a FQSN: oracle.peo.cloud.vm_allocation. 

    Thus end users can lookup & access one service thru it's FQSN - Fully Qualified Service Name, right?

    To archive this target, two more things need to do: 

1. Creating one service category file(cloud.json), containing meta information of all services of the same class.

.. code-block:: javascript

    { 

        "vm_allocation": {
            "version": 1.0,                                                                                                                                                                                 <== Optional
            "workflow_template_path":  "/home/suzzy/vm_allocation.template",        <== above service template_file we create, Apscli will run this file as a service
            "desc": "Creating one vm, allocating ip_addr & storage for it, then booting"
            "release": "2018-07-30"                                                                                                                                                                  <==  Optional
        },
        "vlan_allocation": {                                                        <== another cloud service
            "version": 1.0,
            "workflow_template_path":  "/u01/SRA/vlan_allocation.template",
            "desc":  "Creating VLAN for one tenant, enable & active this VLAN",
            "release": "2018-06-30"
        },
        ...
    }

2. Creating a series of directories('oracle/peo/') under 'metadata/' directory, put 'cloud.json' file into it and eventually, such a directory structure('metadata/oracle/peo/cloud.json') 

   is formed. So when use say: pls execute service 'oracle.peo.cloud.vm_allocation', Apscli will find 'cloud.json' file first under 'metadata/oracle/peo/' directory, then locate the 

   'workflow_template_path' item in the 'vm_allocation' section of this file.

   Let's start apscli to run DAG / workflow thru FQSN:

- ./apscli.py -fqsn oracle.peo.cloud.vm_allocation -wp /home/suzzy/vm_allocation.param.json -po



Help
------------------------------
A. How to publish a service?
::

  Service code(one or more scripts / binary files) deployment.
  service_template_file definition, with zero or more parameters appearing in the form of $param1, $param2 ... 
  Service category file preparation, containing service's meta_info such as: service_name, desc, workflow_template_path, release, version …
  Service category file deployment, deploy your category_file into the same directory specified by FQSN, if there are no related directories, create them first.

B. What's the relationship between jobs / micro-services and services from Apscli's point of view?
::

  Micro-service is fine-grained & from the developer’s point of view, there are two kinds of micro-services:

  1.Local micro-service: it may be a python_function / a script_file / a binary_file with executable permission. e.g.
     def foo() / foo.sh / foo.py / foo.pl / foo.rb / foo.out …
  2.Remote micro-service: a synchronous request to a remote end_point, with zero or more parameters. e.g.
     RESTful / SOAP / RPC / MQ …

  Service is coarse-grained & normally composed of one or more jobs / micro-services & from the user’s point of view.

  Micro-service correspondes to a well-tested / reusable common-script-lib, developed & maintained by developer’s team, while
  service_template_file is defined by user by his own, or at least chosen from multiple pre-defined templates at his will.

  What they have in common is, both micro-services and service are `reusable`.


Contributing
------------------------------

apscli is an open source project. See `CONTRIBUTING`__ for details.

Oracle gratefully acknowledges the contributions to apscli that have been made by the community.

__ https://github.com/oracle/apscli/blob/master/CONTRIBUTING.rst



License
------------------------------

Copyright (c) 2018, 2019, Oracle and/or its affiliates. All rights reserved.

Pls refer to the file 'LICENSE.txt'.

