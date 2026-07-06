# -*- coding: utf-8 -*-
from plone import api
from plone.restapi.interfaces import IExpandableElement
from plone.restapi.interfaces import ISerializeToJsonSummary
from plone.restapi.services import Service
from Products.CMFCore.interfaces import IFolderish
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface

from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel



@implementer(IExpandableElement)
@adapter(Interface, Interface)
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
        data = self.get_sizelimits_data()
        if data:
            result["limit-sizes"] = {"items": data}
        return result

    def get_sizelimits_data(self, context=None):
        if context is None:
            context = self.context
        res = []


        limit_file_size = api.portal.get_registry_record(
            "file_size", interface=ILimitFileSizePanel
        )

        limit_image_size = api.portal.get_registry_record(
                "image_size", interface=ILimitFileSizePanel
        )


        res.append({"file_size_limit": limit_file_size})
        res.append({"image_size_limit": limit_image_size})

        return res


class LimitSizesGet(Service):
    def reply(self):
        data = LimitSizes(self.context, self.request)
        return data(expand=True)["limit-sizes"]