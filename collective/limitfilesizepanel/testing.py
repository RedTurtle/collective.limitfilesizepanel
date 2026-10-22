from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.restapi.testing import PLONE_RESTAPI_DX_FIXTURE
from plone.testing import z2

import collective.limitfilesizepanel


class LimitFileSizePanelLayer(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.limitfilesizepanel)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.limitfilesizepanel:default")


LIMITFILESIZEPANEL_FIXTURE = LimitFileSizePanelLayer()


LIMITFILESIZEPANEL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LIMITFILESIZEPANEL_FIXTURE,),
    name="LimitFileSizePanelLayer:IntegrationTesting",
)


LIMITFILESIZEPANEL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LIMITFILESIZEPANEL_FIXTURE,),
    name="LimitFileSizePanelLayer:FunctionalTesting",
)


class LimitFileSizePanelRestapiLayer(PloneSandboxLayer):
    defaultBases = (PLONE_RESTAPI_DX_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=collective.limitfilesizepanel)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.limitfilesizepanel:default")


LIMITFILESIZEPANEL_RESTAPI_FIXTURE = LimitFileSizePanelRestapiLayer()
LIMITFILESIZEPANEL_RESTAPI_TESTING = FunctionalTesting(
    bases=(LIMITFILESIZEPANEL_RESTAPI_FIXTURE, z2.ZSERVER_FIXTURE),
    name="LimitFileSizePanelLayer:RestApiTesting",
)


class LimitFileSizePanelJSONWidgetLayer(PloneSandboxLayer):
    """
    Site with collective.z3cform.jsonwidget installed, to test its uninstall in
    upgrade step to 1400. Remove it when we drop that dependency.
    """

    defaultBases = (LIMITFILESIZEPANEL_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.z3cform.jsonwidget
        import redturtle.reactbundle

        self.loadZCML(package=collective.z3cform.jsonwidget)
        self.loadZCML(package=redturtle.reactbundle)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.z3cform.jsonwidget:default")


LIMITFILESIZEPANEL_JSONWIDGET_FIXTURE = LimitFileSizePanelJSONWidgetLayer()
LIMITFILESIZEPANEL_JSONWIDGET_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LIMITFILESIZEPANEL_JSONWIDGET_FIXTURE,),
    name="LimitFileSizePanelLayer:JSONWidgetIntegrationTesting",
)
