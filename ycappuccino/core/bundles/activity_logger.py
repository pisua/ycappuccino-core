'''
Created on 8 dec. 2017

component that provide a activity logger

@author: apisu
'''
# cohorte
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, Instantiate, Property
from ycappuccino.core.api import IActivityLogger, IConfiguration, YCappuccino

import logging
from logging.handlers import RotatingFileHandler

import os

import uuid

levels = {'CRITICAL': logging.CRITICAL,
          'ERROR': logging.ERROR,
          'WARNING': logging.WARNING,
          'INFO': logging.INFO,
          'DEBUG': logging.DEBUG
          }
_logger = logging.getLogger(__name__)

PREFIX_PROPERTY = "activity.logger"
LOG_DIR = "log"
ACTIVITY_NAME = {'key': "name", 'default': "default"}


@ComponentFactory('Activity-Logger-Factory')
@Provides(specifications=[IActivityLogger.name, YCappuccino.name])
@Requires('_config', IConfiguration.name)
@Property('_name', "name", "main")
@Instantiate("logger")
class ActivityLogger(logging.Logger):

    def __init__(self):
        super(ActivityLogger, self).__init__("activity-{}".format(uuid.uuid4().__str__()))
        self._format = None
        self._file_nb = None
        self._file_size = None
        self._level = "INFO"
        self._config = None
        self._context = None  # bundle context
        self._file = None  # path of the file

        self._name = None  # name of the component

    def get_prefix_config(self):
        """ get the prefix for activity log depending of the instance default activity.logger """
        if self._name == ACTIVITY_NAME["default"]:
            return PREFIX_PROPERTY
        else:
            return PREFIX_PROPERTY + "." + self._name

    def get_default_log_name(self):
        if self._name != ACTIVITY_NAME["default"]:
            return "Log-Activity-{}.log".format(self._name)
        else:
            return "Log-Activity.log"

    def load_configuration(self):
        # load configuration
        w_data_path = os.getcwd()+"/data"
        self._file = os.path.join(w_data_path, LOG_DIR)
        w_file_name = self._config.get(self.get_prefix_config() + ".file", self.get_default_log_name())
        self._file = os.path.join(self._file, w_file_name)

        # see https://docs.python.org/2/library/logging.html#logrecord-attributes
        self._format = self._config.get(self.get_prefix_config() + ".format",
                                        '%(asctime)s;%(levelname)s;%(threadName)s;%(filename)s;%(module)s;%(funcName)s;(%(lineno)d);%(message)s')
        self._file_nb = self._config.get(self.get_prefix_config() + ".nb", 10)
        self._file_size = self._config.get(self.get_prefix_config() + ".size", 20 * 1024 * 1024)
        self._level = self._config.get(self.get_prefix_config() + ".level", "INFO")

    def __str__(self):
        return "filename={}, nb_file={}, file_size={}, level={}".format(self._file, self._file_nb, self._file_size,
                                                                        self._level)

    @Validate
    def validate(self, context):
        _logger.info("ActivityLogger validating...")
        self._context = context
        self.load_configuration()
        _logger.info("activity logger=[{}]".format(self))
        w_data_path = os.getcwd()+"/data"
        if not os.path.isdir(w_data_path):
            os.mkdir(w_data_path)

        w_log_dir = os.path.join(w_data_path, LOG_DIR)
        if not os.path.isdir(w_log_dir):
            os.mkdir(w_log_dir)

        w_handler = RotatingFileHandler(self._file, mode='a', maxBytes=self._file_size, backupCount=self._file_nb,
                                        encoding="utf8", delay=0)
        w_log_formatter = logging.Formatter(self._format)
        w_handler.setFormatter(w_log_formatter)
        if self._level in levels:
            w_handler.setLevel(levels[self._level])
        else:
            _logger.warn("level defined in property {} is not correct. set by default to info".format(self._leve))
            w_handler.setLevel(logging.INFO)
        self.addHandler(w_handler)


        _logger.info("ActivityLogger validated")

    @Invalidate
    def inValidate(self, context):
        _logger.info("ActivityLogger invalidating...")
        _logger.info("ActivityLogger invalidated")
