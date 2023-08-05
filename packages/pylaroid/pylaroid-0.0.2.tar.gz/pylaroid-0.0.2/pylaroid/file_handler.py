import logging
from os.path import dirname

from watchdog.events import FileSystemEventHandler

from pylaroid.models import PhotoSheet


class PhotoEventHandler(FileSystemEventHandler):
    """Transform photo into self-developing film"""

    photo_sheet = None

    def on_created(self, event):
        super(PhotoEventHandler, self).on_created(event)

        what = 'directory' if event.is_directory else 'file'
        logging.info("Created %s: %s", what, event.src_path)
        if not self.photo_sheet:
            root_path = dirname(event.src_path)
            self.photo_sheet = PhotoSheet(root_path)
        self.photo_sheet.add_photo(event.src_path)

#    def on_moved(self, event):
#        super(PhotoEventHandler, self).on_moved(event)
#
#        what = 'directory' if event.is_directory else 'file'
#        logging.info("Moved %s: from %s to %s", what, event.src_path,
#                     event.dest_path)
#
#    def on_deleted(self, event):
#        super(PhotoEventHandler, self).on_deleted(event)
#
#        what = 'directory' if event.is_directory else 'file'
#        logging.info("Deleted %s: %s", what, event.src_path)
#
#    def on_modified(self, event):
#        super(PhotoEventHandler, self).on_modified(event)
#
#        what = 'directory' if event.is_directory else 'file'
#        logging.info("Modified %s: %s", what, event.src_path)
#
