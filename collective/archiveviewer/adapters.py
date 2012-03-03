try:
	from cStringIO import StringIO
except:
	from StringIO import StringIO
import zipfile	

from zope import interface
from zope import component

from collective.archiveviewer.utils import read_zip
from collective.archiveviewer.utils import get_zip_filenames
from collective.archiveviewer.interfaces import IArchiveFile
from collective.archiveviewer.interfaces import IArchiveReader


class BaseReader(object):

	interface.implements(IArchiveReader)
	component.adapts(IArchiveFile)

	def __init__(self, context):
		self.context = context
		self.content = self.get_content()

	def get_content(self):
		raise NotImplementedError()

	def read(self):
		raise NotImplementedError()

	def list_filenames(self):
		raise NotImplementedError()


class ZipReader(BaseReader):

	def get_content(self):
		return read_zip(self.context)

	def read(self, path):
		return self.content.read(path)

	def list_filenames(self):
		return get_zip_filenames(self.content)