# encoding=utf-8

# Set default logging handler to avoid "No handler found" warnings.
import logging
import sys
import os

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())


__author__ = 'Huayang Jiang (huayang.jiang@oracle.com)'
__license__ = 'dual-licensed - Universal Permissive License (UPL) and Apache License 2.0'

from constant import SERVICE_META_REPO_PATH, SERVICE_VERSION_CALCULATE_PATH, LOG_DIR, APSCLI_PATH, CONF_DIR
from util.wf_runtime import build_workflow_then_exec
from util.wf_build import gen_service_category_dic, Workflow, register_fqsn, unregister_fqsn, gen_fqsn_list

__all__ = ['__author__', '__license__', 'build_workflow_then_exec', 'gen_service_category_dic', 'Workflow', 'register_fqsn', 'unregister_fqsn', 'gen_fqsn_list', 'SERVICE_META_REPO_PATH', 'SERVICE_VERSION_CALCULATE_PATH', 'LOG_DIR', 'APSCLI_PATH', 'CONF_DIR']

