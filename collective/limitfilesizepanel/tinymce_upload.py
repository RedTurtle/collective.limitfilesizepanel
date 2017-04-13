# -*- coding: utf-8 -*-
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from Products.TinyMCE.adapters.Upload import Upload as BaseUpload
from Acquisition import aq_inner
from Acquisition import aq_parent
from zExceptions import BadRequest
from zope.component import getUtility
from plone import api
from plone.api.exc import InvalidParameterError
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces._content import IFolderish
from plone.outputfilters.browser.resolveuid import uuidFor
from Products.validation.i18n import safe_unicode

import pkg_resources
try:
    pkg_resources.get_distribution('plone.dexterity')
    pkg_resources.get_distribution('plone.namedfile')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY = False
    pass
else:
    HAS_DEXTERITY = True
    from plone.dexterity.interfaces import IDexterityContent
    from plone.namedfile.interfaces import INamedImageField
    from plone.rfc822.interfaces import IPrimaryFieldInfo

from Products.TinyMCE.interfaces.utility import ITinyMCE
from Products.TinyMCE import TMCEMessageFactory as _
from zope.i18n import translate
from collective.limitfilesizepanel.interfaces import ICheckSizeUtility
from collective.limitfilesizepanel import messageFactory as lfspmf
from zope.component import getUtility

import logging
logger = logging.getLogger(__name__)


class Upload(BaseUpload):

    def upload(self):
        """Adds uploaded file"""
        object = aq_inner(self.context)
        if not IFolderish.providedBy(object):
            object = aq_parent(object)

        context = self.context
        request = context.REQUEST
        ctr_tool = getToolByName(self.context, 'content_type_registry')
        utility = getUtility(ITinyMCE)

        id = request['uploadfile'].filename
        content_type = request['uploadfile'].headers["Content-Type"]
        typename = ctr_tool.findTypeName(id, content_type, "")

        # Permission checks based on code by Danny Bloemendaal

        # 1) check if the current user has permissions to add stuff
        if not context.portal_membership.checkPermission('Add portal content', context):
            return self.errorMessage(_("You do not have permission to upload files in this folder"))

        # 2) check image types uploadable in folder.
        #    priority is to content_type_registry image type
        allowed_types = [t.id for t in context.getAllowedTypes()]
        if typename in allowed_types:
            uploadable_types = [typename]
        else:
            uploadable_types = []

        if content_type.split('/')[0] == 'image':
            image_portal_types = utility.imageobjects.split('\n')
            uploadable_types += [t for t in image_portal_types
                                    if t in allowed_types
                                       and t not in uploadable_types]

        # limitfilesizepanel check
        size_check = self.check_file_size(uploadable_types, request)
        if size_check and not size_check.get('valid', False):
            msg = lfspmf('validation_error',
                    default=u"Validation failed. Uploaded data is too large: ${size}MB (max ${max}MB)",
                    mapping={
                        'size': safe_unicode("%.1f" % size_check.get('sizeMB')),
                        'max': safe_unicode("%.1f" % size_check.get('maxsize'))
                    }
                    )
            return self.errorMessage(msg)
        # end otf limitfilesizepanel check

        # Get an unused filename without path
        id = self.cleanupFilename(id)

        title = request['uploadtitle']
        description = request['uploaddescription']

        for metatype in uploadable_types:
            try:
                newid = context.invokeFactory(type_name=metatype, id=id)
                if newid is None or newid == '':
                    newid = id

                obj = getattr(context, newid, None)
                if HAS_DEXTERITY and IDexterityContent.providedBy(obj):
                    if not self.setDexterityImage(obj):
                        return self.errorMessage(_("The content-type '%s' has no image-field!" % metatype))
                else:
                    pf = obj.getPrimaryField()
                    pf.set(obj, request['uploadfile'])
                break

            except ValueError:
                continue
            except BadRequest:
                return self.errorMessage(_("Bad filename, please rename."))
        else:
            return self.errorMessage(_("Not allowed to upload a file of this type to this folder"))


        # Set title + description.
        # Attempt to use Archetypes mutator if there is one, in case it uses a custom storage
        if title:
            try:
                obj.setTitle(title)
            except AttributeError:
                obj.title = title

        if description:
            try:
                obj.setDescription(description)
            except AttributeError:
                obj.description = description

        if not obj:
            return self.errorMessage(_("Could not upload the file"))

        obj.reindexObject()

        if utility.link_using_uids:
            return self.okMessage("resolveuid/%s" % (uuidFor(obj)))

        return self.okMessage("%s" % (obj.absolute_url()))

    def check_file_size(self, metatypes, request):
        """
        call a support view that check the size of uploaded file
        """
        try:
            helper_view = view = api.content.get_view(
                name='lfsp_helpers_view',
                context=api.portal.get(),
                request=request,
            )
        except InvalidParameterError:
            helper_view = None
        if not helper_view:
            return None
        maxsize = self.get_maxsize(metatypes)
        if not maxsize:
            return None
        return helper_view.check_size(
            maxsize=maxsize,
            uploadfile=request['uploadfile'])

    def get_maxsize(self, metatypes):
        """
        Return max size set in the controlpanel.
        We manage only File and Image types because with tiny you can create
        only an image or a file.
        """
        if len(metatypes) != 1:
            return 0
        file_size = api.portal.get_registry_record(
            'file_size',
            interface=ILimitFileSizePanel)
        image_size = api.portal.get_registry_record(
            'image_size',
            interface=ILimitFileSizePanel)
        if metatypes[0] == 'File' and file_size:
            return float(file_size)
        elif metatypes[0] == 'Image' and image_size:
            return float(image_size)
        return 0
