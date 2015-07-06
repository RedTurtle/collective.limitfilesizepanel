# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from collective.limitfilesizepanel import logger
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility


PROFILE_ID = 'profile-collective.limitfilesizepanel:default'


def migrateTo1000(context):
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'rolemap')
    logger.info('Migrated to version 1.1.2')

def migrateTo1100(context):
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
    logger.info('Migrated to version 1.3')
