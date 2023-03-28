#app="all"
from ycappuccino.core.api import IActivityLogger, IService, YCappuccino
from ycappuccino.storage.api import IManager
from ycappuccino.endpoints.api import IJwt
from ycappuccino.core.decorator_app import App

import logging
from pelix.ipopo.decorators import ComponentFactory, Requires, Validate, Invalidate, Provides, Instantiate
import hashlib

from ycappuccino.rest_app_base.api import ITenantTrigger
from ycappuccino.storage.api import ITrigger, IFilter

from ycappuccino.core.models.utils import YDict

from ycappuccino.rest_app_base.models.organization import Organization

from ycappuccino.storage.models.model import Model

_logger = logging.getLogger(__name__)


@ComponentFactory('TenantTrigger-Factory')
@Provides(specifications=[YCappuccino.name,ITenantTrigger.name, ITrigger.name, IFilter.name])
@Requires("_log", IActivityLogger.name, spec_filter="'(name=main)'")
@Requires("_organization_manager", IManager.name, spec_filter="'(item_id=organization)'")
@Requires("_jwt", IJwt.name)
@Instantiate("TenantTrigger")
@App(name="ycappuccino.rest-app")

class TenantTrigger(ITrigger,IFilter):

    def __init__(self):
        super(TenantTrigger, self).__init__("tenantTrigger", "organization",["upsert","delete"], a_synchronous=True, a_post=True);
        self._organization = {}
        self._organization_father = {}
        self._log = None
        self._organization_manager = None


    def _load_tenant_tree(self):
        offset = 0
        has_data = True
        while has_data:
            organizations  = self._organization_manager.get_many("organization",{"size":50,"offset":offset})
            if organizations is not None and len(organizations) > 0:
                for organization in organizations:
                    self._organization[organization.id] = organization
                    if organization.father not in self._organization_father.keys():
                        self._organization_father[organization.father] = [organization.id]
                    else:
                        self._organization_father[organization.father].append(organization.id)
            offset=offset+50
            has_data = len(organizations)>0
    def get_filter(self, a_tenant=None):
        if a_tenant is not None:
            return YDict({
                "key":"_tid",
                "value":{
                    "$in":self.get_sons_tenant(a_tenant)
                }
            })
    def get_sons_tenant(self, a_id):
        res = [a_id]
        self._get_sons_tenant(a_id, res)
        return res

    def _get_sons_tenant(self, a_id, a_res):
        if a_id in self._organization_father.keys():
            for w_id in self._organization_father[a_id]:
                a_res.append(w_id)
                self._get_sons_tenant(w_id,a_res)


    def execute(self, a_action, organization):
        w_org = organization
        if isinstance(w_org,Model):
            w_org = w_org.__dict__
        if a_action == "delete":
            del self._organization[w_org["_id"]]
            del self._organization_father[w_org["_father"]][w_org["_id"]]
        else:
            self._organization[w_org["_id"]] = w_org
        if "_father" in w_org.keys() and w_org["_father"] is not None:
            if w_org["_father"] not in self._organization_father.keys():
                self._organization_father[w_org["_father"]] = [w_org["_id"]]
            else:
                self._organization_father[w_org["_father"]].append(w_org["_id"])


    @Validate
    def validate(self, context):
        self._log.info("TenantService validating")
        self._load_tenant_tree()
        if "system" not in self._organization.keys():
            w_organization = Organization()
            w_organization.id("system")
            w_organization.name("system organization")

            self._organization_manager.up_sert_model(w_organization._id, w_organization)
            self.execute("upsert",w_organization)
        self._log.info("TenantService validated")

    @Invalidate
    def invalidate(self, context):
        self._log.info("TenantService invalidating")

        self._log.info("TenantService invalidated")
