from zope import interface

from collective.archiveviewer.utils import is_archive_file
from collective.archiveviewer.interfaces import IArchiveFile


def fileModified(obj, event):
    """ Check if obj is an archive file and mark/unmark accordingly
    """
    changed = False
    if is_archive_file(obj):
        if not IArchiveFile.providedBy(obj):
            interface.alsoProvides(obj,IArchiveFile)
            changed = True
    if changed:
        obj.reindexObject(idxs=['object_provides'])





