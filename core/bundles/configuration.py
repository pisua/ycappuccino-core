
import os
import logging
from pelix.ipopo.decorators import ComponentFactory, Provides, Validate, \
    Invalidate, Instantiate
import shutil
from ycappuccino.core.api import IConfiguration
FILE_NAME = {'key': 'file_name', 'default': "config.properties"}


@ComponentFactory('Configuration-Factory')
@Provides(IConfiguration.name, controller='_service_controller')
@Instantiate("config")
class Configuration(IConfiguration):

    def __init__(self):
        self._log = logging.getLogger(__name__)
        """ Logger """
        self._file_name = "config.properties"
        """ Configuration file name, injected """
        self._path = None
        """ Path to config file """
        self._dict = {}
        """ Configuration dictionary """
        self._service_controller = True  # service controller

    @Validate
    def validate(self, context=None):
        self._log.info("Validating '{0}' ...".format(__name__))
        self._path = self._get_path()
        self._log.info("Configuration file path: [{0}]".format(self._path))
        self._dict = self.read(self._path) or {}

        self._log.info("Configuration size : [{0}]".format(len(self._dict)))
        self._log.info("Validated.")

    @Invalidate
    def invalidate(self, _):
        self._log.info("Invalidating '{0}' ...".format(__name__))
        self._log.info("Invalidated.")

    def get(self, key, default=None):
        """
        Get configuration value.

        :param key: type: str       Configuration key.
        :return:    type: str       Configuration value, or None.
        """
        w_val = self._dict.get(key, default)
        self._log.info("get config key={}, value={}".format(key, w_val))
        if isinstance(w_val, str) and w_val.lower() == "true":
            return True
        if isinstance(w_val, str) and w_val.lower() == "false":
            return False
        return w_val

    def has(self, key):
        """
        Determine whether a configuration exists.

        :param key: type: str       Configuration key.
        :return:    type: boolean
        """
        return key in self._dict

    def backupConfig(self):
        """ backup last configuration file """
        shutil.copy(self._path, self._path + ".back")

    def set(self, key, value):
        """
        Set configuration value.

        :param key:     type: str   Configuration key.
        :param value:   type: str   Configuration value.
        """
        if "=" in key:
            raise KeyError("Equal sign is not allowed in configuration keys.")
        self._dict[key] = value
        self.write(self._path, self._dict)

    def _get_path(self):
        path = self.get_data()
        if path is not None:
            return os.path.join(path, "conf", self._file_name)
        path = self.get_base()
        if path is not None:
            return os.path.join(path, "base", "conf", self._file_name)
        return self._file_name

    def get_base(self ):
        return os.getcwd()+"/"+"conf"

    def get_data(self ):
        return os.getcwd() + "/"

    @classmethod
    def read(cls, path, aLogger=None):
        if not os.path.isfile(path):
            return None
        props = {}
        with open(path, "rt") as f:
            for line in f:
                conf = line.strip()
                if conf and not conf.startswith("#"):
                    key_value = conf.split("=")
                    key = key_value[0].strip()
                    value = "=".join(key_value[1:]).strip().strip("\"")
                    if value == "true":
                        props[key] = True
                    elif value == "false":
                        props[key] = False
                    else:
                        props[key] = value
                    if (aLogger != None):
                        aLogger.info("Configuration {0}=[{1}]".format(key, value))

        return props

    @classmethod
    def write(cls, path, props):
        if not os.path.isfile(path):
            dir = os.path.dirname(path)
            if dir and dir not in ["", "."] and not os.path.exists(dir):
                os.makedirs(dir)
        # backup old config
        with open(path, "w+") as f:
            for key in props:
                f.write("{}={}\n".format(key, props[key]))
