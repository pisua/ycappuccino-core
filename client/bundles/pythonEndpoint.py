from server.api import IEndpoint, IActivityLogger

import pelix.http
import pelix.remote
import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, BindField, UnbindField, Instantiate, Property
import os

_logger = logging.getLogger(__name__)


@ComponentFactory('PythonEndpoint-Factory')
@Provides(specifications=[pelix.http.HTTP_SERVLET, IEndpoint.name])
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Instantiate("PythonEndpoint")
@Property("_servlet_path", pelix.http.HTTP_SERVLET_PATH, "/brython")
@Property("_reject", pelix.remote.PROP_EXPORT_REJECT, pelix.http.HTTP_SERVLET)
class PythonEndpoint(object):
    """ bundle that allow to load python source from import """

    def __init__(self):
        self._path = os.getcwd()

    def do_GET(self, request, response):
        """  return file content """
        w_req_path = request.get_path()

        w_path = self._path + "/client/widget" + w_req_path
        # check if python is a core widget
        # else check if it's custom widget

        with open(w_path) as f:
            w_lines = f.readlines()
            response.send_content(200, "\n".join(w_lines), "text/plain")

        response.send_content(404, "", "text/plain")