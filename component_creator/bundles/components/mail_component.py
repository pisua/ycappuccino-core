#app="all"
from ycappuccino.core.api import IActivityLogger, IService, YCappuccino
from ycappuccino.storage.api import IManager
from ycappuccino.endpoints.api import IJwt
from ycappuccino.core.decorator_app import App

import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Property, Provides, Instantiate, BindField, UnbindField
import hashlib

from ycappuccino.rest_app_base.api import ITenantTrigger
from ycappuccino.storage.api import ITrigger

from ycappuccino.component_creator.api import  IComponentServiceFactory
from ycappuccino.component_creator.bundles.components.api import IMail
# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.message import EmailMessage
_logger = logging.getLogger(__name__)



@ComponentFactory('Mail')
@Provides(specifications=[YCappuccino.name, IMail.name, IComponentServiceFactory.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@App(name="ycappuccino.component_creator")
class ComponentMail(IMail):
    def __init__(self):
        super(IMail, self).__init__();
        self._host = None
        self._port = None

    def send(self, a_subject, a_from, a_to, a_mail):

        msg = EmailMessage()
        msg.set_content(a_mail)

        # me == the sender's email address
        # you == the recipient's email address
        msg['Subject'] = a_subject
        msg['From'] = a_from
        msg['To'] = a_to
        #TODO test with TLS etc...
        with smtplib.SMTP("{}:{}".format(self.host, self.port)) as s:
            s.send_message(msg)
    @Validate
    def validate(self, context):
        self._log.info("ComponentMail validating")
        self._log.info("ComponentMail validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("ComponentMail invalidating")
        self._log.info("ComponentMail invalidated")