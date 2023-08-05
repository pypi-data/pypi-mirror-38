# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.immediatecreate


class CollectiveImmediatecreateLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.immediatecreate)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.immediatecreate:default")
        fti = portal.portal_types.Folder
        fti.manage_changeProperties(
            add_view_expr="string:${folder_url}/++addimmediate++Folder"
        )
        behaviors = list(fti.getProperty("behaviors"))
        behaviors += ["plone.richtext", "collective.immediatecreate"]
        behaviors = tuple(behaviors)
        fti.manage_changeProperties(behaviors=behaviors)


COLLECTIVE_IMMEDIATECREATE_FIXTURE = CollectiveImmediatecreateLayer()


COLLECTIVE_IMMEDIATECREATE_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_IMMEDIATECREATE_FIXTURE,),
    name="CollectiveImmediatecreateLayer:IntegrationTesting",
)


COLLECTIVE_IMMEDIATECREATE_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_IMMEDIATECREATE_FIXTURE,),
    name="CollectiveImmediatecreateLayer:FunctionalTesting",
)


COLLECTIVE_IMMEDIATECREATE_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_IMMEDIATECREATE_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="CollectiveImmediatecreateLayer:AcceptanceTesting",
)
