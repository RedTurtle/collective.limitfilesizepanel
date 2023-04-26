# -*- coding: utf-8 -*-
from collective.limitfilesizepanel import logger
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone import api
from Products.CMFCore.utils import getToolByName

import json

PROFILE_ID = "profile-collective.limitfilesizepanel:default"


def migrateTo1000(context):
    setup_tool = getToolByName(context, "portal_setup")
    setup_tool.runImportStepFromProfile(PROFILE_ID, "plone.app.registry")
    setup_tool.runImportStepFromProfile(PROFILE_ID, "rolemap")
    logger.info("Migrated to version 1.1.2")


def migrateTo1100(context):
    setup_tool = getToolByName(context, "portal_setup")
    setup_tool.runImportStepFromProfile(PROFILE_ID, "plone.app.registry")
    logger.info("Migrated to version 1.3")


def migrateTo1200(context):
    setup_tool = getToolByName(context, "portal_setup")
    setup_tool.runImportStepFromProfile(PROFILE_ID, "browserlayer")
    logger.info("Migrated to version 1200")


def migrateTo1300(context):
    old = api.portal.get_registry_record(
        "types_settings", interface=ILimitFileSizePanel
    )

    new = []
    for data in old:
        new_data = {
            "content_type": data.__Broken_state__.get("content_type", ""),
            "field_name": data.__Broken_state__.get("field_name", ""),
            "size": data.__Broken_state__.get("size", ""),
        }
        new.append(new_data)
    registry = getUtility(IRegistry)

    # remove old field
    del registry.records[
        "collective.limitfilesizepanel.interfaces.ILimitFileSizePanel.types_settings"
    ]
    # re-add it
    setup_tool = getToolByName(context, "portal_setup")
    setup_tool.runImportStepFromProfile(PROFILE_ID, "plone.app.registry")

    # set new value
    api.portal.set_registry_record(
        "types_settings",
        json.dumps(new),
        interface=ILimitFileSizePanel,
    )

    # install new dependency
    setup_tool.runAllImportStepsFromProfile(
        "profile-collective.z3cform.jsonwidget:default"
    )
