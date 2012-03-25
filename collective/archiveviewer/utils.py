try:
	from cStringIO import StringIO
except:
	from StringIO import StringIO
import zipfile
import os
import mimetypes 

from zope import component

# from Products.CMFPlone.interfaces import IPropertiesTool
from Products.CMFCore.interfaces import IPropertiesTool

ENABLED_ARCHIVES = ['application/zip',] 

# zip stuff

def read_zip(obj):
    return zipfile.ZipFile(StringIO(str(obj)))

def get_zip_filenames(reader):
    return [entry.filename for entry in reader.filelist]


def is_archive_file(obj):
    # TODO: make this dynamic
    # maybe looking for all registered named adapters?
    if obj.getContentType() in ENABLED_ARCHIVES:
        try:
            reader = read_zip(obj)
            return True
        except (RuntimeError,zipfile.BadZipfile):
            return False
    return False


def get_downloadable_ctypes():
    pprops = component.getUtility(IPropertiesTool)
    settings = pprops.archive_viewer_settings
    res = {}
    for ext in settings.downloadable_content_types:
        mimetype,encoding = mimetypes.guess_type('a.%s' % ext)
        res[ext] = mimetype
    return res

def get_ext(fname):
    return os.path.splitext(fname)[-1].strip('.')

def is_downloadable(ext):
    return ext in get_downloadable_ctypes()
