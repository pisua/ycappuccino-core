#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
Starts the Pelix framework and ycappuccino_core ycappuccino_core
"""

import logging
import sys
import os
from ycappuccino.core import utils
from ycappuccino.core.utils import MyMetaFinder


sys.path.append(os.getcwd())
# Pelix
from pelix.framework import create_framework
from pelix.ipopo.constants import use_ipopo
import pelix.services

w_finder = MyMetaFinder()
sys.meta_path.insert(0, w_finder)

# ------------------------------------------------------------------------------

# Module version import syson
__version_info__ = (0, 1, 0)
__version__ = ".".join(str(x) for x in __version_info__)


_logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------

import importlib.util

item_manager=None
context = None

def set_item_manager(a_item_manager):
    global item_manager
    item_manager  = a_item_manager

subsystem = []

def init_subsystem(a_path):
    global context
    subsystem.append(a_path)
    utils.find_and_install_bundle(a_path,"",context)

def init(root_dir=None, port=9000):
    """ """
    global item_manager
    global context

    # Create the Pelix framework
    framework = create_framework((
        # iPOPO
        'pelix.ipopo.core',

        # Shell bundles
        'pelix.shell.core',
        'pelix.shell.console',
        'pelix.shell.remote',
        'pelix.shell.ipopo',

        # ConfigurationAdmin
        'pelix.services.configadmin',
        'pelix.shell.configadmin',

        # EventAdmin,
        'pelix.services.eventadmin',
        'pelix.shell.eventadmin',
        'ycappuccino.core.bundles.managers',
        'ycappuccino.core.bundles.item_manager',
        'ycappuccino.core.bundles.configuration',
        'ycappuccino.core.bundles.jwt',
        'ycappuccino.core.bundles.endpoints',
        'ycappuccino.core.bundles.indexEndpoint',
        'ycappuccino.core.bundles.activity_logger',
        'ycappuccino.core.bundles.proxy',
        'ycappuccino.core.bundles.core_bootstrap',

        # bundle core model
        'ycappuccino.core.model.account',
        'ycappuccino.core.model.login',
        'ycappuccino.core.model.role',
        'ycappuccino.core.model.model'

    ))

    # Start the framework
    framework.start()

    # Instantiate EventAdmin
    with use_ipopo(framework.get_bundle_context()) as ipopo:
        ipopo.instantiate(pelix.services.FACTORY_EVENT_ADMIN, 'event-admin', {})

    context = framework.get_bundle_context()

    # retrieve item_manager

    # install custom
    # load ycappuccino
    w_root =""
    if root_dir is  None:
        root_dir = os.getcwd()
    for w_elem in root_dir.split("/"):
        w_root=w_root+"/"+w_elem

    utils.find_and_install_bundle(w_root,"",context)

    # Install & start iPOPO
    context.install_bundle('pelix.ipopo.core').start()

    # Install & start the basic HTTP service
    context.install_bundle('pelix.http.basic').start()

    # Instantiate a HTTP service component
    with use_ipopo(context) as ipopo:
        ipopo.instantiate(
            'pelix.http.service.basic.factory', 'http-server',
            {'pelix.http.port': port})



    item_manager.load_item()
    w_finder.set_context(context)
    try:
        # Wait for the framework to stop
        framework.wait_for_stop()
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down")
        framework.stop()
        sys.exit(0)

