# -*- coding: utf-8 -*-
from plone.namedfile.field import NamedBlobFile, NamedBlobImage
from zope import interface


class ITestSchema(interface.Interface):

    file = NamedBlobFile(
        title=u"Example file",
        required=False,
    )

    image = NamedBlobImage(
        title=u"Example image",
        required=False,
    )


class FileObject(object):

    portal_type = 'File'  # we need a valid portal_type


class NewsObject(object):

    portal_type = 'News Item'  # we need a valid portal_type


class ImageObject(object):

    portal_type = 'Image'  # we need a valid portal_type
