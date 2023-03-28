#app="all"
from ycappuccino.core.api import IActivityLogger
from ycappuccino.rest_app_base.api import IClobReplaceService

import inspect
import pelix.remote
import logging
import mimetypes
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Provides, Instantiate, Property, UnbindField
import os
from os import path
from ycappuccino.core.decorator_app import App

from pelix.ipopo.decorators import BindField
from ycappuccino.endpoints.api import IClientIndexPath

from ycappuccino.core.utils import bundle_models_loaded_path_by_name

_logger = logging.getLogger(__name__)

COMPONENT_FACTORY = "@ComponentFactory"
COMPONENT_INSTANTIATE = "@Instantiate"
COMPONENT_REQUIRE = "@Requires"
COMPONENT_PROPERTY ="@Property"

@ComponentFactory('IndexEndpoint-Factory')
@Provides(specifications=[pelix.http.HTTP_SERVLET])
@Requires("_log",IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_list_path_client",IClientIndexPath.name, aggregate=True, optional=True)
@Requires("_list_replace_clob",IClobReplaceService.name, aggregate=True, optional=True)
@Instantiate("IndexEndpoint")
@Property("_servlet_path", pelix.http.HTTP_SERVLET_PATH, "/")
@Property("_reject", pelix.remote.PROP_EXPORT_REJECT, pelix.http.HTTP_SERVLET)
@App(name="ycappuccino.rest-app")

class IndexEndpoint(object):

    """ bundle that allow to open index.html.save as root path of http endpoint and provide client bundle on path client """
    def __init__(self):
        self._path_core = os.getcwd()+"/ycappuccino"
        self._path_app = os.getcwd()
        self._list_path_client = []
        self._path_client = {}
        self._file_etag = {}
        self._client_path = inspect.getmodule(self).__file__.replace("core{0}bundles{0}indexEndpoint.py".format(os.path.sep), "client")
        self._map_python_file = {}
        self._list_replace_clob = []
        self._replace_clob = {}
        self._pyscript_core_client_path = None
        self._log = None

    @BindField("_list_path_client")
    def bind_client_path(self, field, a_client_path, a_service_reference):
        if a_client_path.get_priority() not in self._path_client :
            self._path_client[a_client_path.get_priority()] = {
                a_client_path.get_id(): a_client_path
            }
        else:
            self._path_client[a_client_path.get_priority()][a_client_path.get_id()] = a_client_path

        if a_client_path.is_core() and a_client_path.get_type() == "pyscript":
            self._pyscript_core_client_path = a_client_path

    @UnbindField("_list_path_client")
    def unbind_client_path(self, field, a_client_path, a_service_reference):
        if self._path_client[a_client_path.get_priority()] is not None:
            del self._path_client[a_client_path.get_priority()][a_client_path.get_id()]

    @BindField("_list_replace_clob")
    def bind_replace_clob(self, field, a_replace_clob, a_service_reference):
        self._replace_clob[a_replace_clob.extension()] = a_replace_clob


    @UnbindField("_list_replace_clob")
    def unbind_replace_clob(self, field, a_replace_clob, a_service_reference):
        del self._replace_clob[a_replace_clob.extension()]

    def manage_python(self, a_path):
        """ manage python component client"""

        with open(a_path) as f:
            w_lines = f.readlines()
            w_lines_str = ""

            for w_line in w_lines:
               w_lines_str = "".join([w_lines_str, w_line])

            return w_lines_str

    def get_replace_clob_from_extension(self,a_path):
        w_extension = a_path[a_path.index("."):]
        w_list =[]
        for key in self._replace_clob.keys():
            if key in w_extension:
                w_list.append(self._replace_clob[key])
        return w_list

    def manage_clob(self, a_path, a_client_path):
        """ return the content of the file and include html trick if needed """
        w_extension = a_path[a_path.index("."):]
        with open(a_path) as f:
            w_lines = f.readlines()
            w_lines_str = ""
            for w_line in w_lines:
                w_line = self._manage_html_file(w_line)

                w_lines_str = "".join([w_lines_str, w_line])

            w_replace_services = self.get_replace_clob_from_extension(a_path)
            for w_replace_service in w_replace_services:
                w_lines_str = w_replace_service.replace_content(w_lines_str, a_path, a_client_path)

            return w_lines_str

    def manage_blob(self, a_path):
        """ return the content of the blob"""
        if os.path.exists(a_path):
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
        """ manage add client_pyscript_yblues script on header and onload on body"""

        return a_line

    def _get_path(self, a_header, a_base_path, a_file_path):
        """ return the effective file path """
        w_path = a_base_path
        w_client_path = None

        w_file_path = a_file_path

        # not in current app . we check if it exists in ycappuccino
        w_in_known_path = False
        for w_prio in sorted(self._path_client.keys(),reverse=True):
            for w_id in self._path_client[w_prio].keys():
                if self._path_client[w_prio][w_id].is_auth():
                    w_authorization = None
                    if "authorization" in a_header:
                        w_authorization = a_header["authorization"]
                    if not self._path_client[w_prio][w_id].check_auth(w_authorization):
                        return None
                if w_id in w_file_path:
                    w_client_path  =self._path_client[w_prio][w_id]
                    for w_path in w_client_path.get_path() :
                        w_file_path = w_path + a_file_path.replace(w_client_path.get_ui_path()+"/","/")
                        if path.exists(w_file_path):
                            w_in_known_path = True
                            w_client_path = self._path_client[w_prio][w_id]
                            break
                    if not w_in_known_path and w_client_path.get_type() == "pyscript":
                        for w_path in self._pyscript_core_client_path.get_path():
                            w_file_path = w_path +"/"+ "/".join(a_file_path.split("/")[2:]).replace(self._pyscript_core_client_path.get_ui_path() + "/", "/")
                            if path.exists(w_file_path):
                                w_client_path = self._path_client[w_prio][w_id]
                                w_in_known_path = True
                                break
                        if not w_in_known_path:
                            ## it's a server bundle model that we have to load
                            w_file = bundle_models_loaded_path_by_name[".".join(a_file_path.split("/")[2:]).replace(".py","")]
                            if path.exists(w_file):
                                w_file_path = w_file
                                w_in_known_path = True

                if w_in_known_path :
                    break
            if w_in_known_path:
                break
        if not w_in_known_path:
            w_file_path = w_path + "/client" + a_file_path

        if a_file_path.endswith("/"):
            w_file_path = w_file_path + "index.html"
            if not os.path.exists(w_file_path) and w_client_path is not None and w_client_path.get_type() == "pyscript":
                for w_path in self._pyscript_core_client_path.get_path():
                    w_file_path = w_path+"/index.html"
                    if os.path.exists(w_file_path) :
                        break

        return w_file_path, w_client_path

    def _get_path_core(self, a_header,  a_file_path):
        """ return file path for core client  """
        return self._get_path(a_header, self._path_core,a_file_path)

    def _get_path_app(self,  a_header,a_file_path):
        """ return the effective file path client app"""
        return self._get_path(a_header, self._path_app, a_file_path)

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
        w_header = request.get_headers()

        w_file = w_req_path.split("?")[0]
        is_clob = False
        is_blob = False
        w_path, w_client_path = self._get_path_app(w_header,w_file)
        if w_path is None:
            response.send_content(404, "", "text/plain")
            return
        is_python = self._is_python_file(w_path)
        is_clob = self._is_text_file(w_path)
        is_blob = self._is_binary_file(w_path)
        # get date of file and put it as if-none-match
        w_exists_replace = len(self.get_replace_clob_from_extension(w_path))>0

        if  "If-None-Match" in w_header and w_path in self._file_etag:
            w_etag_header = w_header["If-None-Match"]
            if w_etag_header ==  str(os.path.getmtime(w_path)):
                response.send_content(304, "", "")
                return
        if os.path.exists(w_path):
            self._file_etag[w_path] = str(os.path.getmtime(w_path))
            response.set_header("etag",self._file_etag[w_path])

        try:
            w_lines_str = ""
            if is_python:
                w_lines_str = self.manage_python(w_path)
            if is_clob or is_python:
                w_lines_str = self.manage_clob(w_path, w_client_path)
            elif is_blob:
                w_lines_str = self.manage_blob(w_path)
            if w_lines_str is None:
                response.send_content(404,"")
            else:
                response.send_content(200, w_lines_str, mimetypes.guess_type(w_req_path)[0])
        except Exception as e:
            self._log.info("fail to return content for path {}".format(w_path))
            self._log.exception(e)
            response.send_content(500, "", "text/plain")

    @Validate
    def validate(self,context=None):
        self._log.info("validating...")
        self._log.info("validated")