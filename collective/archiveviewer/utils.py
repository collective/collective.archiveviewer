try:
	from cStringIO import StringIO
except:
	from StringIO import StringIO
import zipfile


ENABLED_ARCHIVES = ['application/zip',] 


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

