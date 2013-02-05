# -*- coding: utf-8 -*-

from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName

from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import safe_unicode

from collective.limitfilesizepanel import logger

PROFILE_ID = 'profile-collective.limitfilesizepanel:default'

def migrateTo1000(context):
    setup_tool = getToolByName(context, 'portal_setup')
    setup_tool.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')
    logger.info('Migrated to version 1.1')
