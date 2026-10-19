# -*- coding: utf-8 -*-
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanelLayer
from plone import api
from plone.api.exc import InvalidParameterError
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.services import Service
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


EXPOSE_PERMISSION = "collective.limitfilesizepanel: Expose size limits"
BYPASS_PERMISSION = "collective.limitfilesizepanel: Bypass limit size"


@implementer(IExpandableElement)
@adapter(Interface, ILimitFileSizePanelLayer)
class LimitSizes(object):
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, expand=False):
        result = {
            "limit-sizes": {
                "@id": "{}/@limit-sizes".format(self.context.absolute_url())
            }
        }
        if not expand:
            return result
        # the expander is reachable by anyone with ?expand=limit-sizes, so
        # check the same permission of the @limit-sizes service
        if not api.user.has_permission(EXPOSE_PERMISSION, obj=self.context):
            return result
        result["limit-sizes"]["items"] = self.get_sizelimits_data()
        return result

    def get_registry_value(self, name):
        try:
            return api.portal.get_registry_record(name, interface=ILimitFileSizePanel)
        except InvalidParameterError:
            return None

    def get_sizelimits_data(self):
        """
        Sizes are in MB. 0 means no limit, None means that the value is not
        set in the registry.
        """
        return {
            "file_size_limit": self.get_registry_value("file_size"),
            "image_size_limit": self.get_registry_value("image_size"),
            "can_bypass": bool(
                api.user.has_permission(BYPASS_PERMISSION, obj=self.context)
            ),
        }


class LimitSizesGet(Service):
    def reply(self):
        data = LimitSizes(self.context, self.request)
        return data(expand=True)["limit-sizes"]
