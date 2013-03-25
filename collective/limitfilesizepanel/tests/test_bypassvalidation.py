from collective.limitfilesizepanel.tests import base
from collective.limitfilesizepanel.patches import canBypassValidation
from unittest import TestSuite, makeSuite


class TestBypassSize(base.MaxSizeTestCase):
    """
    This test cover the bypass size validation feature.
    """

    def testBypassValidation(self):
        """
        """
        #first check that current user can't bypass validation
        self.assertFalse(canBypassValidation(self.portal))
        #now set the permission to "Member" role
        self.portal.manage_permission('collective.limitfilesizepanel: Bypass limit size',
                                      ['Member'],
                                      acquire=False)
        #now check that current user can bypass validation
        self.assertTrue(canBypassValidation(self.portal))

    def tearDown(self):
        """
        revert settings to default
        """
        self.portal.manage_permission('collective.limitfilesizepanel: Bypass limit size',
                                      [],
                                      acquire=False)


def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(TestBypassSize))
    return suite
