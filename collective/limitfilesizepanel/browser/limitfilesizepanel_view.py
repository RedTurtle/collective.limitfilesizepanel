# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from Acquisition import aq_base
from Products.validation.i18n import recursiveTranslate
from ZPublisher.HTTPRequest import FileUpload
from collective.limitfilesizepanel import messageFactory as _
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from plone import api
from Products.Five.browser import BrowserView


class View(BrowserView):
    '''
    View for
    '''

    def check_size(self, uploadfile, maxsize):
        """ An example method """
        context = self.context

        result = {
            'maxsize': maxsize,
            'valid': True
        }

        if self.canBypassValidation():
            return result

        new_data_only = api.portal.get_registry_record(
            'new_data_only',
            interface=ILimitFileSizePanel)

        # calculate size
        if (isinstance(uploadfile, FileUpload) or isinstance(uploadfile, file) or
              hasattr(aq_base(uploadfile), 'tell')):
            uploadfile.seek(0, 2)  # eof
            size = uploadfile.tell()
            uploadfile.seek(0)
        elif not new_data_only:
            # we want to validate already saved data. Let use the default Atchetypes validation method
            try:
                size = len(uploadfile)
            except TypeError:
                size = 0
        else:
            # We don't want to validate already saved data
            return True

        size = float(size)
        sizeMB = (size / (1024 * 1024))
        result['sizeMB'] = sizeMB

        if sizeMB > maxsize:
            result['valid'] = False
        return result

    def canBypassValidation(self):
        """
        Check if the user has bypass permission
        """
        sm = getSecurityManager()
        return sm.checkPermission(
            "collective.limitfilesizepanel: Bypass limit size", self.context)
