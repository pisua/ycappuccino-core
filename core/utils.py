#app="all"
import sys
import os.path, glob
import re

from threading import current_thread
from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location
import ycappuccino.core.framework
import logging

_logger = logging.getLogger(__name__)

bundle_loaded = []

bundle_models_loaded_path_by_name = {}

def load_bundle(a_file, a_module_name,a_context):
    """ return list of models to load . need to be load after component"""
    global  item_manager
    try:
        if "/" in a_file and not a_file.split("/")[-1].startswith("test_"):
            with open(a_file, "r") as f:
                content = f.read()
                if "pelix" not in a_module_name and \
                        "@ComponentFactory" in content and \
                        "pelix.ipopo.decorators" in content :
                    if ycappuccino.core.framework.app_name is None:
                        bundle_loaded.append(a_module_name)
                        a_context.install_bundle(a_module_name).start()
                    else:
                        w_app_patterns = []
                        if not "," in ycappuccino.core.framework.app_name:
                            w_app_patterns = [ycappuccino.core.framework.app_name]
                        else:
                            w_app_patterns = ycappuccino.core.framework.app_name.split(",")
                        for w_app_pattern in w_app_patterns:
                            w_app_pattern_applyed = "@App\(name=\""+w_app_pattern.replace("*",".*")
                            w_app_pattern_applyed_2 = "@App\(name='" + w_app_pattern.replace("*", ".*")
                            if re.search(w_app_pattern_applyed, content) or re.search(w_app_pattern_applyed_2, content):
                                bundle_loaded.append(a_module_name)
                                a_context.install_bundle(a_module_name).start()
                                return None

                        if "@App(name=" not in content or "ycappuccino/core/utils" in a_file:
                            bundle_loaded.append(a_module_name)
                            a_context.install_bundle(a_module_name).start()
                            return None

                        print("module {} not loaded ".format(a_file))
                if a_module_name == "ycappuccino.core.models.decoratrs" or a_module_name == "ycappuccino.core.models.utils" or a_module_name == "ycappuccino.core.decorator_app":
                    add_bundle_model(a_module_name, a_file)
                if "@Item" in content :
                    if ycappuccino.core.framework.app_name is None:
                        add_bundle_model(a_module_name, a_file)

                        return a_module_name
                    else:
                        w_app_patterns = []
                        if not "," in ycappuccino.core.framework.app_name:
                            w_app_patterns = [ycappuccino.core.framework.app_name]
                        else:
                            w_app_patterns = ycappuccino.core.framework.app_name.split(",")
                        for w_app_pattern in w_app_patterns:
                            w_app_pattern_applyed = "@App\(name=\""+w_app_pattern.replace("*",".*")
                            w_app_pattern_applyed_2 = "@App\(name='" + w_app_pattern.replace("*", ".*")
                            if re.search(w_app_pattern_applyed, content) or re.search(w_app_pattern_applyed_2, content):
                                add_bundle_model(a_module_name,a_file)
                                return a_module_name

                        if "@App(name=" not in content or "ycappuccino/core/utils" in a_file:
                            add_bundle_model(a_module_name, a_file)
                            return a_module_name
                        print("module {} not loaded ".format(a_file))
    except Exception as e:
        _logger.exception("fail to load bundle {}".format(repr(e)))


def add_bundle_model(a_module_name, a_file, a_cumul=False):
    if not a_cumul and a_module_name not in bundle_models_loaded_path_by_name.keys():
        bundle_models_loaded_path_by_name[a_module_name] = a_file


def find_and_install_bundle(a_root, a_module_name, a_context):
    """ find and install all bundle in path """
    w_list_model = []

    for w_file in glob.iglob(a_root + "/*"):
        if "/" in w_file and not w_file.split("/")[-1].startswith("test_"):

            if os.path.exists(w_file) and \
                    "pelix" not in w_file and \
                    "pelix" not in a_module_name and \
                    "client" not in a_module_name and \
                    "framework" not in w_file:
                w_module_name = ""

                if os.path.isdir(w_file) and os.path.isfile(w_file+"/__init__.py"):
                    if a_module_name == "":
                        w_module_name = w_file.split("/")[-1]
                    else:
                        w_module_name = a_module_name + "." + w_file.split("/")[-1]
                    find_and_install_bundle(w_file,w_module_name,a_context)
                elif os.path.isfile(w_file) and w_file.endswith(".py"):
                    w_module_name = a_module_name+"."+w_file.split("/")[-1][:-3]
                    if w_module_name not in bundle_loaded:
                        w_model = load_bundle(w_file,w_module_name,a_context)
                        if w_model is not None:
                            w_list_model.append(w_model)

        # load models at the end of all component
        for w_model in w_list_model:
            a_context.install_bundle(w_model)


class MyMetaFinder(MetaPathFinder):

    def __init__(self,):
        super(MyMetaFinder).__init__();
        self._context = None
        self._init_bundles = []

    def set_context(self,a_context):
        self._context = a_context
        for w_bundle in self._init_bundles:
            find_and_install_bundle(w_bundle["path"],w_bundle["module"],self._context)
        self._init_bundles = []

    def find_spec(self, fullname, path, target=None):
        if path is not None:
            w_path = path[0]
            w_filename = fullname.split(".")[-1]
            w_fullpath = "{}/{}.py".format(w_path, w_filename)
            if not os.path.isfile(w_fullpath):
                w_fullpath = w_path+"/"+w_filename

            if self._context:
                if fullname not in bundle_loaded:
                    find_and_install_bundle(w_fullpath, fullname, self._context)
            elif "pelix" not in w_fullpath and "core" not in w_fullpath:
                w_module = {
                    "path": w_fullpath,
                    "module": fullname
                }
                self._init_bundles.append(w_module)
        if path is None or path == "":
            path = [os.getcwd()]  # top level import --
            if "." in fullname:
                *parents, name = fullname.split(".")
            else:
                name = fullname

            for entry in path:
                if os.path.isdir(os.path.join(entry, name)):
                    # this module has child modules
                    filename = os.path.join(entry, name, "__init__.py")
                    submodule_locations = [os.path.join(entry, name)]
                else:
                    filename = os.path.join(entry, name + ".py")
                    submodule_locations = None
                if not os.path.exists(filename):
                    continue

                return spec_from_file_location(fullname, filename, loader=MyLoader(filename),submodule_search_locations=submodule_locations)

            return None  # we don't know how to import this


class MyLoader(Loader):
    def __init__(self, filename):
        self.filename = filename

    def create_module(self, spec):
        return None  # use default module creation semantics

    def exec_module(self, module):
        with open(self.filename) as f:
            data = f.read()

        # manipulate data some way...

        exec(data, vars(module))

def install():
    """Inserts the finder into the import machinery"""
    sys.meta_path.insert(0, MyMetaFinder())


def run(a_runnable):
    try:
        if a_runnable != None:
            current_thread().name = a_runnable._name
            return a_runnable.run()
    except Exception as e:
        pass