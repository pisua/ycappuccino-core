from server.api import IEndpoint, IActivityLogger

import pelix.http
import pelix.remote
import logging
import mimetypes
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, BindField, UnbindField, Instantiate, Property
import os

_logger = logging.getLogger(__name__)


@ComponentFactory('IndexEndpoint-Factory')
@Provides(specifications=[pelix.http.HTTP_SERVLET])
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Instantiate("IndexEndpoint")
@Property("_servlet_path", pelix.http.HTTP_SERVLET_PATH, "/")
@Property("_reject", pelix.remote.PROP_EXPORT_REJECT, pelix.http.HTTP_SERVLET)
class IndexEndpoint(object):

    """ bundle that allow to open index.html as root path of http endpoint and provide client bundle on path client """
    def __init__(self):
        self._path = os.getcwd()+"/brython"

    def do_GET(self, request, response):
        """  return file content """
        w_req_path = request.get_path()
        if w_req_path == "/":
            w_req_path = "/index.html"

        w_path = self._path+w_req_path
        with open(w_path) as f:
            w_lines = f.readlines()
            response.send_content(200, "\n".join(w_lines), mimetypes.guess_type(w_req_path)[0])

        response.send_content(404, "", "text/plain")
