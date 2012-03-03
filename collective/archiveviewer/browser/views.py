import zipfile
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from zope.interface import implements, Interface
from zope.publisher.interfaces import IPublishTraverse
from zope import component

from plone.memoize import instance

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.archiveviewer import _
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
        # StringIO(str(self.context)) is probably very inefficient
        # (and is called for each asset of each lesson)
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
            return PublishableString(content)