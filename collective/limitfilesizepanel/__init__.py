# -*- coding: utf-8 -*-

import logging
from zope.i18nmessageid import MessageFactory

project_name = 'collective.limitfilesizepanel'
messageFactory = MessageFactory(project_name)

from collective.limitfilesizepanel import monkeypatch

logger = logging.getLogger(project_name)
