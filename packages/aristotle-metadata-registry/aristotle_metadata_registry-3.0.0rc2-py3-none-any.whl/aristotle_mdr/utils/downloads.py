from importlib import import_module

from django.conf import settings

from aristotle_mdr import exceptions as registry_exceptions


def get_download_module(module_name):

    import re
    if not re.search(r'^[a-zA-Z0-9\_\.]+$', module_name):  # pragma: no cover
        # bad module_name
        raise registry_exceptions.BadDownloadModuleName("Download name isn't a valid Python module name.")
    try:
        return import_module("%s.downloader" % module_name)
    except:
        debug = getattr(settings, 'DEBUG')
        if debug:
            raise
        return None
