import zipfile
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from zope.interface import implements, Interface
from zope.publisher.interfaces import IPublishTraverse
from zope import component

from plone.memoize import instance
from plone.memoize import view

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.archiveviewer import _
from collective.archiveviewer import utils
from collective.archiveviewer.interfaces import IArchiveReader


class PublishableString(str):
    """Zope will publish this since it has a __doc__ string"""
    
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return self.data


class IArchiveView(Interface):
    """
    ZipRead view interface
    """


class ContentsView(BrowserView):
    """ @@contents browser view to access zipfile's contents
    """
    implements(IArchiveView, IPublishTraverse)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.accumulated_path = []
        self.content_type = None
        if hasattr(context,'getContentType'):
            self.content_type = context.getContentType() 

    def __call__(self):
        """ This view has no template yet for non-traversing requests """
        pass

    @property
    @instance.memoize
    def reader(self):
        return component.queryAdapter(self.context,
                                      IArchiveReader,
                                      name=self.content_type)

    @property
    @instance.memoize
    def filenames(self):
        return self.reader.list_filenames() 

    def publishTraverse(self, request, name):
        path = '/'.join(self.accumulated_path + [name])
        if (path + '/') in self.filenames:
            self.accumulated_path.append(name)
            return self
        if path in self.filenames:
            content = self.reader.read(path)
            return self.publish_content(name,content)

    @property
    @view.memoize
    def downloadable_ctypes(self):
        return utils.get_downloadable_ctypes()

    def publish_content(self, name, content):
        ext = utils.get_ext(name)
        if ext in self.downloadable_ctypes.keys():
            # set headers properly
            ctype = self.downloadable_ctypes.get(ext)
            self.request.RESPONSE.setHeader('Content-Type',ctype)
            self.request.RESPONSE.setHeader('Content-Length',len(content))
            self.request.RESPONSE.setHeader('Content-Disposition','inline; filename=%s' % name)
        return PublishableString(content)