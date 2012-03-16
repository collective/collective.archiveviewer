from zope import interface


class IArchiveFile(interface.Interface):
	""" marker interface for archive files
	"""

class IArchiveReader(interface.Interface):
	""" adapter for reading IArchiveFile
	""" 

	def get_content(self):
		""" load the content of the archive
		"""

	def read(self, path):
		""" read the content of the contained file matching path
		"""

	def list_filenames(self):
		""" returns the llist of the filenames
		"""
