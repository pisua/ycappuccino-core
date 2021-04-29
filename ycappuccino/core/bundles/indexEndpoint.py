from ycappuccino.core.api import IActivityLogger

import inspect
import pelix.http
import pelix.remote
import logging
import mimetypes
import re
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, BindField, UnbindField, Instantiate, Property
import os
from os import path
_logger = logging.getLogger(__name__)

COMPONENT_FACTORY = "@ComponentFactory"


@ComponentFactory('IndexEndpoint-Factory')
@Provides(specifications=[pelix.http.HTTP_SERVLET])
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Instantiate("IndexEndpoint")
@Property("_servlet_path", pelix.http.HTTP_SERVLET_PATH, "/")
@Property("_reject", pelix.remote.PROP_EXPORT_REJECT, pelix.http.HTTP_SERVLET)
class IndexEndpoint(object):

    """ bundle that allow to open index.html as root path of http endpoint and provide client bundle on path client """
    def __init__(self):
        self._path = os.getcwd()
        self._brython_path = inspect.getmodule(self).__file__.replace("core{0}bundles{0}indexEndpoint.py".format(os.path.sep), "brython")
        self._client_path = inspect.getmodule(self).__file__.replace("core{0}bundles{0}indexEndpoint.py".format(os.path.sep), "client")
        self._map_python_file = {}

    def manage_python(self,a_path):
        with open(a_path) as f:
            w_lines = f.readlines()
            w_lines_str = ""
            to_added_line = []
            to_added_line.append("import pelix")
            for w_line in w_lines:
                w_line = self._manage_python_component(w_line, to_added_line)

                w_lines_str = "".join([w_lines_str, w_line])
            return w_lines_str

    def manage_html(self, a_path):
        with open(a_path) as f:
            w_lines = f.readlines()
            w_lines_str = ""
            for w_line in w_lines:
                w_line = self._manage_html_file(w_line)

                w_lines_str = "".join([w_lines_str, w_line])
            return w_lines_str

    def _manage_python_component(self,a_line, to_added_line):
        w_factory_name = self._get_component(a_line)
        if w_factory_name is not None:
            pass
            #to_added_line.append("pelix.ipopo.decorators.ComponentFactoryCall({}.__class__,"+w_factory_name+")")

        w_class_name = self._get_class_name(a_line)
        if w_class_name is not  None:
            for w_line in to_added_line:
                to_added_line[to_added_line.index(w_line)] = w_line.format(w_class_name)

        for w_to_replace in re.findall("(__\w+)+", a_line):
            if "__" not in w_to_replace[2:]:
                # manage replace __ by _ to prevent importation pb
                w_replaced = w_to_replace.replace("__", "_")
                a_line = a_line.replace(w_to_replace, w_replaced)

        a_line = a_line + "\n\n"
        a_line = a_line + "\n".join(to_added_line)
        return a_line

    def _get_component(self, a_line):
        """
        :param a_line:
        :return: string that correspond to the agument passed in componentFactoryp pamameter
        """
        if COMPONENT_FACTORY in a_line:
            return a_line[len(COMPONENT_FACTORY)+1:a_line.index(")")]

    def _get_class_name(self, a_line):
        if "class " in a_line:
            w_class_with_params = a_line.split(" ")[1]
            return w_class_with_params[0:w_class_with_params.index("(")]

    def _is_provided(self, a_line):
        return "@Provides" in a_line

    def _is_requires(self, a_line):
        return "@Requires" in a_line

    def _is_html_head(self, a_line):
        return "<head>" in a_line

    def _is_html_body(self, a_line):
        return "<body>" in a_line

    def _add_brython_script(self, a_line):
        w_line = a_line + "\n" \
                 + "<script type=\"text/javascript\" src=\"brython.js\"></script>" \
                 + "<script type=\"text/javascript\" src=\"brython_stdlib.js\"></script>"
        return w_line


    def _manage_html_file(self, a_line):
        if self._is_html_head(a_line):
            return self._add_brython_script(a_line)
        elif self._is_html_body(a_line):
            return a_line.replace("body","body onload=\"brython(1)\"")

    def do_GET(self, request, response):
        """  return file content """
        w_req_path = request.get_path()
        w_path = self._path
        w_file = w_req_path.split("?")[0]
        is_python = False
        is_html = False
        if w_file.endswith(".py"):
            is_python = True
            w_path = w_path + "/client"+w_file

        else:
            if w_file.endswith("/"):

                w_path = w_path + "/client/index.html"
            else:
                w_path = w_path + "/client"+w_file
            if ".html" in w_path:
                is_html= True

        # check if python is a core widget
        # else check if it's custom widget
        if not path.exists(w_path):
            # not in current app . we check if it exists in ycappuccino
            if "brython" in w_path:
                w_path = self._brython_path+w_file
            else:
                w_path = self._client_path+w_file

        if not path.exists(w_path):
            response.send_content(404, "", "text/plain")
            return
        try:
            if is_python:
                w_lines_str = self.manage_python(w_path)
            else:
                w_lines_str = self.manage_html(w_path)

            response.send_content(200, w_lines_str, mimetypes.guess_type(w_req_path)[0])
        except Exception as e:
            _logger.exception(e)
            response.send_content(500, "", "text/plain")

    @Validate
    def validate(self,context=None):
        _logger.info("validating...")
        _logger.info("validated")