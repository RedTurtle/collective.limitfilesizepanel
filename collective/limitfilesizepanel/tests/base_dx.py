from plone.namedfile.field import NamedBlobFile
from plone.namedfile.field import NamedBlobImage
from zope import interface


class ITestSchema(interface.Interface):
    file = NamedBlobFile(
        title="Example file",
        required=False,
    )

    image = NamedBlobImage(
        title="Example image",
        required=False,
    )


class FileObject:
    portal_type = "File"  # we need a valid portal_type


class NewsObject:
    portal_type = "News Item"  # we need a valid portal_type


class ImageObject:
    portal_type = "Image"  # we need a valid portal_type
