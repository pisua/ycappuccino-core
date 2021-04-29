#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
Starts the Pelix framework and ycappuccino_core ycappuccino_core
"""

import logging
import sys
import os
from ycappuccino.core.utils import MyMetaFinder
sys.path.append(os.getcwd())
# Pelix
from pelix.framework import create_framework
from pelix.ipopo.constants import use_ipopo
import pelix.services
import glob


# ------------------------------------------------------------------------------

# Module version import syson
__version_info__ = (0, 1, 0)
__version__ = ".".join(str(x) for x in __version_info__)


_logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------

import importlib.util

item_manager=None

def set_item_manager(a_item_manager):
    global  item_manager
    item_manager  = a_item_manager


def load_bundle(a_file, a_module_name,a_context):
    global  item_manager

    with open(a_file, "r") as f:
        content = f.read()
        if "pelix" not in a_module_name and "@ComponentFactory" in content and "pelix.ipopo.decorators" in content:
            print(a_module_name)
            a_context.install_bundle(a_module_name).start()
        if "@Item" in content:
            # import this model
            a_context.install_bundle(a_module_name)



def find_and_install_bundle(a_root, a_module_name, a_context):
    for w_file in glob.iglob(a_root + "/*"):
        if os.path.exists(w_file) and \
                "pelix" not in w_file and \
                "pelix" not in a_module_name and \
                "client" not in a_module_name and \
                "framework" not in w_file:
            w_module_name = ""

            if os.path.isdir(w_file):
                if a_module_name == "":
                    w_module_name = w_file.split("/")[-1]
                else:
                    w_module_name = a_module_name + "." + w_file.split("/")[-1]
                find_and_install_bundle(w_file,w_module_name,a_context)
            elif os.path.isfile(w_file) and w_file.endswith(".py"):
                load_bundle(w_file,a_module_name+"."+w_file.split("/")[-1][:-3],a_context)


def init(bundles_main=None):
    """ """
    global item_manager

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
        'ycappuccino.core.bundles.proxy'
    ))

    # Start the framework
    framework.start()

    # Instantiate EventAdmin
    with use_ipopo(framework.get_bundle_context()) as ipopo:
        ipopo.instantiate(pelix.services.FACTORY_EVENT_ADMIN, 'event-admin', {})

    context = framework.get_bundle_context()

    # retrieve item_manager

    # install custom
    w_root =""
    for w_elem in os.getcwd().split("/"):
        w_root=w_root+"/"+w_elem
    find_and_install_bundle(w_root,"",context)

    # Install & start iPOPO
    context.install_bundle('pelix.ipopo.core').start()

    # Install & start the basic HTTP service
    context.install_bundle('pelix.http.basic').start()

    # Instantiate a HTTP service component
    with use_ipopo(context) as ipopo:
        ipopo.instantiate(
            'pelix.http.service.basic.factory', 'http-server',
            {'pelix.http.address': 'localhost',
             'pelix.http.port': 9000})

    # launch bundle main of root application
    if bundles_main is not None:
        for w_bundle in bundles_main:
            context.install_bundle(w_bundle).start()

    item_manager.load_item()

    try:
        # Wait for the framework to stop
        framework.wait_for_stop()
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down")
        framework.stop()
        sys.exit(0)

