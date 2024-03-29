# -*- coding: utf-8 -*-

from collective.limitfilesizepanel import logger


def uninstall(portal, reinstall=False):
    if not reinstall:
        # Don't want to delete all registry values if a Manager simply
        # reinstall the product from ZMI
        setup_tool = portal.portal_setup
        setup_tool.runAllImportStepsFromProfile(
            "profile-collective.limitfilesizepanel:uninstall"
        )
        logger.info("Uninstall done")
