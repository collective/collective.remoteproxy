from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class BrowserLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.remoteproxy

        self.loadZCML(package=collective.remoteproxy)

    def setUpPloneSite(self, portal):
        applyProfile(portal, "collective.remoteproxy:default")


COLLECTIVE_REMOTEPROXY_FIXTURE = BrowserLayer()


COLLECTIVE_REMOTEPROXY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_REMOTEPROXY_FIXTURE,), name="BrowserLayer:IntegrationTesting"
)


COLLECTIVE_REMOTEPROXY_FUNCTIONAL = FunctionalTesting(
    bases=(COLLECTIVE_REMOTEPROXY_FIXTURE,), name="BrowserLayer:FunctionalTesting"
)


COLLECTIVE_REMOTEPROXY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_REMOTEPROXY_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name="BrowserLayer:AcceptanceTesting",
)
