# -*- coding: utf-8 -*-
from plone import api
from plone.app.content.browser.file import FileUploadView as BaseFileUploadView

import mimetypes


class FileUpload(BaseFileUploadView):
    """
    add filesize validation to tinymce file upload view
    """

    def __call__(self):
        filedata = self.request.form.get('file', None)
        if not filedata:
            return super(FileUpload, self).__call__()
        filename = filedata.filename
        content_type = mimetypes.guess_type(filename)[0] or ''
        ctr = api.portal.get_tool(name='content_type_registry')
        portal_type = ctr.findTypeName(
            filename.lower(), content_type, '') or 'File'

        helper_view = api.content.get_view(
            name='lfsp_helpers_view',
            context=self.context,
            request=self.context.REQUEST,)

        if helper_view.newDataOnly() and '/edit' in self.request.get('HTTP_REFERER'):  # noqa
            return super(FileUpload, self).__call__()
        maxsize = helper_view.get_maxsize_tiny((portal_type,))
        if not maxsize:
            return super(FileUpload, self).__call__()

        size_check = helper_view.check_size_dx(
            maxsize=maxsize,
            uploadfile=filedata
        )
        if size_check and not size_check.get('valid', False):
            response = self.request.RESPONSE
            response.setStatus(403)
            return size_check.get('error', '')
        return super(FileUpload, self).__call__()
