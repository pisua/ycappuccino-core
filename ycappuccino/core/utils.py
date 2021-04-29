import sys
import os.path

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location


class MyMetaFinder(MetaPathFinder):

    def __init__(self,):
        super(MyMetaFinder).__init__();
        self._context = None
        self._init_bundles = []



    def set_context(self,a_context):
        self._context = a_context
        for w_bundle in self._init_bundles:
            self._load_bundle(w_bundle)
        self._init_bundles = []

    def find_spec(self, fullname, path, target=None):
        if path is not None:
            w_path = path[0]
            w_filename = fullname.split(".")[-1]
            w_fullpath = "{}/{}.py".format(w_path, w_filename);

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

