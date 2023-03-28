from pelix.framework import create_framework
import sys, threading
from pelix.ipopo.constants import use_ipopo
import pelix

context = None

def init(a_list_bundle=None):
    global context
    list_bundle = [
        # iPOPO
        'pelix.ipopo.core',
        # Shell bundles
        'pelix.shell.core',
        'pelix.shell.remote',
        'pelix.shell.ipopo',
        # ConfigurationAdmin
        'pelix.services.configadmin',
        'pelix.shell.configadmin',
        'ycappuccino.core.list_components',
        # EventAdmin,
        'pelix.services.eventadmin'
    ]
    if a_list_bundle is not None and len(a_list_bundle)>0:
        for item in a_list_bundle:
            list_bundle.append(item)

    framework = create_framework(tuple(list_bundle))

    # Start the framework
    framework.start()

    # Instantiate EventAdmin
    with use_ipopo(framework.get_bundle_context()) as ipopo:
        ipopo.instantiate(pelix.services.FACTORY_EVENT_ADMIN, 'event-admin', {})

    context = framework.get_bundle_context()

    from ycappuccino.core.list_components import list_component


