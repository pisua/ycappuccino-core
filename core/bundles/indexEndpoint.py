from ycappuccino.core.api import IActivityLogger

import inspect
import pelix.remote
import logging
import mimetypes
import re
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Provides, Instantiate, Property, UnbindField, BindField
import os
from os import path

from pelix.ipopo.decorators import BindField
from ycappuccino.core.api import IClientIndexPath

_logger = logging.getLogger(__name__)

COMPONENT_FACTORY = "@ComponentFactory"
COMPONENT_INSTANTIATE = "@Instantiate"
COMPONENT_REQUIRE = "@Requires"
COMPONENT_PROPERTY ="@Property"

@ComponentFactory('IndexEndpoint-Factory')
@Provides(specifications=[pelix.http.HTTP_SERVLET])
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_list_path_client",IClientIndexPath.name, aggregate=True, optional=True)
@Instantiate("IndexEndpoint")
@Property("_servlet_path", pelix.http.HTTP_SERVLET_PATH, "/")
@Property("_reject", pelix.remote.PROP_EXPORT_REJECT, pelix.http.HTTP_SERVLET)
class IndexEndpoint(object):

    """ bundle that allow to open index.html as root path of http endpoint and provide client bundle on path client """
    def __init__(self):
        self._path_core = os.getcwd()+"/ycappuccino"
        self._path_app = os.getcwd()
        self._list_path_client = []
        self._path_client = {}

        self._client_path = inspect.getmodule(self).__file__.replace("core{0}bundles{0}indexEndpoint.py".format(os.path.sep), "client")
        self._map_python_file = {}



    @BindField("_list_path_client")
    def bind_client_path(self, field, a_client_path, a_service_reference):
        self._path_client[a_client_path.get_id()] = a_client_path.get_path()

    @UnbindField("_list_path_client")
    def unbind_client_path(self, field, a_client_path, a_service_reference):
        del  self._path_client[a_client_path.get_id()]


    def manage_python(self, a_path):
        """ manage python component client"""
        with open(a_path) as f:
            w_lines = f.readlines()
            w_lines_str = ""
            w_added_lines = []
            w_import_line = None
            w_component = {}
            for w_line in w_lines:
                (w_new_component , w_line, w_added_line_comp, import_pelix) = self._manage_python_component(w_line, w_component)
                w_component = w_new_component
                if import_pelix is not None:
                    w_import_line = import_pelix
                if len(w_added_line_comp) > 0:
                    for w_added in w_added_line_comp:
                        w_added_lines.append(w_added)
                w_lines_str = "".join([w_lines_str, w_line])

            for w_added in w_added_lines:
                w_lines_str = "\n\n".join([w_lines_str,w_added])

            if w_import_line is not None:
                return w_import_line+"\n\n"+w_lines_str
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


    def _call_decorator_factory(self, to_added_line,  a_factory_name, a_component_prop):
        to_added_line.append("pelix.ipopo.decorators.ComponentFactoryCall({}.__class__," + a_factory_name + ")")
        a_component_prop["factory"] = a_factory_name

    def _call_decorator_instance(self, to_added_line, a_instance_name, a_component_prop):
        to_added_line.append("pelix.ipopo.decorators.InstantiateCall({}.__class__,factory=" + a_component_prop["factory"] + ", name=" + a_instance_name + ")")
        a_component_prop["instance"] = a_instance_name

    def _call_decorator_require(self,  to_added_line, a_require_instance, a_component_prop, a_instance):
        to_added_line.append("pelix.ipopo.decorators.RequireCall({}.__class__, instance="+a_instance+",field=" + a_require_instance + ")")
        if "requires" not in a_component_prop:
            a_component_prop["rqeuires"] = []
        a_component_prop["rqeuires"].append(a_require_instance)

    def _call_decorator_property(self,  to_added_line, a_property, a_component_prop, a_instance):
        to_added_line.append("pelix.ipopo.decorators.PropertyCall({}.__class__, instance="+a_instance+",field=" + a_property + ")")
        if "properties" not in a_component_prop:
            a_component_prop["properties"] = []
        a_component_prop["properties"].append(a_property)

    def _manage_python_component(self,a_line, a_component_prop):
        """ manage python component factory ipopo simulation """
        w_factory_name = self._get_component(a_line)
        to_added_line = []
        w_with_import_line = None

        if w_factory_name is not None:
            w_with_import_line = "import pelix"
            self._call_decorator_factory(to_added_line, w_factory_name, a_component_prop)

        w_instance_name = self._get_instantiate(a_line)
        if w_instance_name is not  None:
            self._call_decorator_instance(to_added_line, w_instance_name, a_component_prop)

        w_require_instance = self._get_require(a_line)
        if w_require_instance is not None:
            self._call_decorator_require(to_added_line, w_require_instance, a_component_prop)

        w_property = self._get_property(a_line)
        if w_property is not None:
            self._call_decorator_property(to_added_line, w_property, a_component_prop)

        for w_to_replace in re.findall("(__\w+)+", a_line):
            if "__" not in w_to_replace[2:]:
                # manage replace __ by _ to prevent importation pb
                w_replaced = w_to_replace.replace("__", "_")
                a_line = a_line.replace(w_to_replace, w_replaced)

        return (a_component_prop, a_line, to_added_line, w_with_import_line)

    def _get_instantiate(self, a_line):
        """
        :param a_line:
        :return: string that correspond to the agument passed in componentFactoryp pamameter
        """
        if COMPONENT_INSTANTIATE in a_line:
            return a_line[len(COMPONENT_INSTANTIATE) + 1:a_line.index(")")]

    def _get_require(self, a_line):
        """
        :param a_line:
        :return: string that correspond to the agument passed in componentFactoryp pamameter
        """
        if COMPONENT_REQUIRE in a_line:
            return a_line[len(COMPONENT_REQUIRE) + 1:a_line.index(")")]

    def _get_property(self, a_line):
        """
        :param a_line:
        :return: string that correspond to the agument passed in componentFactoryp pamameter
        """
        if COMPONENT_PROPERTY in a_line:
            return a_line[len(COMPONENT_PROPERTY) + 1:a_line.index(")")]

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



    def _manage_html_file(self, a_line):
        """ manage add brython script on header and onload on body"""

        return a_line

    def _get_path(self, a_base_path, a_file_path):
        """ return the effective file path """
        w_path = a_base_path
        w_file_path = a_file_path
        if a_file_path.endswith(".py"):
            is_python = True
            w_file_path = w_path + "/client" + a_file_path

        else:
            # not in current app . we check if it exists in ycappuccino
            w_in_known_path = False
            for w_id in self._path_client.keys():
                if w_id in a_file_path:
                    w_file_path = self._path_client[w_id] + a_file_path
                    w_in_known_path = True
                    break
            if not w_in_known_path:
                w_file_path = w_path + "/client" + a_file_path

            if a_file_path.endswith("/"):
                w_file_path = w_file_path + "index.html"

        return w_file_path

    def _get_path_core(self, a_file_path):
        """ return file path for core client  """
        return self._get_path(self._path_core,a_file_path)

    def _get_path_app(self, a_file_path):
        """ return the effective file path client app"""
        return self._get_path(self._path_app, a_file_path)

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
        w_path = self._get_path_app(w_file)
        is_python = self._is_python_file(w_path)
        is_clob = self._is_text_file(w_path)
        is_blob = self._is_binary_file(w_path)

        if not path.exists(w_path):
            # check path in core client
            w_path = self._get_path_core(w_file)
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