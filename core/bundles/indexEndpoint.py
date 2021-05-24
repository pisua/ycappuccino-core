from ycappuccino.core.api import IActivityLogger

import inspect
import pelix.remote
import logging
import mimetypes
import re
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Provides, Instantiate, Property
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

    def manage_python(self, a_path):
        """ manage python component client"""
        with open(a_path) as f:
            w_lines = f.readlines()
            w_lines_str = ""
            to_added_line = []
            to_added_line.append("import pelix")
            for w_line in w_lines:
                w_line = self._manage_python_component(w_line, to_added_line)

                w_lines_str = "".join([w_lines_str, w_line])
            return w_lines_str

    def manage_clob(self, a_path):
        """ return the content of the file and include html trick if needed """
        with open(a_path) as f:
            w_lines = f.readlines()
            w_lines_str = ""
            for w_line in w_lines:
                w_line = self._manage_html_file(w_line)

                w_lines_str = "".join([w_lines_str, w_line])
            return w_lines_str

    def manage_blob(self, a_path):
        """ return the content of the blob"""

        with open(a_path,mode = "rb") as f:
            w_lines = f.read()
            return w_lines

    def _manage_python_component(self,a_line, to_added_line):
        """ manage python component factory ipopo simulation """
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
        """
        :param a_line: r
        :return:
        """
        return "@Provides" in a_line

    def _is_requires(self, a_line):
        """
        :param a_line:
        :return:
        """
        return "@Requires" in a_line

    def _is_html_head(self, a_line):
        """
        return true if it's a head html
        :param a_line:
        :return:
        """
        return "<head>" in a_line

    def _is_html_body(self, a_line):
        """
        return true if it's a body html
        :param a_line:
        :return:
        """
        return "<body>" in a_line

    def _add_brython_script(self, a_line):
        """
        add automicatically brython script
        :param a_line:
        :return:
        """
        w_line = a_line + "\n" \
                 + "<script type=\"text/javascript\" src=\"brython.js\"></script>" \
                 + "<script type=\"text/javascript\" src=\"brython_stdlib.js\"></script>"
        return w_line


    def _manage_html_file(self, a_line):
        """ manage add brython script on header and onload on body"""
        if self._is_html_head(a_line):
            return self._add_brython_script(a_line)
        elif self._is_html_body(a_line):
            return a_line.replace("body","body onload=\"brython(1)\"")
        else:
            return a_line

    def _get_path(self, a_file_path):
        """ return the effective file path """
        w_path = self._path
        w_file_path = a_file_path
        if a_file_path.endswith(".py"):
            is_python = True
            w_file_path = w_path + "/client" + a_file_path

        else:
            # not in current app . we check if it exists in ycappuccino
            if "brython" in a_file_path:
                w_file_path = self._brython_path + a_file_path
            else:
                w_file_path = w_path + "/client" + a_file_path

            if a_file_path.endswith("/"):
                w_file_path = w_path + "/client/index.html"

        return w_file_path

    def _is_binary_file(self, a_path):
        """ return true if it's a binary file """
        return ".jpg"  in a_path or ".png"  in a_path or ".svg"  in a_path or ".jpeg"  in a_path or ".ico"  in a_path or ".pdf"  in a_path

    def _is_text_file(self, a_path):
        """ return true if it's a binary file """
        return ".html"  in a_path or ".css"  in a_path or ".js"  in a_path or ".txt"  in a_path or ".ttf"  in a_path or ".map"  in a_path

    def _is_python_file(self, a_path):
        """ return true if it's a binary file """
        return ".py"  in a_path

    def do_GET(self, request, response):
        """  return file content """
        w_req_path = request.get_path()
        w_file = w_req_path.split("?")[0]
        is_clob = False
        is_blob = False
        w_path = self._get_path(w_file)
        is_python = self._is_python_file(w_path)
        is_clob = self._is_text_file(w_path)
        is_blob = self._is_binary_file(w_path)

        if not path.exists(w_path):
            response.send_content(404, "", "text/plain")
            return
        try:
            w_lines_str = ""
            if is_python:
                w_lines_str = self.manage_python(w_path)
            elif is_clob:
                w_lines_str = self.manage_clob(w_path)
            elif is_blob:
                w_lines_str = self.manage_blob(w_path)

            response.send_content(200, w_lines_str, mimetypes.guess_type(w_req_path)[0])
        except Exception as e:
            _logger.info("fail to return content for path {}".format(w_path))
            _logger.exception(e)
            response.send_content(500, "", "text/plain")

    @Validate
    def validate(self,context=None):
        _logger.info("validating...")
        _logger.info("validated")