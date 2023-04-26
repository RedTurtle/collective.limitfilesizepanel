# -*- coding: utf-8 -*-
from collective.limitfilesizepanel.interfaces import ILimitFileSizePanel
from collective.limitfilesizepanel.testing import LIMITFILESIZEPANEL_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from plone.namedfile.field import validate_image_field
from plone.namedfile.field import validate_file_field
from plone.namedfile.interfaces import INamedImageField
from plone.namedfile.interfaces import INamedFileField
from zope.interface import implementer
from plone.namedfile.file import NamedImage
from plone.namedfile.file import NamedFile
from io import BytesIO
from PIL import Image
from transaction import commit
from zope.interface.exceptions import Invalid

import unittest
import json


@implementer(INamedImageField)
class FakeImageField(object):
    def __init__(self, name=""):
        self.name = name

    __name__ = "logo"

    def getName(self):
        return self.name


@implementer(INamedFileField)
class FakeFileField(object):
    def __init__(self, name=""):
        self.name = name

    __name__ = "file"

    def getName(self):
        return self.name


class TestValidation(unittest.TestCase):

    layer = LIMITFILESIZEPANEL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.registry = queryUtility(IRegistry)

        api.portal.set_registry_record(
            "new_data_only",
            False,
            interface=ILimitFileSizePanel,
        )

        api.portal.set_registry_record(
            "file_size",
            1,
            interface=ILimitFileSizePanel,
        )
        api.portal.set_registry_record(
            "image_size",
            1,
            interface=ILimitFileSizePanel,
        )

        api.portal.set_registry_record(
            "types_settings",
            json.dumps(
                [{"content_type": "News Item", "field_name": "image", "size": 2}]
            ),
            interface=ILimitFileSizePanel,
        )
        commit()

    def generate_image(self, needed_size=1):
        # Set the dimensions of the image
        width = 1024
        height = 1024
        img_size = 1024 * 1024 * needed_size
        # Create a new image with white background
        image = Image.new("RGB", (width, height), (255, 255, 255))

        # Save the image to an in-memory buffer as a JPEG file with maximum quality
        buffer = BytesIO()
        image.save(buffer, format="JPEG", quality=100)

        # Get the size of the image buffer in bytes
        size = buffer.tell()

        # Ensure that the image buffer is exactly 1 MB
        if size < img_size:
            padding = b"\0" * (img_size - size)
            buffer.write(padding)

        return buffer

    def test_validate_image_field(self):
        # field is empty
        field = FakeImageField()
        field.context = self.portal

        image = NamedImage()

        # 1mb image is ok
        image._setData(self.generate_image())
        validate_image_field(field, image)

        image._setData(self.generate_image(2))

        with self.assertRaises(Invalid) as cm:
            validate_image_field(field, image)

        self.assertIn(
            "Validation failed. Uploaded data is too large: 2.0MB (max 1.0MB)",
            str(cm.exception),
        )

    def test_validate_file_field(self):
        # field is empty
        field = FakeFileField()
        field.context = self.portal

        example_file = NamedFile()
        text = " " * (1024 * 1024)
        example_file._setData(BytesIO(text.encode()))
        # 1mb file is ok
        validate_file_field(field, example_file)

        text = " " * (1024 * 1024 * 2)
        example_file._setData(BytesIO(text.encode()))

        with self.assertRaises(Invalid) as cm:
            validate_file_field(field, example_file)

        self.assertIn(
            "Validation failed. Uploaded data is too large: 2.0MB (max 1.0MB)",
            str(cm.exception),
        )

    def test_validate_image_field_on_news(self):
        news = api.content.create(
            type="News Item",
            id="news",
            container=self.portal,
        )

        field = FakeImageField(name="image")
        field.context = news
        image = NamedImage()

        # 1mb image is ok
        image._setData(self.generate_image())
        validate_image_field(field, image)

        # 2mb image is ok
        image._setData(self.generate_image(2))
        validate_image_field(field, image)

        # 3mb image is not ok
        image._setData(self.generate_image(3))

        with self.assertRaises(Invalid) as cm:
            validate_image_field(field, image)

        self.assertIn(
            "Validation failed. Uploaded data is too large: 3.0MB (max 2.0MB)",
            str(cm.exception),
        )
