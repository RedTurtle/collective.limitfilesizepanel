# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Acquisition import aq_parent
from collective.limitfilesizepanel import messageFactory as lfspmf
from plone import api
from plone.api.exc import InvalidParameterError
from plone.outputfilters.browser.resolveuid import uuidFor
from Products.CMFCore.interfaces._content import IFolderish
from Products.CMFCore.utils import getToolByName
from Products.TinyMCE.adapters.Upload import Upload as BaseUpload
from Products.validation.i18n import safe_unicode
from zExceptions import BadRequest

import logging
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

try:
    from Products.TinyMCE import TMCEMessageFactory as _
except ImportError:
    from zope.i18nmessageid import MessageFactory
    _ = MessageFactory('plone.tinymce')


logger = logging.getLogger(__name__)


class Upload(BaseUpload):
    """
    P4 patch
    """
    def upload(self):  # NOQA
        """Adds uploaded file"""
        context = aq_inner(self.context)
        if not IFolderish.providedBy(context):
            context = aq_parent(context)

        request = context.REQUEST
        ctr_tool = getToolByName(context, 'content_type_registry')
        utility = getToolByName(context, 'portal_tinymce')

        uploadfile = request['uploadfile']
        id = uploadfile.filename
        content_type = uploadfile.headers["Content-Type"]
        typename = ctr_tool.findTypeName(id, content_type, "")

        # Permission checks based on code by Danny Bloemendaal

        # 1) check if the current user has permissions to add stuff
        if not context.portal_membership.checkPermission(
                'Add portal content', context):
            return self.errorMessage(
                _("You do not have permission to upload files in this folder"))

        # 2) check image types uploadable in folder.
        #    priority is to content_type_registry image type
        allowed_types = [t.id for t in context.getAllowedTypes()]
        if typename in allowed_types:
            uploadable_types = [typename]
        else:
            uploadable_types = []

        if content_type.split('/')[0] == 'image':
            image_portal_types = utility.imageobjects.split('\n')
            uploadable_types += [
                t for t in image_portal_types
                if t in allowed_types and t not in uploadable_types]

        # limitfilesizepanel check
        size_check = self.check_file_size(uploadable_types, request)
        if size_check and not size_check.get('valid', False):
            msg = lfspmf(
                'validation_error',
                default=u"Validation failed. Uploaded data is too large: ${size}MB (max ${max}MB)",  # NOQA
                mapping={
                    'size': safe_unicode("%.1f" % size_check.get('sizeMB')),
                    'max': safe_unicode("%.1f" % size_check.get('maxsize'))
                }
            )
            return self.errorMessage(msg)
        # end otf limitfilesizepanel check

        # Get an unused filename without path
        id = self.cleanupFilename(id)

        for metatype in uploadable_types:
            try:
                newid = context.invokeFactory(type_name=metatype, id=id)
                if newid is None or newid == '':
                    newid = id
                break
            except ValueError:
                continue
            except BadRequest:
                return self.errorMessage(_("Bad filename, please rename."))
        else:
            return self.errorMessage(
                _("Not allowed to upload a file of this type to this folder"))

        obj = getattr(context, newid, None)

        # Set title + description.
        # Attempt to use Archetypes mutator if there is one, in case it uses
        # a custom storage
        title = request['uploadtitle']
        description = request['uploaddescription']

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

        if HAS_DEXTERITY and IDexterityContent.providedBy(obj):
            if not self.setDexterityItem(obj, uploadfile, id):
                msg = _(
                    "The content-type '${type}' has no image- or file-field!",
                    mapping={'type': metatype})
                return self.errorMessage(msg)
        else:
            # set primary field
            pf = obj.getPrimaryField()
            pf.set(obj, uploadfile)

        if not obj:
            return self.errorMessage(_("Could not upload the file"))

        obj.reindexObject()
        folder = obj.aq_parent.absolute_url()

        if utility.link_using_uids:
            path = "resolveuid/%s" % (uuidFor(obj))
        else:
            path = obj.absolute_url()

        tiny_pkg = pkg_resources.get_distribution("Products.TinyMCE")
        if tiny_pkg.version.startswith('1.2'):
            # Plone < 4.3
            return self.okMessage(path)
        else:
            # Plone >= 4.3
            return self.okMessage(path, folder)

    def check_file_size(self, metatypes, request):
        """
        call a support view that check the size of uploaded file
        """
        try:
            helper_view = api.content.get_view(
                name='lfsp_helpers_view',
                context=api.portal.get(),
                request=request,
            )
        except InvalidParameterError:
            helper_view = None
        if not helper_view:
            return None
        maxsize = helper_view.get_maxsize_tiny(metatypes)
        if not maxsize:
            return None
        return helper_view.check_size(
            maxsize=maxsize,
            uploadfile=request['uploadfile'])
