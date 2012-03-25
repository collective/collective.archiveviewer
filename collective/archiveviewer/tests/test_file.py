try:
    import json
except ImportError:
    import simplejson as json

import unittest
from os import path
from urllib import quote

from zope.interface import providedBy
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from zope.event import notify
from zope import component

from Products.CMFPlone.utils import _createObjectByType

from Products.Five.testbrowser import Browser
from Products.PloneTestCase.setup import portal_owner, default_password

from collective.archiveviewer.interfaces import IArchiveFile
from collective.archiveviewer.interfaces import IArchiveReader
from collective.archiveviewer.tests.base import TestCase
from collective.archiveviewer import utils


def get_file_content(fname):
    filename = path.join(path.dirname(__file__), fname)
    f = open(filename)
    filedata = f.read()
    f.close()
    return filedata

EXPECTED_FILENAMES = [
    # update me if you update 'example.zip'
    'test_file.txt',
    'test_file.html',
    'folder/',
    'downloadablefile.pdf',
    'downloadablefile.odt',
    'downloadablefile.doc',
    'downloadablefile.docx',
]

EXPECTED_DOWNLOADABLE = ['pdf','odt','doc','docx',] 


class TestUtils(TestCase):

    def setUp(self):
        super(self.__class__, self).setUp()

    def test_zip_utils(self):
        filedata = get_file_content('example.zip')
        reader = utils.read_zip(filedata)
        fnames = utils.get_zip_filenames(reader)
        for i in EXPECTED_FILENAMES:
            self.assertTrue(i in fnames)

    def test_downaloadable_mapping(self):
        pass


class ZipView(TestCase):

    def setUp(self):
        super(self.__class__, self).setUp()

        # load file content
        filedata = get_file_content('example.zip')

        # create an ATFile w/ the content
        self.loginAsPortalOwner()
        # self.portal.invokeFactory("File", 'archive')
        _createObjectByType("File", self.portal, id='archive')
        self.archive = archive = self.portal.archive

        # we should not have IArchiveFile
        self.assertTrue(IArchiveFile not in providedBy(archive))
        archive.setFile(filedata)

        # trigger modified event since we have a subscriber for that
        event = ObjectModifiedEvent(archive)
        notify(event)
        # now we must have IArchiveFile
        self.assertTrue(IArchiveFile in providedBy(archive))

        # look for a zip reader
        zipreader = component.queryAdapter(archive, IArchiveReader,
                                           name=archive.getContentType())
        self.failIf(zipreader is None)

        self.logout()

    def test_view_txt(self):
        browser = Browser()
        browser.open(self.archive.absolute_url() + '/@@contents/test_file.txt')
        self.assertTrue("test file content" in browser.contents)

    def test_view_html(self):
        browser = Browser()
        browser.open(self.archive.absolute_url() + '/@@contents/test_file.html')
        self.assertTrue(browser.isHtml)
        self.assertTrue("<title>test file</title>" in browser.contents)

    def test_view_nested_txt(self):
        browser = Browser()
        browser.open(self.archive.absolute_url() + '/@@contents/folder/other_file.txt')
        self.assertTrue("other file content" in browser.contents)

    def test_downloadable_contents(self):
        browser = Browser()
        downloadable = utils.get_downloadable_ctypes()
        for ext in EXPECTED_DOWNLOADABLE:
            mime = downloadable.get(ext)
            url = '%s/@@contents/downloadablefile.%s' % (self.archive.absolute_url(),
                                                   ext)
            browser.open(url)
            self.assertEqual(browser.headers["Content-type"], mime)


def test_suite():
    import sys
    return unittest.findTestCases(sys.modules[__name__])

