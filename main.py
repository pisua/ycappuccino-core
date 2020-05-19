#!/usr/bin/env python
# -- Content-Encoding: UTF-8 --
"""
Starts the Pelix framework and ycappuccino server
"""

import logging
import sys
import os
sys.path.append(os.getcwd())

# Pelix
from pelix.framework import create_framework
from pelix.ipopo.constants import use_ipopo
import pelix.services
# ------------------------------------------------------------------------------

# Module versiimport syson
__version_info__ = (0, 1, 0)
__version__ = ".".join(str(x) for x in __version_info__)


_logger = logging.getLogger(__name__)

# ------------------------------------------------------------------------------


def main():
    """ """

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

        # YCappuccino server
        'server.bundles.activity_logger',
        'server.bundles.item_manager',
        'server.bundles.storage',
        'server.bundles.configuration',
        'server.bundles.endpoints',
        'client.bundles.indexEndpoint'

    ))

    # Start the framework
    framework.start()

    # Instantiate EventAdmin
    with use_ipopo(framework.get_bundle_context()) as ipopo:
        ipopo.instantiate(pelix.services.FACTORY_EVENT_ADMIN, 'event-admin', {})

    context = framework.get_bundle_context()

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

    try:
        # Wait for the framework to stop
        framework.wait_for_stop()
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down")
        framework.stop()
        sys.exit(0)

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # Setup logs
    logging.basicConfig(level=logging.INFO)


    # Run the script
    main()
