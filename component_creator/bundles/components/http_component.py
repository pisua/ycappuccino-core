#app="all"
from ycappuccino.core.api import IActivityLogger, IService, YCappuccino

from ycappuccino.core.decorator_app import App

import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Provides, Instantiate, BindField, UnbindField
import httpx

from ycappuccino.component_creator.api import  IComponentServiceFactory
from ycappuccino.component_creator.bundles.components.api import IHttp

_logger = logging.getLogger(__name__)



@ComponentFactory('Http')
@Provides(specifications=[YCappuccino.name, IHttp.name, IComponentServiceFactory.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@App(name="ycappuccino.component_creator")
class ComponentHttp(IHttp):
    def __init__(self):
        super(IHttp, self).__init__();
        self._scheme = None
        self._host = None
        self._port = None
        self._path = None
        self._headers = {}
    def get(self, a_headers, a_sub_url):
        """ abstract constructor """
        w_headers = a_headers
        for w_key, w_value in self._headers.items():
            if w_key not in w_headers.keys():
                w_headers[w_key] = w_value
        if self._path is not None:
            w_full_url = "{}://{}:{}/{}/{}".format(self._scheme, self._host, self._port, self._path, a_sub_url)
        else:
            w_full_url = "{}://{}:{}/{}".format(self._scheme, self._host, self._port, a_sub_url)
        with httpx.Client() as client:
            response =  client.get(w_full_url, headers=w_headers)
        return response

    def post(self, a_headers, a_sub_url, a_body):
        """ abstract constructor """
        # merge header by default and header received
        w_headers = a_headers
        for w_key, w_value in self._headers.items():
            if w_key not in w_headers.keys():
                w_headers[w_key] = w_value

        if self._path is not None:
            w_full_url = "{}://{}:{}/{}/{}".format(self._scheme, self._host, self._port, self._path, a_sub_url)
        else:
            w_full_url = "{}://{}:{}/{}".format(self._scheme, self._host, self._port, a_sub_url)
        with httpx.Client() as client:
            response = client.post(w_full_url, headers=w_headers, data=a_body)
        return response

    def delete(self, a_headers, a_sub_url):
        """ abstract constructor """
        w_headers = a_headers
        for w_key, w_value in self._headers.items():
            if w_key not in w_headers.keys():
                w_headers[w_key] = w_value
        if self._path is not None:
            w_full_url = "{}://{}:{}/{}/{}".format(self._scheme, self._host, self._port, self._path, a_sub_url)
        else:
            w_full_url = "{}://{}:{}/{}".format(self._scheme, self._host, self._port, a_sub_url)
        with httpx.Client() as client:
            response = client.delete(w_full_url, headers=w_headers)
        return response

    def put(self, a_headers, a_sub_url, a_body):
        """ abstract constructor """
        w_headers = a_headers
        for w_key, w_value in self._headers.items():
            if w_key not in w_headers.keys():
                w_headers[w_key] = w_value
        if self._path is not None:
            w_full_url = "{}://{}:{}/{}/{}".format(self._scheme, self._host, self._port, self._path, a_sub_url)
        else:
            w_full_url = "{}://{}:{}/{}".format(self._scheme, self._host, self._port, a_sub_url)
        with httpx.Client() as client:
            response = client.put(w_full_url, headers=w_headers, data=a_body)
        return response

    @Validate
    def validate(self, context):
        self._log.info("ComponentHttp validating")
        self._log.info("ComponentHttp validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("ComponentHttp invalidating")
        self._log.info("ComponentHttp invalidated")