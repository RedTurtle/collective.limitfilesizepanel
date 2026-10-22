from collective.limitfilesizepanel import logger
from plone import api
from plone.base.utils import get_installer
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.tool import UNKNOWN
from zope.component import getUtility

PROFILE_ID = "profile-collective.limitfilesizepanel:default"
TYPES_SETTINGS_RECORD = (
    "collective.limitfilesizepanel.interfaces.ILimitFileSizePanel.types_settings"
)
JSONWIDGET = "collective.z3cform.jsonwidget"
JSONWIDGET_PROFILE = f"profile-{JSONWIDGET}:default"


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
    # types_settings has been removed in 1400 (see migrateTo1400), so there is
    # nothing to migrate anymore
    logger.info("Migrated to version 1300")


def migrateTo1400(context):
    # set only the new permission: re-importing the whole rolemap would
    # reset also the roles customized on the site for the other permissions
    portal = api.portal.get()
    portal.manage_permission(
        "collective.limitfilesizepanel: Expose size limits",
        roles=["Manager", "Site Administrator", "Editor", "Contributor"],
        acquire=False,
    )

    # types_settings field has been removed
    registry = getUtility(IRegistry)
    if TYPES_SETTINGS_RECORD in registry.records:
        del registry.records[TYPES_SETTINGS_RECORD]

    # collective.z3cform.jsonwidget is no more a dependency
    installer = get_installer(portal)
    if installer.is_product_installed(JSONWIDGET) and not is_profile_required(
        JSONWIDGET_PROFILE
    ):
        installer.uninstall_product(JSONWIDGET)
        logger.info(f"Uninstalled {JSONWIDGET}")
    logger.info("Migrated to version 1400")


def is_profile_required(profile_id):
    """
    Check if there is some other installed profile that depends on the given one
    """
    setup_tool = api.portal.get_tool("portal_setup")
    for info in setup_tool.listProfileInfo():
        if profile_id not in (info.get("dependencies") or ()):
            continue
        if setup_tool.getLastVersionForProfile(info["id"]) != UNKNOWN:
            return True
    return False
