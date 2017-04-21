# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.limitfilesizepanel


class LimitFileSizePanelLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.limitfilesizepanel)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.limitfilesizepanel:default')


LIMITFILESIZEPANEL_FIXTURE = LimitFileSizePanelLayer()


LIMITFILESIZEPANEL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(LIMITFILESIZEPANEL_FIXTURE,),
    name='LimitFileSizePanelLayer:IntegrationTesting'
)


LIMITFILESIZEPANEL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(LIMITFILESIZEPANEL_FIXTURE,),
    name='LimitFileSizePanelLayer:FunctionalTesting'
)


LIMITFILESIZEPANEL_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        LIMITFILESIZEPANEL_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='LimitFileSizePanelLayer:AcceptanceTesting'
)
