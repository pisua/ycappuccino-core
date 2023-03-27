#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
#app="all"

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

item_manager=None
context = None

def set_item_manager(a_item_manager):
    global item_manager
    item_manager  = a_item_manager

subsystem = []
listener_factory= None

def init_subsystem(a_path):
    global context
    subsystem.append(a_path)
    utils.find_and_install_bundle(a_path, "", context)

app_name = None

class ListenerFactories():
    def __init__(self, a_context):
        self._context = a_context
        self._factory_by_spec = {}
        with use_ipopo(context) as ipopo:
            ipopo.add_listener(self)
        self._notifier_by_spec = {}
    def handle_ipopo_event(self, event):
        '''
        event: A IPopoEvent object
        '''
        # ...
        with use_ipopo(self._context) as ipopo:
            w_description = ipopo.get_factory_details(event.get_factory_name())
            for w_service_spec in w_description["services"][0]:
                if w_service_spec not in self._factory_by_spec:
                    self._factory_by_spec[w_service_spec] = []
                self._factory_by_spec[w_service_spec].append(w_description["name"])
                if w_service_spec in self._notifier_by_spec:
                    for w_notifier in self._notifier_by_spec[w_service_spec]:
                        w_notifier.notify(w_description["name"])

    def subscribe_notifier(self, a_service_spec, a_notifier):
        if a_service_spec not in self._notifier_by_spec:
            self._notifier_by_spec[a_service_spec] = []
        self._notifier_by_spec[a_service_spec].append(a_notifier)

    def get_factories_by_service_specification(self, a_service_spec):
        if a_service_spec in self._factory_by_spec.keys():
            return self._factory_by_spec[a_service_spec]
        return []
def init(root_dir=None, app=None, port=9000):
    """ """
    global item_manager
    global context
    global app_name, listener_factory
    app_name = app
    # Create the Pelix framework
    framework = create_framework((
        # iPOPO
        'pelix.ipopo.core',

        # Shell ycappuccino
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
        'ycappuccino.core.bundles.configuration',
        'ycappuccino.core.bundles.activity_logger',
        'ycappuccino.core.bundles.proxy'

    ))

    # Start the framework
    framework.start()

    # Instantiate EventAdmin
    with use_ipopo(framework.get_bundle_context()) as ipopo:
        ipopo.instantiate(pelix.services.FACTORY_EVENT_ADMIN, 'event-client_pyscript_core', {})

    context = framework.get_bundle_context()

    # retrieve item_manager
    listener_factory = ListenerFactories(context)
    # install custom
    # load ycappuccino
    w_root =""
    if root_dir is  None:
        root_dir = os.getcwd()
    for w_elem in root_dir.split("/"):
        w_root=w_root+"/"+w_elem

    utils.find_and_install_bundle(w_root, "", context)

    # Install & start iPOPO
    context.install_bundle('pelix.ipopo.core').start()

    # Install & start the basic HTTP service
    context.install_bundle('pelix.http.basic').start()

    # Instantiate a HTTP service component
    with use_ipopo(context) as ipopo:
        ipopo.instantiate(
            'pelix.http.service.basic.factory', 'http-server',
            {'pelix.http.port': port})



    w_finder.set_context(context)

    if item_manager is not None:
        item_manager.load_item()

    try:
        # Wait for the framework to stop
        framework.wait_for_stop()
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down")
        framework.stop()
        sys.exit(0)

