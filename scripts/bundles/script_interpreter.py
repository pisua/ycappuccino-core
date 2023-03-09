#app="all"
import json

from ycappuccino.core.api import IActivityLogger, IService, YCappuccino
from ycappuccino.storage.api import IManager
from ycappuccino.core.decorator_app import App
from ycappuccino.scripts.api import IScriptInterpreter
import dukpy
import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, Instantiate


_logger = logging.getLogger(__name__)


@ComponentFactory('ScriptInterpreter-Factory')
@Provides(specifications=[IService.name, YCappuccino.name,IScriptInterpreter.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_manager_media", IManager.name, spec_filter="'(item_id=media)'")
@Instantiate("ScriptInterpreter")
@App(name="ycappuccino.script")
class ScriptInterpreter(IService):

    def __init__(self):
        super(ScriptInterpreter, self).__init__();
        self._manager_media = None
        self._log = None
        self._context = None
    def get_name(self):
        return "scripts"

    def is_sercure(self):
        return True



    def post(self, a_header, a_url_path, a_body):
        """ return tuple of 2 element that admit a dictionnary of header and a body"""
        if a_url_path.get_params() is not None and "scriptId" in a_url_path.get_params():
            w_id = a_url_path.get_params()["scriptId"]
            w_resp = self.execute_script(w_id)
            w_meta = {
                "type": "object",
                "size": 1
            }
            return w_meta, w_resp
        raise Exception("no script Id received")

    def is_secure(self):
        return True

    def has_root_path(self):
        return False

    def has_post(self):
        return True

    def has_put(self):
        return False

    def has_get(self):
        return False

    def has_delete(self):
        return False

    def get_extra_path(self):
        """ return the list of extra path that are manage by service """
        return {
            "post": ["{scriptId}/execute"],
            "get": [],
            "put": [],
            "delete": []
        }

    def get_class(self,kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m
    def execute_script(self, a_script_id):
        w_script = self._manager_media.get_one("media", a_script_id, None)
        if w_script is None:
            raise Exception("can't find script from id {}".format(a_script_id))

        w_filename = "{}/{}.{}".format(w_script.get_path(), w_script.get_file_name(), w_script.get_extension())
        w_content = ""
        w_component = {}
        with open(w_filename, "r") as f:
            w_line = f.readline()
            if "//@Require" in w_line:
                w_split_line = w_line.split(" ")

                w_ldap_filter = None
                if len(w_split_line)>2:
                    w_class_name = w_split_line[1]
                    w_variable_name = w_split_line[2]
                    if len(w_split_line) > 3:
                        w_ldap_filter = w_split_line[3]

                    w_ref = self._context.get_service_reference(self.get_class(w_class_name),w_ldap_filter)
                    w_service = self._context.get_service(w_ref)
                    w_component[w_variable_name] = w_service
            else:
                w_content = w_content + w_line + "\n"

        dukpy.evaljs(w_content, components=w_component)
        return {
            "result":"script executed"
        }

    def get(self, a_header, a_url_path):
        return self.post(a_header, a_url_path, None)

    def delete(self, a_header, a_url_path):
        return self.post(a_header, a_url_path, None)

    @Validate
    def validate(self, context):
        self._log.info("ScriptInterpreter validating")
        self._context = context
        self._log.info("ScriptInterpreter validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("ScriptInterpreter invalidating")

        self._log.info("ScriptInterpreter invalidated")



